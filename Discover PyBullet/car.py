
import pybullet as p
import time
p.connect(p.GUI)
offset = [0,0,0]


p.resetSimulation()

p.setGravity(0,0,-10)
useRealTimeSim = 0

p.setTimeStep(1./120.)
p.setRealTimeSimulation(useRealTimeSim) # either this

otherCar = p.loadURDF("f10_racecar/racecar_differential.urdf", [0,1,.3])
track = p.loadURDF("plane.urdf")