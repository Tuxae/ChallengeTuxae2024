# https://medium.com/@chand.shelvin/pybullet-getting-started-a068a0e3d492

import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)# p.DIRECT for non-graphical version

p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("r2d2.urdf",cubeStartPos, cubeStartOrientation)

print("Number of Joints: ", p.getNumJoints(boxId))

for i in range (10000):
   p.stepSimulation()
   time.sleep(1./240.)
   print("Step: ", i)
   
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)

p.disconnect()