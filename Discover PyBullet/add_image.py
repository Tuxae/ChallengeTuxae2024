
import pybullet as p
import time
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from PIL import Image

p.connect(p.GUI)
offset = [0.225,0.225,0]

# turtle = p.loadURDF("test.urdf",offset)
turtle = p.loadURDF("turtlebot.urdf",offset)
# soccer = p.loadURDF("soccerball.urdf",offset)
# Set the path to the directory containing your .urdf and .obj files
# p.setAdditionalSearchPath("../Assets")
planeId = p.loadURDF("vinyle_table.urdf")
# plane = p.loadURDF("plane.urdf")
# p.setRealTimeSimulation(1)
p.setTimeStep(1./240.)

forward=1
turn=0.1
for i in range(500):
   p.setGravity(0,0,-10)
   time.sleep(1./240.)
   keys = p.getKeyboardEvents()
   leftWheelVelocity=0
   rightWheelVelocity=0
   speed=10
   p.stepSimulation()

   rightWheelVelocity+= (forward+turn)*speed
   leftWheelVelocity += (forward-turn)*speed
   if i%100==0:
      # Print the position and orientation of the turtle
      time.sleep(1)
      pos_ori = p.getBasePositionAndOrientation(turtle)
      euler = p.getEulerFromQuaternion(pos_ori[1])
      alpha = euler[2]
      print(pos_ori[0], euler)
      # Print the acceleration of the turtle
      # print(p.getBaseVelocity(turtle))
      # Move the camera
      x, y, z = pos_ori[0]
      distance = 0.5
      pitch = -pi/4
      x += distance * np.cos(alpha) * np.cos(pitch)
      y += distance * np.sin(alpha) * np.cos(pitch)
      # Resume simulation
      time.sleep(1)

      p.resetDebugVisualizerCamera(cameraDistance=distance, cameraYaw=alpha/pi*180-90, cameraPitch=pitch/pi*180, cameraTargetPosition=(x, y, z+0))
      # get the camera image
      time.sleep(1)
      width, height, rgbImg, depthImg, segImg = p.getCameraImage(1080,1080, renderer=p.ER_BULLET_HARDWARE_OPENGL)
      # show the camera image
      print(len(rgbImg))
      np_img = np.array(rgbImg, dtype=np.uint8).reshape(height, width, 4)[:, :, :3]
      # change dtype to uint8
      print(np_img.shape, np_img.dtype, np_img.min(), np_img.max())
      # show the camera image
      # save image using numpy
      img = Image.fromarray(np_img)
      img.save(f"camera_image_{i}.png")


      # plt.imshow(np_img)
      # savefig without borders
      # plt.savefig(f"camera_image_{i}.png", bbox_inches='tight', pad_inches=0)
      # plt.imshow(rgbImg)

   p.setJointMotorControl2(turtle,0,p.VELOCITY_CONTROL,targetVelocity=leftWheelVelocity)
   p.setJointMotorControl2(turtle,1,p.VELOCITY_CONTROL,targetVelocity=rightWheelVelocity)


p.disconnect()