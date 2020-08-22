import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    # 7x7 gauss with a 50 too 150 canny works good
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

def display_lines(image, lines):
    line_image = np.zeros_like(image) #same as image but black
    if lines is not None: #checks if array isnt empty
        for line in lines: #each line is a 2D array with our coordinates x1,y1 etc...
            #we have 2D array like: [[x1,y1,x2,y2]]
            #this gets it to [x1,y1,x2,y2]
            x1, y1, x2, y2 = line.reshape(4)
            #this draws it onto our image
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0), 1) #last two are color and line thickness
    return line_image

def region_of_interest(image):
    #this will only keep a section of the image the rest will be blacked out

    rectangle = np.array([[(500,0),(565,0),(565,365),(500,365)]]) #this picks out four points to create a rectangle
    mask = np.zeros_like(image) #this makes everything black
    cv2.fillPoly(mask,rectangle,255) #this will take the black picture and put a white rectangle over the top (so binary is 11111111)
    #to just show that rectangle in the image we will use binary and operator, this does:
    #[1 0 1 1 1]
    #[0 1 1 1 0] the binary and operator spits out: [0 0 1 1 0] only if there is both ones it spits out ones
    #this is nice since the backround is black [0 0 0 0 0] whenever you apply the operator it will always turn zero
    #conversly if you have all ones it will alwasys put a 1 where it needs so it keeps the original picture
    #[1 1 1 1 1] & [1 0 1 1 0] -> [1 0 1 1 0] see, now using this to apply to our oringal picture
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

img = cv2.imread(r'C:\Users\hayde\OneDrive\Desktop\Research Code\TFPX Heater GM0108 samples\sample_02.jpg', 0) #greyscale for only 1 channel
img_copy = np.copy(img) #copies the numpy array of img, pixels range from 0 to a value of 255
canny = canny(img_copy)
cropped = region_of_interest(canny)
#in order to detect line we will use a Hough transfer (pho vs theta graph)
#dont super understand but get the idea
#the idea is for the computer to get a point.
#it then figures out all possible lines that could go through it in polar coordinates
#my problem is wouldnt a point only have one possible line to go throught it so how could u plot a bunch?
#it plots a bunch of these (makes a sin curve) and the line of best fit is the bin with the most intersections
lines = cv2.HoughLinesP(cropped, 2, np.pi/180, 15, np.array([]),minLineLength=10, maxLineGap=10) #100,40,10
#ONLY TWEAK: fourth,sixth,seventh inputs
#3 two is how specific you want the bins, its actually an array or something, dont understand at all
#I just think of it as if a bin is too small or big it wont be accurate as in too many intersects or just one
#the 100 is the bin count to be accepted as a line
#the minlinelength is any lines traced by less than 40 pixels are rejected
#maxlinegap is indicates the maximum distance in pixels between segmented lines which we will allow to be conntected into a single line
line_image = display_lines(canny, lines)
cv2.imshow('result',line_image)
cv2.waitKey(0)
