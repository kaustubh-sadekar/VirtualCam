import cv2
import numpy as np
import math
from vcam import vcam,meshGen

cap = cv2.VideoCapture(0)
ret,img = cap.read()

H,W = img.shape[:2]

c1 = vcam(H=H,W=W)
grid = meshGen(H,W)
src = grid.getConvexMesh(0.3)
c1.set_tvec(0,0,1)

while True:
	ret, img = cap.read()
	output = c1.applyMesh(img,src)
	cv2.imshow("output",output)
	cv2.waitKey(1)

