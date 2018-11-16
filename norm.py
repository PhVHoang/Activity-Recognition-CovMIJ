import numpy as np

def normCord(cord):
    minX = np.min(cord)
    maxX = np.max(cord)
    normX = (cord - minX)/(maxX - minX)
    return normX

def normSeT(T):
    minT = np.min(T)
    maxT = np.max(T)
    normT = (T - minT)/(maxT - minT)
    return normT
