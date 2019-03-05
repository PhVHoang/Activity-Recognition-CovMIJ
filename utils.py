import os
import numpy as np

def getAllDataFilename(filepath):
    allFile = []
    for file in os.listdir(filepath):
        if file.endswith(".txt"):
            allFile.append(file)
    return allFile

def getActionLabel(filename):
    with open(filename, "r") as f:
        action_labels = f.readlines()
    action_labels = [int(x.strip()[1:3]) for x in action_labels]
    return action_labels

def getActionSubject(filename):
    with open(filename, "r") as f:
        action_labels = f.readlines()
    action_labels = [int(x.strip()[5:7]) for x in action_labels]
    return action_labels

# sizeMatrix = N
# get index of upper Covariance Matrix

def getValueMatrix(sizeMatrix):
    getMatrixIndex = np.zeros(0)
    tmp = sizeMatrix
    for i in range(sizeMatrix):
        getMatrixIndex = np.append(getMatrixIndex, np.arange(tmp-sizeMatrix+i, tmp))
        tmp += sizeMatrix
    getMatrixIndex = getMatrixIndex.astype(np.uint8)
    return getMatrixIndex

def getIdxMostJoints(matrixJoints):

    return None
