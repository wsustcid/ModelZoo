'''
@Author: Shuai Wang
@Github: https://github.com/wsustcid
@Version: 1.0.0
@Date: 2020-07-17 09:31:02
@LastEditTime: 2020-07-17 16:31:15
@Description:  Create annotations form the raw vkitti dataset 
'''

## The original data structure of vkitti_2.0.3 is:
'''
VKITTI/
├── vkitti_2.0.3_rgb
│   ├── Scene01
│   │   ├── 15-deg-left
│   │   │   └── frames
│   │   │       └── rgb
│   │   │           ├── Camera_0
│   │   │           └── Camera_1
│   │   ├── 15-deg-right
│   │   ├── 30-deg-left
│   │   ├── 30-deg-right
│   │   ├── clone
│   │   ├── fog
│   │   ├── morning
│   │   ├── overcast
│   │   ├── rain
│   │   └── sunset
│   ├── Scene02
│   ├── Scene06
│   ├── Scene18
│   └── Scene20  (as test)
├── vkitti_2.0.3_textgt
│   ├── Scene01
│   │   ├── 15-deg-left
│   │   │   ├── bbox.txt
│   │   │   ├── colors.txt
│   │   │   ├── extrinsic.txt
│   │   │   ├── info.txt
│   │   │   ├── intrinsic.txt
│   │   │   └── pose.txt
│   │   ├── 15-deg-right
│   │   ├── 30-deg-left
│   │   ├── 30-deg-right
│   │   ├── clone
│   │   ├── fog
│   │   ├── morning
│   │   ├── overcast
│   │   ├── rain
│   │   └── sunset
│   ├── Scene02
│   ├── Scene06
│   ├── Scene18
│   └── Scene20
└── 
'''

import os
import argparse
from glob import glob

def collect_classes(data_root):
    """ Collect all the class names in vkitti

    results: 'Car', 'Van', 'Truck'
    """

    info_paths = glob(os.path.join(data_root, 'vkitti_2.0.3_textgt/*/clone/info.txt'))
    classes = []
    for info_path in info_paths:
        print('Collecting from {}'.format(info_path))
        with open(info_path, 'r') as f:
            lines = f.readlines() # trackID label model color
            print("num of trackID: ", len(lines))
            for line in lines[1:]:
                name = line.split(' ')[1]
                if name not in classes:
                    classes.append(name)
   
    print("All labeled classes: ", classes)



def create_vkitti_annotation(data_dir, gt_dir, anno_path):
    """
    bbox.txt:
    frame cameraID trackID left right top bottom number_pixels truncation_ratio occupancy_ratio isMoving
    0 0 0 774 1241 169 374 75554 0.07726043 0.7891994 False
    """
    
    img_dir = os.path.join(data_dir, 'frames/rgb/Camera_0')
    bbox_path = os.path.join(gt_dir, 'bbox.txt')
    info_path = os.path.join(gt_dir, 'info.txt')
    
    print("==> Create annotations for images in: ", img_dir)
    # create a dict saves trackID and corresponding label
    label_dict = {}
    with open(info_path, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            track_id = line.split(' ')[0]
            label = line.split(' ')[1]
            label_dict[track_id] = label
    print("Num of tracking objects: {}".format(len(label_dict)))
    
    class_id = {'Car': 0, 'Van': 1, 'Truck': 2}
    
    anno_f = open(anno_path, 'a')
    with open(bbox_path, 'r') as f:
        lines = f.readlines()
        last_frame_id = None
        annotation = None
        count = 1
        for line in lines[1:]:
            frame_id = line.split(' ')[0]
            camera_id = line.split(' ')[1]
            track_id = line.split(' ')[2]
            bbox = line.split(' ')[3:7]
            
            if camera_id == '0':
                if frame_id != last_frame_id:
                    if annotation is not None:
                        # save last 
                        anno_f.write(annotation+'\n')
                        count +=1
                    # update 
                    img_path = os.path.join(img_dir, 'rgb_'+frame_id.zfill(5)+'.jpg')
                    annotation = img_path + ' ' + bbox[0] + ',' + bbox[2] + ',' + bbox[1] + ',' + bbox[3] + ',' +  str(class_id[label_dict[track_id]])
                else:
                    annotation += ' ' + bbox[0] + ',' + bbox[2] + ',' + bbox[1] + ',' + bbox[3] + ',' +  str(class_id[label_dict[track_id]])    
                
                last_frame_id = frame_id
        # save the final annotation
        anno_f.write(annotation+'\n')
        anno_f.close()    

    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_root", default="/media/ubuntu16/Documents/Datasets/VKITTI")
    parser.add_argument("--train_annotation", default="./data/dataset/vkitti_train.txt")
    parser.add_argument("--test_annotation",  default="./data/dataset/vkitti_test.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation): os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation): os.remove(flags.test_annotation)

    ## collect all class names
    #collect_classes(flags.data_root)
    
    data_path_1 = os.path.join(flags.data_root, 'vkitti_2.0.3_rgb/Scene01/clone')
    gt_path_1 = os.path.join(flags.data_root, 'vkitti_2.0.3_textgt/Scene01/clone')

    data_path_2 = os.path.join(flags.data_root, 'vkitti_2.0.3_rgb/Scene02/clone')
    gt_path_2 = os.path.join(flags.data_root, 'vkitti_2.0.3_textgt/Scene02/clone')

    data_path_3 = os.path.join(flags.data_root, 'vkitti_2.0.3_rgb/Scene06/clone')
    gt_path_3 = os.path.join(flags.data_root, 'vkitti_2.0.3_textgt/Scene06/clone')

    data_path_4 = os.path.join(flags.data_root, 'vkitti_2.0.3_rgb/Scene18/clone')
    gt_path_4 = os.path.join(flags.data_root, 'vkitti_2.0.3_textgt/Scene18/clone')

    data_path_5 = os.path.join(flags.data_root, 'vkitti_2.0.3_rgb/Scene20/clone')
    gt_path_5 = os.path.join(flags.data_root, 'vkitti_2.0.3_textgt/Scene20/clone')

    num1 = create_vkitti_annotation(data_path_1, gt_path_1, flags.train_annotation)
    num2 = create_vkitti_annotation(data_path_2, gt_path_2, flags.train_annotation)
    num3 = create_vkitti_annotation(data_path_3, gt_path_3, flags.train_annotation)
    num4 = create_vkitti_annotation(data_path_4, gt_path_4, flags.train_annotation)
    num5 = create_vkitti_annotation(data_path_5, gt_path_5, flags.test_annotation)
    
    print('The number of image for train is: %d\tThe number of image for test is:%d <==' %(num1+num2+num3+num4, num5))


