# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 06:52:00 2020

@author: CVPR
"""

# Make Json


# import
from collections import OrderedDict

import cv2
import glob
import json
import base64


# get img, label list
image_list = glob.glob(r".\attack\*.png")
label_list = glob.glob(r".\attack\*.txt")


# get image data
def get_image_data(img_path):
    img_info = cv2.imread(img_path)

    imagePath   = img_path
    img_data    = base64.b64encode(open(img_path, "rb").read())
    imageHeight = img_info.shape[0]
    imageWidth  = img_info.shape[1]

    return [imagePath, img_data, imageHeight, imageWidth]


#x1, y1, x2, y1, x1, y2, x2, y2
# get label data
def get_label_data(label_path, group_id, shape_type):
    label_list = []

    with open(label_path, 'r') as MyFile:
        MyString  = MyFile.read()
        sentences = MyString.rstrip().split("\n")

        for sentence in sentences:
            label_list.append(sentence.split(", ") + [group_id, shape_type])
  
    return label_list


# pointsList
def point_list(label_data):
    point_list = []
    
    point_list.append([float(label_data[1]), float(label_data[2])])
    point_list.append([float(label_data[3]), float(label_data[4])])
    point_list.append([float(label_data[7]), float(label_data[8])])
    point_list.append([float(label_data[5]), float(label_data[6])])

    return point_list


# shapesDict
def shapes_list(label_data):
    shape_list = []

    for i in label_data:
        shapes = OrderedDict()

        shapes["label"]      = i[-3]
        shapes["points"]     = point_list(i)
        shapes["group_id"]   = i[-2]
        shapes["shape_type"] = i[-1]
        shapes["flags"]      = {}

        shape_list.append(shapes)

    return shape_list


# data 2 Json
def data2Json(img_data, label_data):
    file_data = OrderedDict()

    file_data["version"]     = "4.5.6"
    file_data["flags"]       = {}
    file_data["shapes"]      = shapes_list(label_data)
    file_data["imagePath"]   = img_data[0].split("/")[-1]
    file_data["imageData"]   = str(img_data[1]).lstrip("b'")
    file_data["imageHeight"] = img_data[2]
    file_data["imageWidth"]  = img_data[3]

    return file_data


group_id   = None
shape_type = "polygon"


# main
for i in range(len(image_list)):
    img_data   = get_image_data(image_list[i])
    label_data = get_label_data(label_list[i], group_id, shape_type)
    result     = data2Json(img_data, label_data)

    if i % 10 == 0:
        with open('./valid_result_json/{}.json'.format(image_list[i].split("\\")[-1].strip(".png")), 'w', encoding="utf-8") as jsonfile:
            json.dump(result, jsonfile, ensure_ascii=False, indent="\t")

    else:
        with open('./result_json/{}.json'.format(image_list[i].split("\\")[-1].strip(".png")), 'w', encoding="utf-8") as jsonfile:
            json.dump(result, jsonfile, ensure_ascii=False, indent="\t")