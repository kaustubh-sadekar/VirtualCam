import cv2
import numpy as np
import math


class vcam:

	def __init__(self,H=400,W=400):
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
		self.update_M()
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

	def renderMesh(self,src):
		"""
		Renders the mesh grid points to get better visual understanding
		"""
		self.update_M()
		pts = self.project(src)
		canvas = np.zeros((self.H,self.W,3),dtype=np.uint8)
		pts = (pts.T).reshape(-1,1,2).astype(np.int32)
		cv2.drawContours(canvas,pts,-1,(0,255,0),3)
		return canvas

	def applyMesh(self,img,meshPts):
		pts1,pts2 = np.split(self.project(meshPts),2)
		x = pts1.reshape(self.H,self.W)
		y = pts2.reshape(self.H,self.W)
		return cv2.remap(img,x.astype(np.float32),y.astype(np.float32),interpolation=cv2.INTER_LINEAR)


class meshGen:

	def __init__(self,H,W):

		self.H = H
		self.W = W


	def getSimpleMesh(self):

		x = np.linspace(-self.W/2, self.W/2, self.W)
		y = np.linspace(-self.H/2, self.H/2, self.H)

		xv,yv = np.meshgrid(x,y)

		X = xv.reshape(-1,1)
		Y = yv.reshape(-1,1)
		Z = X*0+1 # The mesh will be located on Z = 1 plane

		return np.concatenate(([X],[Y],[Z],[X*0+1]))[:,:,0]

	def getConvexMesh(self,epsilon):

		x = np.linspace(-self.W/2, self.W/2, self.W)
		y = np.linspace(-self.H/2, self.H/2, self.H)

		xv,yv = np.meshgrid(x,y)

		X = xv.reshape(-1,1)
		Y = yv.reshape(-1,1)
		Z = -np.sqrt((self.W*epsilon)**2 - X**2 - Y**2)

		return np.concatenate(([X],[Y],[Z],[X*0+1]))[:,:,0]
