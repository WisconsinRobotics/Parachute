import numpy as np
# Creates a frame that puts four modules in a rectangular arrangement
# TODO EXPERIMENT WITH ADDING MORE GEOMETRIC ARRANGEMENTS
class Frame:

        # Frame coords are initialized as (0,0) making the center of our frame the origin.
        frame_coords = np.array([0,0])

        def __init__(self, x_size, y_size, r_wheel):
            # Establish frame center coordinates and edge size in meters
            self.x_size = x_size
            self.y_size = y_size
            self.r_wheel = r_wheel
            # Establishes translational and rotational velocity
            self.v_comp = np.array([])
            self.w_comp = []
            self.r_perp = []
            self.m_coords = []
            self.m_vectors = [np.array([0, 1]) for _ in range(4)]
            self.output_vectors = []
            self.output_vel = []
            self.m_vel = [np.linalg.norm(self.m_vectors[i]) for i in range(len(self.m_vectors))]
            self.wheel_speeds = []
            # Calculate module coordinates
            self.m_coords.append(np.array([x_size / 2, y_size / 2]))
            self.m_coords.append(np.array([-x_size / 2, y_size / 2]))
            self.m_coords.append(np.array([-x_size / 2, -y_size / 2]))
            self.m_coords.append(np.array([x_size / 2, -y_size / 2]))
            # Use module coordinates to determine a perpendicular vector to the frame
            self.r_perp = [np.array([-(self.m_coords[i] - self.frame_coords)[1],
                                      (self.m_coords[i] - self.frame_coords)[0]])
                                      for i in range(len(self.m_coords))]

        # Sets target velocity and scales perpendiculars
        def set_target_vel(self, v, w):
            # Sets velocity as a numpy array
            self.v_comp = v
            # Adds the omega scaled perp vector to a list
            self.w_comp = [w * (perp/np.linalg.norm(perp)) for perp in self.r_perp]
            # May need to be done individually if implementation was wrong
            self.output_vectors = [np.array([self.v_comp[0] + self.w_comp[i][0],
                                             self.v_comp[1] + self.w_comp[i][1]])
                                   for i in range(len(self.w_comp))]
            self.output_vel = [np.linalg.norm(output) for output in self.output_vectors]

        def rotate_module(self):
            for i in range(len(self.output_vectors)):
                phi = np.arccos((np.dot(self.output_vectors[i], self.m_vectors[i])) /
                                (self.m_vel[i] * self.output_vel[i]))
                cw = np.array([[np.cos(phi), np.sin(phi)],
                               [-np.sin(phi), np.cos(phi)]])
                ccw = np.array([[np.cos(phi), -np.sin(phi)],
                                [np.sin(phi), np.cos(phi)]])
                if np.cross(self.output_vectors[i], self.m_vectors[i]) > 0:
                    # Rotate CW
                    self.m_vectors[i] = (np.matmul(cw, self.m_vectors[i]) *
                                         (np.linalg.norm(self.output_vectors[i])))
                else:
                    # Rotate CCW
                    self.m_vectors[i] = (np.matmul(ccw, self.m_vectors[i]) *
                                         (np.linalg.norm(self.output_vectors[i])))

                self.m_vel = [(np.linalg.norm(m)) for m in self.m_vectors]

                self.wheel_speeds.append(self.m_vel[i]/self.r_wheel)

            return self.m_vectors