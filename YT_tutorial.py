import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    scale_percent = 25  #percent of original size
    width = int(image.shape[1] * scale_percent / 100)                 # shape gets the size of it and its the second item then multiplies it by the percent
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)                                             # resize takes a tuple as a input so this puts it in a tuple
    resized = cv2.resize(img_copy, dim,interpolation=cv2.INTER_AREA)  # saw something about interpolation inter area not sure what it does
    blur = cv2.GaussianBlur(resized, (7, 7), 0)  # reduces noise
    # next step is to blur the image using a gaussian Blue
    # pretty much goes over the numpy array and has a weighted average to apply to the image
    # does this with like a 5 by 5 square in this case and does the average
    # make more blurry by making the 5x5 bigger

    # cv2.Canny(image,low_threshold,high_threshold)
    # edge corresponds to a sharp change in the numpy array
    # [0 0 255 255]
    # the change in pixels across is the gradient
    # if you take the columns and rows of the matrix and apply it a x,y space
    # x=row y = column you can make a function f(x,y)
    # canny performs a derivitive of this function aka the grad f
    # this measures the change in intesnity, small grad no change big grad big change

    # Once it computes this it traces the edge with a large change in intensity
    # in a outline of white pixels
    # keeps anything between the low/high threshold
    # 1 to 2 or 1 to 3
    canny = cv2.Canny(blur, 50, 150)
    return canny


img = cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\TFPX Heater GM0108 samples\sample_02.jpg', 0) #greyscale for only 1 channel
img_copy = np.copy(img) #copies the numpy array of img, pixels range from 0 to a value of 255
canny = canny(img_copy)
plt.imshow(canny)
plt.show()
#7x7 gauss with a 50 too 150 canny works good

#for image 2 the x,y slice is:
# (500,0),(565,0),(500,365),(565,365)