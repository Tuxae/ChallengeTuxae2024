
import pybullet as p
import time
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from PIL import Image

p.connect(p.GUI)
offset = [0.225,0.225,0.05]

turtle = p.loadURDF("test.urdf",offset)
planeId = p.loadURDF("vinyle_table.urdf")


p.setGravity(0,0,-10)
p.stepSimulation()
p.resetDebugVisualizerCamera(
                cameraDistance=1, 
                cameraYaw=135, 
                cameraPitch=-45, 
                cameraTargetPosition=(2.5, 1.5, 0)
            )
time.sleep(1)
width, height, rgbImg, depthImg, segImg = p.getCameraImage(1080,1080, renderer=p.ER_BULLET_HARDWARE_OPENGL)
np_img = np.array(rgbImg, dtype=np.uint8).reshape(height, width, 4)[:, :, :3]

img = Image.fromarray(np_img)
img.save(f"image_depart.png")



p.disconnect()