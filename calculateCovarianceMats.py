from norm import *
from utils import *
from MostJoints.getMostInformativeJoints import *
import numpy as np


def calculateCovarianceMat(X, Y, Z, T, nLevels, overlap=False, timeVar=True):
    nFrames = X.shape[0]
    nJoins = X.shape[1]
    assert Y.shape[0] == nFrames
    assert Z.shape[0] == nFrames
    assert T.shape[0] == nFrames
    assert Y.shape[1] == nJoins
    assert Z.shape[1] == nJoins

    # Normalize skeleton coordinators

    normX = normCord(X)
    normY = normCord(Y)
    normZ = normCord(Z)
    normT = normSeT(T)

    # Create a list of full covariance matrices
    fullCovMats = [[] for i in range(nLevels)]
    covMats = [[] for i in range(nLevels)]

    if timeVar:
        sizeMatrix = nJoins * 3 + 1
    else:
        sizeMatrix = nJoins * 3

    listIdxMatrix = getValueMatrix(sizeMatrix)  # get half of covariance matrix indexes

    for l in range(1, nLevels + 1):
        # Compute covariance matrixes for each level
        nofMats = 2 ** (l - 1)
        sizeWindow = 1 / nofMats
        stepWindow = sizeWindow
        if overlap:
            stepWindow = stepWindow / 2
            nofMats = nofMats * 2 - 1
        startFrameTimes = [stepWindow * i for i in range(nofMats)]
        fullCovMats[l - 1] = [[] for i in range(nofMats)]
        covMats[l - 1] = [[] for i in range(nofMats)]
        for i in range(len(startFrameTimes)):
            startTime = startFrameTimes[i]
            endTime = startFrameTimes[i] + sizeWindow + 2 * np.finfo(float).eps
            sliceInds = [j for j in range(T.shape[0]) if normT[j] >= startTime and normT[j] < endTime]
            sliceX = normX[sliceInds, :]
            sliceY = normY[sliceInds, :]
            sliceZ = normZ[sliceInds, :]
            sliceT = normT[sliceInds]
            if not timeVar:
                sliceVars = np.concatenate((np.concatenate((sliceX, sliceY), axis=1), sliceZ), axis=1)
            else:
                sliceVars = np.concatenate((np.concatenate((sliceX, sliceY), axis=1), np.concatenate((sliceZ, sliceT), axis=1)), axis=1)
            covarianceMat = np.cov(sliceVars.T)
            fullCovMats[l - 1][i] = covarianceMat
            # Get half of covarianceMat and save it as a vector (1-D matrix)
            one_half_vector = []
            mask = np.zeros_like(covarianceMat, dtype=np.bool)
            mask[np.triu_indices_from(mask)] = True
            for row in range(covarianceMat.shape[0]):
                for column in range(covarianceMat.shape[0]):
                    if mask[row][column] == True:
                        one_half_vector.append(covarianceMat[row][column])
            covMats[l - 1][i] = np.asarray(one_half_vector)
        covMats[l - 1] = np.asarray(covMats[l - 1])

    covMats = np.asarray(covMats)
    vec = np.empty(0)
    for i in range(covMats.shape[0]):
        for j in range(covMats[i].shape[0]):
            vec = np.hstack((vec, covMats[i][j]))
    return fullCovMats, vec