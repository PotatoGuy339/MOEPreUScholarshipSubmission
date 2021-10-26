# WIP!!! Needs Integrating + Testing
# This section transforms captured bloodstain images from 3D to 2D perspective
# using fiducial markers from Pantone AR repo.
# Returns a transformation matrix describing the fiducial marker (which is to
# be placed on the same surface as the blood)

# packages
import cv2 as cv 
import numpy as np
import argparse
import sys



# get input location
parser = argparse.ArgumentParser()
parser.add_argument("-im", "--image", required=True, help = "input image filepath (3D")
args = vars(parser.parse_args())

# load image
print("Loading images...")
cap = cv.imread(args["image"])
aspRatio = cap.shape[0]/cap.shape[1]
dim = (600, 600/aspRatio)
cap - cv.resize(cap, dim)
(capH, capW) = cap.shape[:2]

# load ArUCo, exit if markers not found
print("Detecting markers...")
ARdict = cv.aruco.Dictionary_get(cv.aruco.DICT_ARUCO_ORIGINAL)
ARparams = cv.aruco.DetectorParameters_create()
(corners, ids, rej) = cv.aruco.detectMarkers(cap, ARdict, parameters=ARparams)

if len(corners) != 4:
	print("[ERROR] Could not find 4 corners...exiting now")
	sys.exit(0)
    
# create list of reference points from fiducial marker
print("fetching reference points...")
ids = ids.flatten()
ref = []

for i in (923, 1001, 241, 1007): 
    # search for coreners and append coords to refPts list
	j = np.squeeze(np.where(ids == i))
	corner = np.squeeze(corners[j])
	ref.append(corner)
    
# define transformation matrix
(refTL, refTR, refBR, refBL) = ref
dstMat = [refTL[0], refTR[1], refBR[2], refBL[3]]
dstMat = np.array(dstMat)