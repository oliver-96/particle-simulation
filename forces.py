import numpy as np

def gravity_force(mass):
    gravity_acceleration = 10
    
    return np.array((0, gravity_acceleration * mass))