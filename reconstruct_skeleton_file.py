import os

skeleton_path_file = 'skeleton-reality-data/'

list_skeleton_file = os.listdir(skeleton_path_file)

def make_re_skeleton():
    for i in range(len(list_skeleton_file)):
        fn = open(os.path.join(skeleton_path_file, list_skeleton_file[i]), 'r')
        r_fn = open(os.path.join(skeleton_path_file, 're_' + list_skeleton_file[i]), 'w')
        cont = fn.readlines()
        for j in range(len(cont)):
            if (j % 2 != 0):
                r_fn.write(cont[j])
        r_fn.close()
        fn.close()


if __name__=="__main__":
    fn = open(os.path.join(skeleton_path_file, "skeleton_raw_3.txt"), 'r')
    r_fn = open(os.path.join(skeleton_path_file, 're_' + "skeleton_raw_3.txt"), 'w')
    cont = fn.readlines()
    for j in range(len(cont)):
        if (j % 2 != 0):
            r_fn.write(cont[j])
    r_fn.close()
    fn.close()