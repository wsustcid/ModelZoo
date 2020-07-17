'''
@Author: Shuai Wang
@Github: https://github.com/wsustcid
@Version: 1.0.0
@Date: 1970-01-01 08:00:00
@LastEditTime: 2020-07-17 16:33:41
@Description:  
'''
#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : show_bboxes.py
#   Author      : YunYang1994
#   Created date: 2019-05-29 01:18:24
#   Description :
#
#================================================================

import cv2
import numpy as np
from PIL import Image

def show_image_boxes(label_file, ID=0):

    image_info = open(label_file).readlines()[ID].split()

    image_path = image_info[0]
    image = cv2.imread(image_path)
    for bbox in image_info[1:]:
        bbox = bbox.split(",")
        image = cv2.rectangle(image,(int(float(bbox[0])),
                                    int(float(bbox[1]))),
                                    (int(float(bbox[2])),
                                    int(float(bbox[3]))), (255,0,0), 2)

    image = Image.fromarray(np.uint8(image))
    image.show()

def show_video_boxes(label_file):
    image_infos = open(label_file).readlines()
    name = {'0': 'Car', '1': 'Van', '2': 'Truck'}
    for i in range(len(image_infos)):
        image_info = image_infos[i].split()
        image = cv2.imread(image_info[0])

        for bbox in image_info[1:]:
            bbox = bbox.split(',')
            image = cv2.rectangle(image, (int(float(bbox[0])),
                                          int(float(bbox[1]))),
                                         (int(float(bbox[2])),
                                          int(float(bbox[3]))), (255,0,0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            image = cv2.putText(image, name[bbox[4]], 
                                (int(float(bbox[0])),int(float(bbox[1]))),
                                font, .5, (255,255,255), 1, cv2.LINE_AA)
        cv2.imshow('video', image)
        k = cv2.waitKey(50) # return -1 if no inputs
        #print(k)
        if k == ord('q'):
            break
    
    cv2.destroyAllWindows()

        


if __name__ == '__main__':
    label_file = "./data/dataset/vkitti_test.txt"
    #show_image_boxes(label_file)
    show_video_boxes(label_file)