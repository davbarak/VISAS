import cv2
import numpy as np
import os

import pandas as pd
from scipy import signal
from PIL import Image, ImageDraw
import nibabel as nib

import subprocess

import csv
import pandas
import geopy.distance
import keyboard
import math
import time
#from matplotlib import pyplot as plt
import os

path, dirs, files = next(os.walk("/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/images/"))
file_count = len(files)
# print (file_count)
# Calculate the correlation using SURF & BFMatcher


# load all the images

all_images = []
titles = []

# max=len(point)

max = file_count
min = 0
pic_num = min

save_to_final = '/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/csv/distances_final.csv'
save_to = '/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/csv/distances2.csv'
org = '/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/csv/distances.csv'

for a in range(min, max):
    image = cv2.imread(
        "/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/images/result" + str(a) + ".png",
        cv2.IMREAD_GRAYSCALE)
    f = "frame_" + str(a)
    titles.append(f)
    #print(f)
    all_images.append(image)

    if pic_num < max:
        pic_num = pic_num + 1
print("finish reading")

correlations = []
# read 2 pic
# os.remove("satellite_1.csv")
for b in range(min, max):
    original = cv2.imread(
        "/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/images/result" + str(b) + ".png",
        cv2.IMREAD_GRAYSCALE)
    image_to_compare = cv2.imread(
        "/home/barak/Documents/university/thesis/tamir/barak-thesis-nodejs/public/images/result" + str(b) + ".png",
        cv2.IMREAD_GRAYSCALE)
    # original = cv2.imread("/home/barak/Documents/university/thesis/python/detect_how_similar_images_are/images/different-golden-gate-bridge.jpg")
    # image_to_compare = cv2.imread("/home/barak/Documents/university/thesis/python/detect_how_similar_images_are/images/duplicate.jpg")

    orb = cv2.xfeatures2d.SURF_create()
    kp_1, desc_1 = orb.detectAndCompute(original, None)
    kp_2, desc_2 = orb.detectAndCompute(image_to_compare, None)

    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
    matches = bf.match(desc_1, desc_2)

    if len(kp_1) <= len(kp_2):
        number_keypoints_original = len(kp_1)
    else:
        number_keypoints_original = len(kp_2)

    # cv2.imshow("correspondences", original)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    orb = cv2.xfeatures2d.SURF_create()
    kp_1, desc_1 = orb.detectAndCompute(original, None)

    for image_to_compare, title in zip(all_images, titles):

        # 2) Check for similarities between the 2 images

        kp_2, desc_2 = orb.detectAndCompute(image_to_compare, None)

        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)
        try:

            matches = bf.match(desc_1, desc_2)
            good_points = []
            for m in matches:
                if m.distance < 0.99:
                    good_points.append(m)

            #print("len of good points", len(good_points))

            number_keypoints = 0
            if len(kp_1) <= len(kp_2):
                number_keypoints = len(kp_1)
            else:
                number_keypoints = len(kp_2)
            percentage_similarity = (len(good_points) / number_keypoints_original) * 100
            print("now frame " + str(b) + " VS " + title + " Similarity: " + str(int(percentage_similarity)) + "%\n")
        except:
            percentage_similarity = 0
            print("now frame " + str(b) + " VS " + title + " Similarity: " + str(int(percentage_similarity)) + "%\n")

        # result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
        # cv2.imshow("result", cv2.resize(result, None, fx=0.8, fy=0.8))
        # cv2.waitKey(0)
        cv2.destroyAllWindows()

        # with open(save_to, mode='a') as csv_file:
        #     fieldnames = ['file_number', 'corelation']
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     writer.writerow({'file_number': title, 'corelation': percentage_similarity})
        correlations.append(percentage_similarity)

    # with open(save_to, mode='w') as csv_file:
    #     with open(org, mode='r') as org_csv:
    #         fieldnames = ['frame1', 'frame2', 'distance', 'correlation']
    #         reader = csv.reader(org_csv)
    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #
    #         for row in reader:
    #             writer.writerow({'frame1': row[0], 'frame2': row[1], 'distance': row[2], 'correlation': percentage_similarity})
    #             #print({'frame1': row['frame1'], 'frame2': row['frame2'], 'distance': row['distance'], 'correlation': percentage_similarity})

with open(org, 'r') as f:
    with open(save_to, 'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)


print(len(correlations))
with open(save_to, 'r') as csvinput:
    with open(save_to_final, 'w') as csvoutput:
        writer = csv.writer(csvoutput)
        i = 0
        for row in csv.reader(csvinput):

            if i < len(correlations):
                writer.writerow(row + [correlations[i]])
                i = i + 1

exit()
