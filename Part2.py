import cv2
import matplotlib.pyplot as plt
import numpy as np
#the following are sensative to detection:
#scaling percent
#threshold amount
#erosion/dilate kernal size
#mins and max of ar filter and size filter

#get image  in greyscale
img = cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\TFPX Heater GM0108 samples\sample_02.jpg', 0)

#resizes image
seperateimg =cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\TFPX Heater GM0108 samples\sample_02.jpg', 0)
scale_percent = 25  # percent of original size
width = int(seperateimg.shape[1] * scale_percent / 100)  # shape gets the size of it and its the second item then multiplies it by the percent
height = int(seperateimg.shape[0] * scale_percent / 100)
dim = (width, height)  # resize takes a tuple as a input so this puts it in a tuple
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
#image resized now apply threshold

ret, thresh = cv2.threshold(resized,110,255, cv2.THRESH_BINARY)
#threshold applied now erode and dilate by same amount to not hurt WBP

kernel = np.ones((3,3), np.uint8)
img_erosion = cv2.erode(thresh, kernel, iterations=1)
img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
#dilation and erosion done, now for finding contours

contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #cv2.RETR_TREE
#contours found now filter area of contours to get in the range of our wirebond pads
#and filter by aspect ratio to get in the range of our wrirebond pads

#this might be too tight will have to test on other pictures
#min = .0012
#max = .0015
sizeMin = .0012
sizeMax = .0015 #tightest fit I could get min = .0012 and max = .0015
pixels = dim[0]*dim[1] #total number of pixels
def sizeFilter(contour):
    return sizeMin < cv2.contourArea(contour)/pixels < sizeMax
#Second Filter is aspect ratio
#min of .3 is perfect
#max of 2 is perfect
ar_min = .3
ar_max = 2
def arFilter(contour):
    rect = cv2.minAreaRect(contour)
    ar = rect[1][0] / rect[1][1]  #width/height
    return ar_min < ar < ar_max
contours = filter(sizeFilter, contours)
contours = filter(arFilter, contours)
contours = list(contours)
#passes each countour to sizeFilter to check if it returns True or not
#it creates an iterator of the ones that return true

#if 0 means your constraint were too strong!
if len(contours) == 0:
    raise Exception("Could not isolate wire bond pads! {} shapes passed filters".format(len(contours)))

#time to draw rectangle over each WBP and get centers





#makes a black image to draw contours on
mask = np.zeros_like(resized)
drawn = cv2.drawContours(mask, contours, -1, (255, 0, 0), 1)

cv2.imshow('wat', drawn)
cv2.waitKey(0)
