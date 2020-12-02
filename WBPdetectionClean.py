import cv2
import matplotlib.pyplot as plt
import numpy as np
#the following are sensative to detection:
#scaling percent
#threshold amount
#erosion/dilate kernal size
#mins and max of ar filter and size filter

#get image  in greyscale
img = cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\201123_HDI_fiducial-20201128T195219Z-001\201123_HDI_fiducial\MH0111\fid_bl.png', 0)


#got image now resize
def resizedimg(image):
    scale_percent = 25  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)  # shape gets the size of it and its the second item then multiplies it by the percent
    height = int(image.shape[0] * scale_percent / 100)
    dims = (width, height)  # resize takes a tuple as a input so this puts it in a tuple
    resized = cv2.resize(image, dims, interpolation=cv2.INTER_AREA)
    tools = [resized, dims]
    #print(dims) (514,385)
    return tools
resized_img = resizedimg(img)[0]
#image resized now apply threshold, blur, erosion, dilate, and contours

def get_contours(image):
    ret, thresh = cv2.threshold(image,125,255, cv2.THRESH_OTSU)
    #threshold applied now erode and dilate by same amount to not hurt WBP
    blur = cv2.GaussianBlur(thresh, (7, 7), 0)  # reduces noise
    kernel = np.ones((3,3), np.uint8)
    #add multiple erosions and dilations
    img_erosion = cv2.erode(blur, kernel, iterations=2)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
    #dilation and erosion done, now for finding contours
    img_contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #cv2.RETR_TREE
    return img_contours
full_contours = get_contours(resized_img)
#got contours now apply filters
#print(full_contours[0]) #called cnts and used for moments and a million things looks absolutely meaningless though

dim = resizedimg(img)[1]
#sizeMin = 0.1
#sizeMax = .8
sizeMin = .05
sizeMax = .3

pixels = int(dim[0])*int(dim[1]) #total number of pixels
def sizeFilter(contour):
    return sizeMin < cv2.contourArea(contour)/pixels < sizeMax

#Second Filter is aspect ratio
#ar_min = .3
#ar_max = 2
ar_min = 0
ar_max = 100
def arFilter(contour):
    rect = cv2.minAreaRect(contour)
    ar = rect[1][0] / rect[1][1]  #width/height
    return ar_min < ar < ar_max
contours = filter(sizeFilter, full_contours)
contours = filter(arFilter, contours)
contours = list(contours)
#passes each countour to sizeFilter to check if it returns True or not
#it creates an iterator of the ones that return true

#if 0 means your constraint were too strong!
if len(contours) == 0:
    raise Exception("Could not isolate wire bond pads! {} shapes passed filters".format(len(contours)))

#time to draw rectangle over each WBP and get centers

#check if contour approximation works(last link)
#STEPS FOR DRAWING BORDER RECTANGLE
#make sure your contours are closed (no holes)
#   kernel = np.ones((3,3), dtype=np.uint8)
#   closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#   _, contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#Not sure what this does
cnt = max(contours, key=cv2.contourArea)
x,y,w,h = cv2.boundingRect(cnt)
#print(x, y, w, h)
cv2.rectangle(resized_img, (x,y), (x+w, y+h), (255,0,0), 1)
#   cnt = max(contours, key=cv2.contourArea)
#   https://www.programiz.com/python-programming/methods/built-in/max
#   https://stackoverflow.com/questions/55587820/how-to-get-the-only-min-area-rectangle-on-a-multiple-contours-image-with-cv2-min
#Get bounding rectangle which comes from the contours and found max with respect to a key=cv2.contourArea
#   x,y,w,h = cv2.boundingRect(cnt)
#Draw rectangle on desired picture
#   cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 1)
#Draw center from moments (look and see if you can use moments for contour area to clean up code
#   https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
#   also use this documentation to solve rotated rectangles


#makes a black image to draw contours on
mask = np.zeros_like(resized_img)
drawn = cv2.drawContours(mask, contours, -1, (255, 0, 0), 1)
cv2.imshow('2', resized_img)
cv2.imshow('wat', drawn)
cv2.waitKey(0)
