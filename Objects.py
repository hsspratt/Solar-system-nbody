import numpy as np

"""Creating the Objects class"""

class Objects():

    position = np.full((1, 3), 0)
    velocity = np.full((1, 3), 0)
    acceleration = np.full((1, 3), 0)
    name = ""
    mass = np.full((1, 1), 0)

    planets_init = np.full((1, 3), 0)

    """Initialisng all the data for each Object - all data stored under its name"""

    def __init__(self, Name, Mass, initPosition, initVelocity, initAcceleration):

        self.name = Name
        self.mass = Mass
        self.position = initPosition
        self.velocity = initVelocity
        self.currentPosition = []
        # self.position_non = initPosition
        # self.velocity_non = initVelocity
        self.acceleration = initAcceleration
        # self.color = color
        self.init = np.hstack((self.position, self.velocity))
        # self.init_non = np.hstack((self.position_non, self.velocity_non))
        # self.oldinit = np.hstack((self.position, self.velocity))
        # self.solution = [] # np.array([0, 0, 0])
        # self.pos = np.array([0,0,0])
        # self.vel = np.array([0,0,0])
        # self.variables = np.hstack((self.position, self.velocity))
        self.KE = np.full((1,1),0,dtype=float)
        self.PE = np.full((1,1),0,dtype=float)
        self.linear_m = np.full((1,1),0,dtype=float)
        self.angular_m = np.full((1,1),0,dtype=float)


    """Creating a function that solves Newtons Law of gravity to find the acceleration"""


    def ThreeBodyEquations(t,sol,G,mass,N,K1,K2):
        """
        Calculates acceleration on each object due to Newton's Law
        planets_pos  is an N x 3 matrix of positions
	    planets_mass is an N x 1 vector of masses
	    G is Newton's Gravitational constant
	    dvbydt is N x 3 matrix of accelerations

        """
        # saves all the planets masses
        planets_mass = mass

        # creates a numpy array for the data to be saved into
        planets_pos = np.full([N,3],0,dtype=float)
        planets_vel = np.full([N,3],0,dtype=float)

        # sci.integrate.solve_ivp() gave the solution planet by planet with the first half
        # of the array being position and the latter half velocity, this splits the solution
        # up into its resepective counterparts

        for i in range(N):
            planets_pos[i,:] = sol[i*3:(i+1)*3]
            planets_vel[i,:] = sol[N*3+(i*3):N*3+(1+i)*3]

        # Harry's attempt
        G = G

        # positions r = [x,y,z] for all particles
        x = planets_pos[:,0:1]
        y = planets_pos[:,1:2]
        z = planets_pos[:,2:3]

        # matrix that stores all pairwise particle separations: r_j - r_i
        # it should be noted that this matrix way is very fast in contrast to looping
        # planet by planet finding the respective distances. While not "technically"
        # mathematically allowed with the laws of matricies the result is very useful

        dx = x.T - x
        dy = y.T - y
        dz = z.T - z


        # matrix that stores 1/r^3 for all particle pairwise particle separations
        inv_r3 = (dx**2 + dy**2 + dz**2)

        inv_r3[inv_r3>0] = inv_r3[inv_r3>0]**(-1.5)

        ax = G * (dx * inv_r3) @ planets_mass
        ay = G * (dy * inv_r3) @ planets_mass
        az = G * (dz * inv_r3) @ planets_mass

        # pack all the variables components back togeather
        planets_acceleration = np.hstack((ax,ay,az)) # containing accelersation of all
        drbydt = K2*planets_vel.flatten()            # solution for derivative of the position
        dvbydt = K1*planets_acceleration.flatten()   # solution for derivative of the velocity

        derivs = np.concatenate((drbydt, dvbydt))

        return derivs

    """Creating a function to calculate the Momentum for each Particle"""

    def kineticenergy(self):
        kineticenergy = (0.5) * self.mass * self.velocity.dot(self.velocity)
        return kineticenergy

    """Creating a function to calculate the Momentum for each Particle"""

    def Momentum(self):
        Momentum = self.mass * (np.linalg.norm(self.velocity))
        return Momentum