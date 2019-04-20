import numpy as np
from norm import *
from utils import *
from MostJoints.getMostInformativeJoints import *

def calculateCovarianceMats(X, Y, Z, T, nLevels, overlap = False, timeVar=True):
    nFrames = X.shape[0]
    nJoins = X.shape[1]
    assert Y.shape[0] == nFrames
    assert Z.shape[0] == nFrames
    assert T.shape[0] == nFrames
    assert Y.shape[1] == nJoins
    assert Z.shape[1] == nJoins
    assert T.shape[1] == 1

    # Normalize skeleton coordinators

    normX = normCord(X)
    normY = normCord(Y)
    normZ = normCord(Z)
    normT = normSeT(T)

    # Create a list of full covariance matrixes
    fullCovMats = [np.zeros()]

    if timeVar:
        sizeMatrix = nJoins*3+1
    else:
        sizeMatrix = nJoins*3

    listIdxMatrix = getValueMatrix(sizeMatrix) # get half of covariance matrix indexes

    for l in range(nLevels):
        nofMats = 2**(l-1)
        sizeWindow = 1/nofMats
        stepWindow = sizeWindow
        if overlap:
            stepWindow = stepWindow/2
            nofMats = nofMats*2-1
        startFrameTimes = [stepWindow*i for i in range(nofMats)]



    return None