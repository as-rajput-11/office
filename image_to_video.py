import numpy as np
import cv2
import os
from natsort import natsorted 

width = 1280
hieght = 720
channel = 3

fps = 30
sec = 1

fourcc = cv2.VideoWriter_fourcc(*'MP42')

video = cv2.VideoWriter('image_to_video.avi', fourcc, float(fps), (width, hieght))

directry = r'/home/bisag/project work task_2023/large image split and overlap/image to video/Lorros'

img_name_list = os.listdir(directry)

for frame_count in range(1):
    img_name = img_name_list
    natsort_file_names = natsorted(img_name)
    listToStr = ' '.join([str(elem) for elem in natsort_file_names])
    a = listToStr.split(' ')
    for b in a :
        print(b)
        img_path = os.path.join(directry, b)
        print(img_path)
        img = cv2.imread(img_path)
        img_resize = cv2.resize(img, (width, hieght))
        video.write(img_resize)
