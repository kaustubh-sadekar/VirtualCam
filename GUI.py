import cv2
import numpy as np
import math
from vcam import vcam,meshGen

class myMirror(meshGen):

	def __init__(self,H,W):
		super(myMirror, self).__init__(H,W)

	def defineMirror(self):

		self.Z = self.X*0+1

	def getMirror(self):
		self.defineMirror()

		return self.getPlane()

def nothing(x):
    pass

WINDOW_NAME = "output"
cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME,700,700)
cv2.createTrackbar("X",WINDOW_NAME,500,1000,nothing)
cv2.createTrackbar("Y",WINDOW_NAME,500,1000,nothing)
cv2.createTrackbar("Z",WINDOW_NAME,0,1000,nothing)
cv2.createTrackbar("alpha",WINDOW_NAME,180,360,nothing)
cv2.createTrackbar("beta",WINDOW_NAME,180,360,nothing)
cv2.createTrackbar("gama",WINDOW_NAME,180,360,nothing)
cv2.createTrackbar("K1",WINDOW_NAME,0,100000,nothing)
cv2.createTrackbar("K2",WINDOW_NAME,0,100000,nothing)
cv2.createTrackbar("P1",WINDOW_NAME,0,100000,nothing)
cv2.createTrackbar("P2",WINDOW_NAME,0,100000,nothing)
cv2.createTrackbar("focus",WINDOW_NAME,600,1000,nothing)
cv2.createTrackbar("Sx",WINDOW_NAME,100,1000,nothing)
cv2.createTrackbar("Sy",WINDOW_NAME,100,1000,nothing)
# cap = cv2.VideoCapture(0)
# ret,img = cap.read()
img = cv2.imread("chess.png")
H,W = img.shape[:2]

c1 = vcam(H=H,W=W)
grid = myMirror(H,W)
src = grid.getMirror()

while True:
	# ret, img = cap.read()
	img = cv2.imread("chess.png")
	X = -cv2.getTrackbarPos("X",WINDOW_NAME) + 500
	Y = -cv2.getTrackbarPos("Y",WINDOW_NAME) + 500
	Z = -cv2.getTrackbarPos("Z",WINDOW_NAME)
	alpha = cv2.getTrackbarPos("alpha",WINDOW_NAME) - 180
	beta = cv2.getTrackbarPos("beta",WINDOW_NAME) - 180
	gamma = -cv2.getTrackbarPos("gama",WINDOW_NAME) - 180
	c1.focus = cv2.getTrackbarPos("focus",WINDOW_NAME) - 500
	c1.sx = (cv2.getTrackbarPos("Sx",WINDOW_NAME)+1)/100
	c1.sy = (cv2.getTrackbarPos("Sy",WINDOW_NAME)+1)/100
	k1 = cv2.getTrackbarPos("K1",WINDOW_NAME)/100000
	k2 = cv2.getTrackbarPos("K2",WINDOW_NAME)/100000
	p1 = cv2.getTrackbarPos("P1",WINDOW_NAME)/100000
	p2 = cv2.getTrackbarPos("P2",WINDOW_NAME)/100000
	c1.KpCoeff[0] = k1
	c1.KpCoeff[1] = k2
	c1.KpCoeff[2] = p1
	c1.KpCoeff[3] = p2

	c1.set_tvec(X,Y,Z)
	c1.set_rvec(alpha,beta,gamma)
	output = c1.applyMesh(img,src)
	M = c1.RT
	print("\n\n############## Camera Matrix ##################")
	print(M)
	cv2.imshow("output",output)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

