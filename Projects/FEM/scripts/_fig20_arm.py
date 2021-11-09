import sys
sys.path.insert(0, "../../../Python")
sys.path.insert(0, "../../../build")
import Drivers
from JGSL import *

if __name__ == "__main__":

    model = "SD"
    if len(sys.argv) > 1:
        model = sys.argv[1]

    sim = Drivers.FEMSimulationBase("double", 3, model)

    sim.set_object("../input/arm10K.vtk", Vector3d(0, 0, 0), 1000, 1e5, 0.4)

    # DBCRangeMin, DBCRangeMax,
    # v, rotCenter, rotAxis, angVelDeg
    sim.set_DBC(Vector3d(-0.1, 0.45, 0.45), Vector3d(0.46, 0.55, 0.55),
                Vector3d(0, 0, 0), Vector3d(0, 0, 0), Vector3d(0, 0, 1), -20)
    sim.set_DBC(Vector3d(0.54, 0.45, 0.45), Vector3d(1.1, 0.55, 0.55),
                Vector3d(0, 0, 0), Vector3d(0, 0, 0), Vector3d(0, 0, 1), 20)
    sim.set_DBC(Vector3d(0.49, 0.45, 0.45), Vector3d(0.51, 0.55, 0.55),
                Vector3d(0, 0, 0), Vector3d(0, 0, 0), Vector3d(0, 0, 1), 0)

    sim.dt = 0.04
    sim.frame_dt = 0.04
    sim.frame_num = 100
    sim.gravity = Vector3d(0, 0, 0)
    sim.initialize_OIPC(1e-6)
    sim.run()
