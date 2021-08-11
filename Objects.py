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
        self.acceleration = initAcceleration
        self.init = np.hstack((self.position, self.velocity))
        self.KE = np.full((1,1),0,dtype=float)
        self.PE = np.full((1,1),0,dtype=float)
        self.linear_m = np.full((1,1),0,dtype=float)
        self.angular_m = np.full((1,1),0,dtype=float)


    """Creating a function that solves Newtons Law of gravity to find the acceleration"""

    """Creating a function to calculate the Momentum for each Particle"""

    """Creating a function to calculate the Momentum for each Particle"""
