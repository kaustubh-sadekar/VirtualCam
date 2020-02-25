import cv2
import numpy as np
import math
from numpy import newaxis
import math
import sys
from tkinter import *
import glob
from cam import cam

# Example use of the class
img = cv2.imread("pano2.jpg")
dst_img = img*0

H = img.shape[0]
W = img.shape[1]

root = Tk()
root.title("SImple GUI")
root.geometry("600x300")

c1v = DoubleVar()
c2v = DoubleVar()
c3v = DoubleVar()
c4v = DoubleVar()
c5v = DoubleVar()
c6v = DoubleVar()
c7v = DoubleVar()
c8v = DoubleVar()

hslid = Scale(root,from_=-1000,to=1000,orient=HORIZONTAL,length=500,resolution = 1,variable=c1v)
hslid.pack()
sslid2 = Scale(root,from_=-1000,to=1000,orient=HORIZONTAL,length=500,resolution = 1,variable=c2v)
sslid2.pack()
sslid2 = Scale(root,from_=-1000,to=1000,orient=HORIZONTAL,length=500,resolution = 0.00001,variable=c3v)
sslid2.pack()
vslid = Scale(root,from_=-np.pi,to=np.pi,orient=HORIZONTAL,length=500,resolution = 0.000001,variable=c4v)
vslid.pack()
sslid = Scale(root,from_=-np.pi,to=np.pi,orient=HORIZONTAL,length=500,resolution = 0.000001,variable=c5v)
sslid.pack()
sslid2 = Scale(root,from_=-np.pi,to=np.pi,orient=HORIZONTAL,length=500,resolution = 0.000001,variable=c6v)
sslid2.pack()
sslid = Scale(root,from_=-100,to=100,orient=HORIZONTAL,length=500,resolution = 0.001,variable=c7v)
sslid.pack()
sslid2 = Scale(root,from_=-100,to=100,orient=HORIZONTAL,length=500,resolution = 0.001,variable=c8v)
sslid2.pack()

c1 = cam(H,W)

while(True):
    dst_img = dst_img*0
    root.update_idletasks()
    root.update()
    
    alpha = -math.radians((c4v.get()))
    beta = -math.radians((c5v.get()))
    gamma = -math.radians((c6v.get()))
    
    Tx = int(c1v.get())
    Ty = int(c2v.get())
    Tz = -int(c3v.get())

    c1.set_rvec(alpha,beta,gamma)
    c1.set_tvec(Tx,Ty,Tz)

    dst_img = c1.render(img)
    cv2.imshow("output",dst_img)

    k = cv2.waitKey(100)
    if k == 27:
        break
