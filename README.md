# VirtualCam

Virtual camera is created **only using OpenCV and numpy**. It simulates a camera where **we can control** all its parameters **intrinsic and extrinsic** to get a better understanding how each component in the **camera projection matrix** affects the final image of the object captured by the camera.

An interractive GUI is also provided which simulates a virtual camera and a plane in 3D world. Basically the plane is a mesh of 3D points. We compute the camera projection matrix and thus the image coordinates corresponding to these 3D points. The projected points and the original mesh points are used to compute a map and finally a remapping function is applied on the image. 
