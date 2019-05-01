import numpy as np
import math

def getIndex(Fk, N):
    """
    This method is equivalent to this bellow formula :
        SMIJ = {{idof(sort(fk), n}}
    """
    listIndex = np.argsort(np.argsort(Fk))
    # listIndex = np.flip(listIndex) // TODO
    listIndex = listIndex[0:N]
    return listIndex

# Create a matrix to represent each joint (from 1st-joint to Jth-joint)
def matrixJoints(X,Y,Z):
    """

    :param X: a numpy array for X axis representation with size = (T*nJoints)
    :param Y: a numpy array for Y axis representation with size = (T*nJoints)
    :param Z: a numpy array for Z axis representation with size = (T*nJoints)
    :return:
        A : a numpy array which is combined of X, Y and Z
        A.shape = (T, 3*nJoints)
    """

    # Get number of joints in a skeletal presentation
    nJoints = X.shape[1]
    # Get number of frames in a skeletal sequence
    T = X.shape[0]

    assert Y.shape[1] == nJoints
    assert Z.shape[1] == nJoints
    assert Y.shape[0] == T
    assert Z.shape[0] == T

    A = np.zeros((T, 3*nJoints))
    for t in range(T):
        coordinatorJoint = np.zeros(0)
        for j in range(nJoints):
            coordinatorJoint = np.append(coordinatorJoint, [X[t][j], Y[t][j], Z[t][j]])
        A[t] = coordinatorJoint
    return A

def varianceJoints(segmentedMatrixJoints):
    """
    variance of joints will be used to get the most informative joints by calculating histogram
    Calculate variance in segmented matrixJoints
    :param
    segmentedMatrixJoints: a segmentation of matrixJoints
    :return:
        variance
    """

    meanSegmentedMatrixJoints = np.mean(segmentedMatrixJoints)
    variance = 0
    for i in range(segmentedMatrixJoints.shape[0]):
        variance = variance + math.sqrt(np.sum((segmentedMatrixJoints[i, :] - meanSegmentedMatrixJoints)**2))
    variance = variance/(segmentedMatrixJoints.shape[0]-1)
    return variance

def listVarianceJoints(segmentedMatrixJoints):
    """
    Get information of each joint in a sequence action (aka a sequence skeletal)
    :param segmentedMatrixJoints:
    :return:
        listVariance
    """
    listVariance = np.zeros(0)
    i = 0
    while (i < 60): # 60 = 3*nJoints
        listVariance = np.append(listVariance, varianceJoints(segmentedMatrixJoints[:, i:i+3]))
        i += 3
    return listVariance

def fucksegmentJoints(matrixJoints, Ns, N):
    m, n= matrixJoints.shape
    listSegment = np.zeros(0)
    widthNs = round(m/Ns)
    if (widthNs == m):
        listSegment = getIndex(listVarianceJoints(matrixJoints), N)
    else:
        for i in range(Ns):
            if (i==Ns-1):
                listSegment = np.append(getIndex(listVarianceJoints(matrixJoints[widthNs*i:m]), N))
            else:
                listSegment = np.append(getIndex(listVarianceJoints(matrixJoints[widthNs*i:widthNs*(i+1)]), N))
    return listSegment



def getMostJoints(X,Y,Z, Ns, N):
    """
    Note that we don't segment the matrix Joints here so Ns's value is 1 for every test case


    :param X: x-axis coordinator
    :param Y: y-axis coordinator
    :param Z: z-axis coordinator
    :param Ns: (1)
    :param N: number of joints (20)
    :return:
    """
    matJoints = matrixJoints(X, Y, Z) # aka matrix A of shape (N, 3*nJoints)
    listMostJoints = fucksegmentJoints(matJoints, Ns, N)
    return listMostJoints

