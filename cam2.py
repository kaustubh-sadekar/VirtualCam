import cv2
import numpy as np
import math


class cam:

	def __init__(self,H,W):
		"""
		H : Desired height of the frame of output video
		W : Desired width of the frame of output
		"""
		self.H = H
		self.W = W
		self.ox = W//2
		self.oy = H//2
		self.alpha = math.radians(0)
		self.beta =  math.radians(0)
		self.gamma = math.radians(0)
		self.Tx = 0
		self.Ty = 0
		self.Tz = 0
		self.K = 0
		self.R = 0
		self.sh = 0 # Shere factor
		self.P = 0

		self.focus = 100 # Focal length of camera in mm
		self.sx = 1 # Effective size of a pixel in mm
		self.sy = 1 # Effective size of a pixel in mm

		self.update_M()

	def update_M(self):
		# Matrix for converting the 2D matrix to 3D matrix
		Rx = np.array([[1, 0, 0], [0, math.cos(self.alpha), -math.sin(self.alpha)], [0, math.sin(self.alpha), math.cos(self.alpha)]])
		Ry = np.array([[math.cos(self.beta), 0, -math.sin(self.beta)], [0, 1, 0], [math.sin(self.beta), 0, math.cos(self.beta)]])
		Rz = np.array([[math.cos(self.gamma), -math.sin(self.gamma), 0], [math.sin(self.gamma), math.cos(self.gamma), 0], [0, 0, 1]])
		self.R = np.matmul(Rx, np.matmul(Ry, Rz))
		self.K = np.array([[-self.focus/self.sx,self.sh,self.ox],[0,self.focus/self.sy,self.oy],[0,0,1]])
		self.M1 = np.array([[1,0,0,-self.Tx],[0,1,0,-self.Ty],[0,0,1,-self.Tz]])

		self.P = np.matmul(np.matmul(self.K,self.R),self.M1)

	def project(self,src):
		pts2d = np.matmul(self.P,src) # A 3X1 matrix
		
		try:
			x = pts2d[0,:]*1.0/(pts2d[2,:]+0.0000000001)
			y = pts2d[1,:]*1.0/(pts2d[2,:]+0.0000000001)
		except:
			print("Division by zero!")
			x = pts2d[0,:]*0
			y = pts2d[1,:]*0

		return np.concatenate(([x],[y]))

	def set_tvec(self,x,y,z):
		self.Tx = x
		self.Ty = y
		self.Tz = z
		self.update_M()

	def set_rvec(self,alpha,beta,gamma):
		self.alpha = alpha
		self.beta = beta
		self.gamma = gamma
		self.update_M()

	def render(self,src):
		pts = self.project(src)
		canvas = np.zeros((self.H,self.W,3),dtype=np.uint8)
		pts = (pts.T).reshape(-1,1,2).astype(np.int32)
		cv2.drawContours(canvas,pts,-1,(0,255,0),3)
		cv2.imshow("output",canvas)
		cv2.waitKey(0)




H = 400
W = 400
c1 = cam(H,W)
c1.set_tvec(0,0,100)
# src = np.array([[0,0,0,1],[-10,10,-10,1],[10,10,-10,1],[10,-10,-10,1],[-10,-10,-10,1]]).T

N = 100
x = np.linspace(-N/2,N/2,N).T
y = np.linspace(-N/2,N/2,N).T
z = np.linspace(-N/2,N/2,N).T
z1 = np.ones(N).T*1
src = np.concatenate(([x],[y],[z1],[z1]))
xv, yv = np.meshgrid(x, y)
src = np.concatenate(([xv.reshape(-1,1)],[yv.reshape(-1,1)],[yv.reshape(-1,1)*0+1],[yv.reshape(-1,1)*0+1]))[:,:,0]
# print(X.shape)


# c1.render(src)
for i in range(0,100):
	c1.set_tvec(0,0,i+1)
	c1.set_rvec(i/100,0,0)
	c1.render(src)

for i in range(100,1,-1):
	c1.set_tvec(0,0,i+1)
	c1.set_rvec(i/100,0,0)
	c1.render(src)