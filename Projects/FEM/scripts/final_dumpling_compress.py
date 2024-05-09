import shutil
import sys
import hashlib
import numpy as np
sys.path.insert(0, "../../../Python")
sys.path.insert(0, "../../../build")
import Drivers
from JGSL import *


joint1 = []
joint2 = []
joint3 = []
joint4 = []
joint5 = []

arrays = {1: joint1, 2: joint2, 3: joint3, 4: joint4, 5: joint5}

def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        contents = f.read()
    return hashlib.md5(contents).hexdigest()

def calculate_rotate(rotation):
    rotate = []
    rotxis = np.cross(np.array([0,0,1]),rotation)
    rotxis = rotxis / np.linalg.norm(rotxis)
    rotate.append(rotxis)
    rotDeg = np.arccos(np.dot(np.array([0,0,1]),rotation)) *180
    rotate.append(rotDeg)
    return rotate

# currunt_content = ''
is_model = False
is_rotate = False
is_rotDeg = False
model_pos = Vector3d(0,0,0)
rotation = Vector3d(0,0,0)
rotDeg = 0.0
rotate = []
fingercount = 0
original = []

# print(currunt_content == '')

def subtract(self, other):
    return self-other


if __name__ == "__main__":
    sim = Drivers.FEMSimulationBase("double", 3, "NH")


    E = 10000
    yield_stress = 1000


    with open("../../../../../hand.txt", 'r') as file:
        lines = file.readlines()

    # if currunt_content != lines:
    #     print("file changes!\n")

    for line in lines:
        if "Joint" in line:
            lsplit = line.split()
            fingercount = int(lsplit[1])
            continue
        if "rotation" in line:
            is_rotate = True
            continue
        if is_rotate:
            coordinate = eval(line)
            lst = list(coordinate)
            lst[1] = -lst[1]
            lst[0] = -lst[0]
            lst[2] = -lst[2]
            # lst[1], lst[2] = lst[2], lst[1]
            coordinate = tuple(lst)
            rotation = Vector3d(*coordinate)
            # rotation = rotation / np.linalg.norm(rotation)
            is_rotate = False
            print(is_rotate)
            continue
        if "rotdeg" in line:
            is_rotDeg = True
            continue
        if is_rotDeg:
            rotDeg = float(line)-180
            is_rotDeg = False
            continue
        if "Model" in line:
            is_model = True
            continue
        if is_model:
            coordinate = eval(line)
            lst = list(coordinate)
            lst[2] = -lst[2]
            #lst[1], lst[2] = lst[2], lst[1]
            coordinate = tuple(lst)
            model_pos = Vector3d(*coordinate)
            is_model = False
            continue
        try:
            coordinate = eval(line)
            lst = list(coordinate)
            #lst.reverse()
            lst[2] = -lst[2]
            #lst[1],lst[2] = lst[2],lst[1]
            coordinate = tuple(lst)
            position = Vector3d(*coordinate)
            arrays[fingercount].append(position)
        except SyntaxError:
            pass

    print('Joint 1 Trajectory:', joint1)
    print('Joint 2 Trajectory:', joint2)

    #original position
    print('original position set!\n')
    #currunt_content = lines

#/////////
    sim.set_nearDistance(3, model_pos)

    for i in range(fingercount):
        original.append(arrays[i + 1][0])
        sim.set_ori_hand(arrays[i + 1][0])

    for i in range(fingercount):
       sim.add_object("../input/sphere1K.vtk",original[i],
           Vector3d(0, 0, 0), Vector3d(0, 0, 0), 0, Vector3d(0.12, 0.12, 0.12))

    print('original:', original)
    time_step = len(arrays[1])
    for i in range(fingercount):
        for j in range(len(arrays[i + 1]) - 1):
            for k in range(25):
                sim.set_DBC(Vector3d(-0.06, -0.06, -0.06) + original[i], Vector3d(0.05, 0.05, 0.05) + original[i],
                        subtract(arrays[i + 1][j + 1], arrays[i + 1][j]), Vector3d(0, 0, 0), Vector3d(0, 0, 0),
                        0, 0, j + 1, j + 2)
#///////////////
    # rotate = calculate_rotate(rotation)
    # for i in range(fingercount):
    #     original[i] += subtract(arrays[i + 1][j + 1], arrays[i + 1][j])

    #the hero model

    # sim.add_object("../input/sphere12K.vtk", Vector3d(0, 0.2, 2.75),
    #                Vector3d(0, 0, 0), Vector3d(0, 0, 0), 0, Vector3d(2.5, 2.5, 1),True)
    #
    # sim.add_object("../input/cube_center.vtk", Vector3d(0, 0.2, 3.25),
    #                Vector3d(0, 0, 0), Vector3d(0, 0, 0), 0, Vector3d(2, 2, 0.01), True)
    # sim.set_DBC(Vector3d(-1, -0.8, 3.24), Vector3d(1, 1.2, 3.26),
    #             Vector3d(0, 0, -0.1), Vector3d(0, 0, 0), Vector3d(0, 0, 0), 0, 0, 0, 30)


    #bunny
    #sim.add_object("./output/main_model/model_p.vtk", model_pos,
    #                Vector3d(0, 0, 0), rotation,rotDeg, Vector3d(1.9, 1.9, 1.9), True)
    sim.add_object("./output/main_model/hero_0.vtk", model_pos,#model_pos + Vector3d(0, 0, 10),
                   Vector3d(0, 0, 0), rotation, rotDeg, Vector3d(1.82, 1.82, 1.82), True)
    #sim.add_object("../input/bunnyx30_13K.vtk", model_pos,
    #               Vector3d(0, 0, 0), Vector3d(0, 0, 0), 0, Vector3d(1, 1, 1), True)
    #sim.set_DBC(Vector3d(-2, -2, -2), Vector3d(2, 2, 2),
    #             Vector3d(0, 0, 0), Vector3d(0, 0, 0), Vector3d(0, 0, 0), 0, 0, 0, 30)
    #sim.add_object("./output/final_dumpling_compress/hero_0.obj", Vector3d(0, 0, 0),
    #               Vector3d(0, 0, 0), Vector3d(0, 0, 0),0, Vector3d(1, 1, 1), True)
    #sim.add_object("../input/sphere1K.vtk", model_pos,
    #               model_pos, rotation,rotDeg, Vector3d(1, 1, 1), True)
    #end
    #bunnyx30_13K.vtk
    # if currunt_content == '':

    sim.write_to_file("output/Ori(3).txt")

    print("start set p!\n")
    sim.initialize_added_objects(Vector3d(0, 0, 0), 1000, E, 0.4)
    sim.set_plasticity("bunnyx30_13K.vtk",E, 0.4, yield_stress, 1.e30, 0.)

    sim.dt = 0.05
    sim.frame_dt = 0.05
    #sim.frame_num = 1
    sim.frame_num = time_step
    sim.gravity = Vector3d(0, 0, 0)
    sim.initialize_OIPC(1e-6)
    sim.adjust_camera(2.5, [0, 0, 0])

    sim.run()
    # currunt_content = lines
    print('one trun ends!\n')

