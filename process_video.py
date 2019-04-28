import numpy as np
import os
import cv2

video_name = 'color.avi'
cap = cv2.VideoCapture(video_name)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

segment_list = np.load('min_at_segment.npy')
frame_count = 0
segment_count = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('frame',gray)
    if ret and frame_count < segment_list[segment_count]:
        cv2.putText(frame, 'Action' + str(segment_count) + ' ' + str(frame_count), (50, 50), cv2.FONT_ITALIC, 0.8, 255)

    frame_count += 1
    if frame_count >= segment_list[segment_count] and segment_count < segment_list.shape[0]-1:
        segment_count += 1

    out.write(frame)

    cv2.imshow('frame', frame)
    cv2.waitKey(10)

    if 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()