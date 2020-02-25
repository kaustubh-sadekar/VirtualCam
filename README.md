# VirtualCam

Virtual camera is created **only using OpenCV and numpy**. It simulates a camera where **we can control** all its parameters **intrinsic and extrinsic** to get a better understanding how each component in the **camera projection matrix** affects the final image of the object captured by the camera. It can be used to understand concepts of image formation and to understand the intrinsic and extrinsic camera parameters. An interractive GUI is also provided which simulates a virtual camera and a plane in 3D world. By changing the extrinsic parameters of the camera (rotation and translation) you can simulate how the image being formed changes.

## Camera Translation
![Camera-Translation](xyz.gif)

When you control the X, Y, Z trackerbars you are basically controlling the position of camera in the 3D world. The plane remains fixed and thus we can observe shifting of the plane as we move the camera. You can also objserve the changes in the last column of the camera projection matrix being prined in the right terminal.


## Camera Rotation
![Camera-Rotation](rot.gif)

When you control the alpha, beta, gamma trackbars you are controlling the rotations of camera in 3D world. This gives turning effect to the image.

## Camera Distortion Coefficients
![Camera-Rotation](distCoeff.gif)

When you control the k and p trackbars you are controlling the distortion coefficients. The computations performed in numpy also take into account the equation for lens distortions for a pin hole camera.


Basically the plane is a mesh of 3D points. We compute the camera projection matrix and thus the image coordinates corresponding to these 3D points. The projected points and the original mesh points are used to compute a map and finally a remapping function is applied on the image.
