import glob
import os
import xml.etree.ElementTree as ET
import numpy as np
from os import getcwd

# dirs = ['train', 'val']
classes = []


def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def splitTrainVal(paths_file):
    full_dir_path = ''
    train_file = open(full_dir_path + 'train.txt', 'w')
    valid_file = open(full_dir_path + 'valid.txt', 'w')

    class_file = open(full_dir_path + 'classes.txt', 'w')

    file1 = open(paths_file, 'r')
    lines = np.array(file1.readlines())

    msk = np.random.rand(len(lines)) < 0.8
    training = lines[msk]
    validation = lines[~msk]

    for image_path in training:
        train_file.write(image_path)

    for image_path in validation:
        valid_file.write(image_path)

    for cls in classes:
        class_file.write(cls + "\n")

    train_file.close()
    valid_file.close()


# cwd = getcwd()
def convertToYolo():
    full_dir_path = ''
    output_path = full_dir_path

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image_paths = getImagesInDir(full_dir_path)
    out_file = open(full_dir_path + 'out.txt', 'w')
    class_file = open(full_dir_path + 'classes.txt', 'w')

    for image_path in image_paths:
        out_file.write(image_path + '\n')
        convert_annotation(full_dir_path, output_path, image_path)

    out_file.close()

    print("Finished processing: ")


if __name__ == '__main__':
    pathToFile = "data.txt"
    splitTrainVal(pathToFile)
