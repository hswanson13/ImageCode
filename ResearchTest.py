#mostly just notes in this file

import cv2
import matplotlib as plt
import numpy as np

#how to get a picture
img = cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\TFPX Heater GM0108 samples\sample_02.jpg', 0)
#second args are 1,0,-1 so 1 is color, 0 is grayscale, -1 unchanged loads image as such including alpah channel

#totally not ripped from the internet
scale_percent = 25 # percent of original size
width = int(img.shape[1] * scale_percent / 100)                 #shape gets the size of it and its the second item then multiplies it by the percent
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)                                           #resize takes a tuple as a input so this puts it in a tuple

resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)  #saw something about interpolation inter area not sure what it does

cv2.imshow('image', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()





