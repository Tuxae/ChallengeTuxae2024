
import pybullet as p
import time
p.connect(p.GUI)
offset = [0,0,0]

# turtle = p.loadURDF("test.urdf",offset)
turtle = p.loadURDF("turtlebot.urdf",offset)
# soccer = p.loadURDF("soccerball.urdf",offset)
# Set the path to the directory containing your .urdf and .obj files
# p.setAdditionalSearchPath("../Assets")
planeId = p.loadURDF("vinyle_table.urdf")
# plane = p.loadURDF("plane.urdf")
p.setRealTimeSimulation(1)

forward=1
turn=0
for i in range(1000):
   p.setGravity(0,0,-10)
   time.sleep(1./240.)
   keys = p.getKeyboardEvents()
   leftWheelVelocity=0
   rightWheelVelocity=0
   speed=10

   rightWheelVelocity+= (forward+turn)*speed
   leftWheelVelocity += (forward-turn)*speed

   p.setJointMotorControl2(turtle,0,p.VELOCITY_CONTROL,targetVelocity=leftWheelVelocity,force=1000)
   p.setJointMotorControl2(turtle,1,p.VELOCITY_CONTROL,targetVelocity=rightWheelVelocity,force=1000)


p.disconnect()