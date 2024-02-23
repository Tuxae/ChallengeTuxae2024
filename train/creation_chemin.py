
import pybullet as p
import time, os
import numpy as np
from math import pi
from PIL import Image
import pandas as pd

# Paramètres de la simulation
FOLDER = "train"

# Paramètres de la caméra
hauteur = 0.15
pitch = -pi/5
distance = hauteur / np.sin(-pitch)
adjacent = distance / np.tan(-pitch)

def create_data(instructions, filename):
    # Chargement des objets (toutes les valeurs sont en mètres et radians)
    p.connect(p.GUI)
    offset = [0.225,0.225,0.05] 
    robot_tuxae = p.loadURDF("robot_tuxae.urdf",offset)
    planeId = p.loadURDF("vinyle_table.urdf")

    # Paramètres de la simulation
    p.setTimeStep(0.01) # Chaque step de simulation dure 0.01 secondes
    p.setGravity(0,0,-10)

    n = len(instructions)
    if os.path.exists(f"{FOLDER}/" + filename):
        input(f"Attention, le fichier {filename} existe déjà.")
    else:
        os.makedirs(f"{FOLDER}/{filename}", exist_ok=True)
    
    df = pd.DataFrame(columns=["vx", "vy", "vrz", "rot_g", "rot_d", "image", "x", "y", "alpha"])
    for i in range(n):
        vit_rot_g, vit_rot_d = instructions[i]
        p.stepSimulation()

        if i%100==0: # On prend une photo toutes les 100 steps (toutes les secondes)
            seconde = i//100
            # Les vitesses du robot
            (vx, vy, _), (_, _, vrz) = p.getBaseVelocity(robot_tuxae) 

            # Les positions absolues de rotation des roues
            rot_g = p.getJointState(robot_tuxae, 0)[0]
            rot_d = p.getJointState(robot_tuxae, 1)[0]

            # La position et l'angle du robot
            pos_ori = p.getBasePositionAndOrientation(robot_tuxae)
            x, y, z = pos_ori[0] # La position du robot
            euler = p.getEulerFromQuaternion(pos_ori[1])
            alpha = euler[2] # L'angle du robot
            
            # On enregistre les données
            image = f"{str(seconde).zfill(3)}.png"
            df.loc[seconde] = [vx, vy, vrz, rot_g, rot_d, image, x, y, alpha]

            p.resetDebugVisualizerCamera(
                cameraDistance=distance, 
                cameraYaw=alpha/pi*180-90, 
                cameraPitch=pitch/pi*180, 
                cameraTargetPosition=(x + adjacent * np.cos(alpha), y + adjacent * np.sin(alpha), 0)
            )
            # get the camera image
            time.sleep(1)
            width, height, rgbImg, _, _ = p.getCameraImage(1080,1080, renderer=p.ER_BULLET_HARDWARE_OPENGL)
            # save the camera image
            np_img = np.array(rgbImg, dtype=np.uint8).reshape(height, width, 4)[:, :, :3]
            img = Image.fromarray(np_img)
            img.save(f"{FOLDER}/{filename}/{image}")

        p.setJointMotorControl2(robot_tuxae,0,p.VELOCITY_CONTROL,targetVelocity=vit_rot_g)
        p.setJointMotorControl2(robot_tuxae,1,p.VELOCITY_CONTROL,targetVelocity=-vit_rot_d)
    df.to_csv(f"{FOLDER}/{filename}.csv")
    p.disconnect()

create_data(
    instructions=[(pi, pi)]*1000,
    filename="ligne_droite"
)