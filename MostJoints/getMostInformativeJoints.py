import os
import numpy as np

def getIndex(Fk, N):

    return None

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




