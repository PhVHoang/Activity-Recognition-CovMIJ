import numpy as np
import math

def getIndex(Fk, N):
    """
    This method is equivalent to this bellow formula :
        SMIJ = {{idof(sort(fk), n}}
    """
    listIndex = Fk.argsort()
    listIndex = np.flip(listIndex)
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
    Get information of each joint in a sequence action (aka a sequence skeletal
    :param segmentedMatrixJoints:
    :return:
        listVariance
    """
    listVariance = np.zeros(0)
    i = 0
    while (i < 60): # 60 = 3*nJoints
        listVariance = np.append(listVariance, varianceJoints(segmentedMatrixJoints[:, i:i+2]))
        i += 3
    return listVariance

def segmentJoints(matrixJoints, Ns, N):
    m, n= matrixJoints.shape()
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
    matJoints = matrixJoints(X, Y, Z)
    listMostJoints = segmentJoints(matJoints, Ns, N)
    return listMostJoints