import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import cv2
from scipy.ndimage.filters import gaussian_filter
matplotlib.use('Agg')

def make_subtracted_mean(image_path, image_list):
    if os.path.isfile('filtered_mean.npy'):
        filtered_mean = np.load('filtered_mean.npy')
        return filtered_mean
    else:
        subtracted_means = []
        saved_depth_info = []
        first_frame = cv2.imread(os.path.join(image_path, image_list[0]))
        for i in range(1, len(image_list)):
            next_frame = cv2.imread(os.path.join(image_path, image_list[i]))
            subtracted_means.append(np.mean(next_frame - first_frame))
            saved_depth_info.append(next_frame)
        # print(len(subtracted_means))
        saved_depth_info = np.asarray(saved_depth_info)
        subtracted_means = np.asarray(subtracted_means)
        filtered_mean = gaussian_filter(subtracted_means, sigma=7)
        np.save('filtered_mean.npy', filtered_mean)
        # np.save('saved_depth_info.npy', saved_depth_info)
        # fig = plt.figure(figsize=(16,10))
        # plt.plot(filtered_mean)
        # fig.savefig('filtered_mean.jpg')
        return filtered_mean


def segment(filtered_mean):
    #end_frame = 2250
    min_at_segment = []
    frame_count = 30
    while frame_count < len(filtered_mean) - 250:
        min_frame = np.argmin(filtered_mean[frame_count:frame_count+250])
        min_at_segment.append(min_frame)

        frame_count += 250
    return min_at_segment


if __name__=="__main__":
    image_path = 'frame/'
    image_list = os.listdir(image_path)
    image_list = sorted(image_list)
    filtered_mean = make_subtracted_mean(image_path, image_list)
    min_at_segment = segment(filtered_mean)
    print(len(min_at_segment))