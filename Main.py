import numpy as np
from Frame import Frame

v = np.array([-4.5,3.6])
w = 3

fr = Frame(x_size=0.25, y_size=0.25, r_wheel=2)

fr.set_target_vel(v, w)

print(fr.output_vectors)
print(fr.rotate_module())
print(fr.output_vel)
print(fr.m_vel)
print(fr.wheel_speeds)