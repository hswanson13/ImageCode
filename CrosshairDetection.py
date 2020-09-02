import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

img = cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\TFPX Heater GM0108 - Crosshairs(gantrycam)\sample_02.png', 0)

scale_percent = 40
xpixel = int(img.shape[1] * scale_percent / 100) #xdirection
ypixel = int(img.shape[0] * scale_percent / 100)  #ydirection
dim = (xpixel, ypixel)
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

def getCircles(image):
    #blur makes detection harder but more precise
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    circle_info = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.4, 100)
    if circle_info is not None:
        #code only works if there is one circle
        #can be adapted if you need to find multiple circles
        x = int(circle_info[0][0][0])
        y = int(circle_info[0][0][1])
        r = int(circle_info[0][0][2])
        circle = cv2.circle(resized, (x,y), r, (255, 255, 255), 4)
        #cv2.rectangle(resized, (x-2,y-2), (x+2,y+2),255,1)
        info_list = [circle, x, y]
        return info_list
    else:
        error = "No circles found, loosen constraints."
        return error

drawn_circles = getCircles(resized)

#take info list to pass into here
def draw_error(image, xpixel, ypixel, x,y):
    error_bound = 10 # 10 micrometers
    #we got width/length of picture in pixels earlier
    x_fov = 2000 # 2mm or 2000 micrometers
    #or if FOV is area then np.sqrt(length_field)
    pixel_length = x_fov/xpixel #this tells you in x_fov there are this many xpixels
    r_error = error_bound / pixel_length #error / pixel length gets you the "radius of error"
    error_circle = cv2.circle(image, (x,y), int(r_error), 255, 1)
    return error_circle

fresh = draw_error(drawn_circles[0], xpixel, ypixel, drawn_circles[1], drawn_circles[2])

cv2.imshow('wat', fresh)
cv2.waitKey(0)


#need to calculate error circle
#going to draw a circle in acceptable area
#accurate within 10 micrometers
#2mm FOV