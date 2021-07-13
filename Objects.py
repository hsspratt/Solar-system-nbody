import numpy as np
import time

class Objects():

    position = np.full((1, 3), 0)
    velocity = np.full((1, 3), 0)
    acceleration = np.full((1, 3), 0)
    name = ""
    mass = np.full((1, 1), 0)

    planets_init = np.full((1, 3), 0)

    def __init__(self, Name, Mass, initPosition, initVelocity, initAcceleration):

        au = 149597870.700e3
        v_factor = 1731460

        self.name = Name
        self.mass = Mass
        self.position = initPosition*au
        self.velocity = initVelocity*v_factor
        self.position_non = initPosition
        self.velocity_non = initVelocity
        self.acceleration = initAcceleration
        # self.color = color
        self.init = np.hstack((self.position, self.velocity))
        self.init_non = np.hstack((self.position_non, self.velocity_non))
        self.oldinit = np.hstack((self.position, self.velocity))
        self.solution = [] # np.array([0, 0, 0])
        self.pos = np.array([0,0,0])
        self.vel = np.array([0,0,0])
        self.variables = np.hstack((self.position, self.velocity))
        self.KE = np.full((1,1),0,dtype=float)
        self.PE = np.full((1,1),0,dtype=float)
        self.linear_m = np.full((1,1),0,dtype=float)
        self.angular_m = np.full((1,1),0,dtype=float)

    def CombineArrays(self, Positions, Velocities, Accelerations, Names, Masses):
        Positions = Positions.append(self.position)
        Velocities = Velocities.append(self.velocity)
        Accelerations = Accelerations.append(self.acceleration)
        Names = Names.append(self.name)
        Masses = Masses.append(self.mass)


    def ThreeBodyEquations(t,sol,G,mass,N,K1,K2):

        planets_mass = mass

        planets_pos = np.full([N,3],0,dtype=float)
        planets_vel = np.full([N,3],0,dtype=float)

        for i in range(N):
            planets_pos[i,:] = sol[i*3:(i+1)*3]
            planets_vel[i,:] = sol[N*3+(i*3):N*3+(1+i)*3]

        # Unpack all the variables from the array "w"

        # Harry's attempt
        G = G

        # positions r = [x,y,z] for all particles
        x = planets_pos[:,0:1]
        y = planets_pos[:,1:2]
        z = planets_pos[:,2:3]

        # matrix that stores all pairwise particle separations: r_j - r_i
        dx = x.T - x
        dy = y.T - y
        dz = z.T - z

        # matrix that stores 1/r^3 for all particle pairwise particle separations
        inv_r3 = (dx**2 + dy**2 + dz**2)

        inv_r3[inv_r3>0] = inv_r3[inv_r3>0]**(-1.5)

        ax = G * (dx * inv_r3) @ planets_mass
        ay = G * (dy * inv_r3) @ planets_mass
        az = G * (dz * inv_r3) @ planets_mass

        # print(dx*inv_r3)
        # planets_acceleration = np.sqrt(ax**2 + ay**2 + az**2)

        planets_acceleration = np.hstack((ax,ay,az))
        drbydt = K2*planets_vel.flatten()
        dvbydt = K1*planets_acceleration.flatten()

        derivs = np.concatenate((drbydt, dvbydt))

        return derivs

    def kineticenergy(self):
        kineticenergy = (0.5) * self.mass * self.velocity.dot(self.velocity)
        return kineticenergy

    """Creating a function to calculate the Momentum for each Particle"""

    def Momentum(self):
        Momentum = self.mass * (np.linalg.norm(self.velocity))
        return Momentum