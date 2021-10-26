# MAJOR WIP!!! Need to find a way to extend method to multiple drops of blood +
# non-elliptical blood stains - see: https://doi.org/10.1016/j.jofri.2014.09.004
# Returns parameters of detected ellipse (centre coords, major-axis length, 
# minor-axis length, rotation angle)

# packages
import cv2 as cv
import numpy as np
import argparse

# get input location
parser = argparse.ArgumentParser()
parser.add_argument("-im", "--image", required=True, help = "input image filepath (2D)")
args = vars(parser.parse_args())

# load image
print("Loading images...")
cap = cv.imread(args["image"])
aspRatio = cap.shape[0]/cap.shape[1]
dim = (600, 600/aspRatio)
cap - cv.resize(cap, dim)
(capH, capW) = cap.shape[:2]

# background subtraction
backSub = cv.createBackgroundSubtractorMOG2()
cap = backSub.apply(cap)

# image binarisation 
gray = cv.cvtColor(cap, cv.COLOR_BGR2GRAY)
gray = cv.blur(gray, (5,5))
ret, gray = cv.threshold(gray, 100, 255,cv.THRESH_BINARY)

# canny edge detection
edges = cv.Canny(gray, 350, 700)
contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# convex hull fitting
cont = np.vstack(contours)
uni_hull = []
hull = cv.convexHull(cont)
uni_hull.append(hull)
uni_hull = np.array(uni_hull) #list of all detected hulls

# ellipse parameters
if len(uni_hull[0]) > 5:
    ellipse = cv.fitEllipse(uni_hull[0])
    # ellipse is in the form ((x, y), (w,h),/theta)
    ((x, y), (w,h),theta) = ellipse
    vert_angle = np.arcsin(w/h)
    
    
# From here, a vector is defined with origin coordinates x,y (in the 2D blood plane), 
# in the direction with vert_angle and theta, which can be converted to 3D space using
# transformation matrix


