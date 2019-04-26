from calculateCovarianceMats import *
import sklearn
from sklearn.multiclass import OneVsRestClassifier

def sort_and_keep_indexes(Ns, numOfJoints):
    Ns = sorted(range(len(Ns)), key = Ns.__getitem__)
    Ns = Ns[len(Ns)-numOfJoints:]
    return Ns

def get_idx_mostJoints_for_each_action(mostInformativeJointsList, action_label):
    action = mostInformativeJointsList[action_label]
    Ns_4 = [0 for i in range(20)]
    Ns_8 = [0 for i in range(20)]
    Ns_12 = [0 for i in range(20)]

    for i in range(len(action)):
        for j in range(0, 12):
            if j < 4:
                Ns_4[action[i][j] - 1] += 1
            if j < 8:
                Ns_8[action[i][j] - 1] += 1
            if j < 12:
                Ns_12[action[i][j] - 1] += 1
    Ns_4 = sort_and_keep_indexes(Ns_4, 4)
    Ns_8 = sort_and_keep_indexes(Ns_8, 8)
    Ns_12 = sort_and_keep_indexes(Ns_12, 12)
    return Ns_4, Ns_8, Ns_12

def get_matrix(numOfJoints):
    return None