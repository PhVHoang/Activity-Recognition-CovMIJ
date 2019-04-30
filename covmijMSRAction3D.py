from calculateCovarianceMats import *
from sklearn.multiclass import OneVsRestClassifier
import setting

def sort_and_keep_indexes(Ns, numOfJoints):
    Ns = sorted(range(len(Ns)), key = Ns.__getitem__)
    Ns = Ns[len(Ns)-numOfJoints:]
    return Ns

def get_idx_mostJoints_for_each_action(train_mostInformativeJointsList, action_label):
    action = train_mostInformativeJointsList[action_label]
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
    Ns_4 = np.asarray(sort_and_keep_indexes(Ns_4, 4))
    Ns_8 = np.asarray(sort_and_keep_indexes(Ns_8, 8))
    Ns_12 = np.asarray(sort_and_keep_indexes(Ns_12, 12))
    return Ns_4, Ns_8, Ns_12


def get_MIJ_matrices(Ns_list, filename):
    action_label = int(filename[1:3]) - 1

    with open('data/' + filename, 'r') as f:
        skeleton_matrix = [line.rstrip('\n') for line in f]
    for j in range(len(skeleton_matrix)):
        skeleton_matrix[j] = [float(coord) for coord in skeleton_matrix[j].split(' ')]

    skeleton_matrix = np.asarray(skeleton_matrix)
    noFrames = int(skeleton_matrix.shape[0] / setting.NUMBER_OF_JOINTS)
    x = skeleton_matrix[:, 0]
    y = skeleton_matrix[:, 1]
    z = skeleton_matrix[:, 2]

    x = x.reshape(setting.NUMBER_OF_JOINTS, int(skeleton_matrix.shape[0] / setting.NUMBER_OF_JOINTS))
    y = y.reshape(setting.NUMBER_OF_JOINTS, int(skeleton_matrix.shape[0] / setting.NUMBER_OF_JOINTS))
    z = z.reshape(setting.NUMBER_OF_JOINTS, int(skeleton_matrix.shape[0] / setting.NUMBER_OF_JOINTS))
    t = np.arange(1, noFrames + 1)
    x = x[Ns_list[action_label]]
    y = y[Ns_list[action_label]]
    z = z[Ns_list[action_label]]
    return x, y, z, t

# training...
def get_covariance_vector(x,y,z,t):
    fullCovmat, vec_covMat = calculateCovarianceMat(x.T, y.T, z.T, t, nLevels=2, overlap=True, timeVar=False)
    return vec_covMat

def make_preprocessed_training_data(filenames):
    X_train, y_train = [], []
    for i in range(len(filenames)):
        x, y, z, t = get_MIJ_matrices(filenames[i])
        vec_covMat = get_covariance_vector(x,y,z,t)
        label = int(filenames[i][1:3])
        X_train.append(vec_covMat)
        y_train.append(label)
    X_train = np.asarray(X_train)
    y_train = np.asarray(y_train)
    return X_train, y_train

