import os
import numpy as np
import setting

def getAllDataFilename(filepath):
    allFile = []
    for file in os.listdir(setting.DATA_PATH):
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

