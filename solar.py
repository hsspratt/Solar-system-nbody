from Objects import Objects
import numpy as np
import scipy.constants

G = scipy.constants.G
planets_init = []

"""Creating the SolarSystem class"""

class SolarSystem:

    planets = []

    G = scipy.constants.G

    def __init__(self, planets_to_add):
        self.planets = planets_to_add

    def numberofplanets(self):
        n = len(self.planets)
        return n

    def array_thing(self, Positions, Velocities, Accelerations, Names, Masses):
        for planet in self.planets:
            planet.arrays(Positions, Velocities, Accelerations, Names, Masses)

    def init_thing(self):
        for i in range(len(self.planets)):
            planets_init[i].append(self.planets[i].init)
            return planets_init

    """Creating a function that calculates the individual kinetic energy of each Particle and then caculates the total
    kinetic energy of the simulation by summing the individual kinetic energies of each Particle"""

    def totalkinetic(self):
        totalkineticenergy = 0.
        for planet in self.planets:
            totalkineticenergy += planet.kineticenergy()
        return totalkineticenergy

    """Creating a function that calculates the individual potential energy of each Particle and then caculates the total
    potential energy of the simulation by summing the individual potential energies of each Particle"""

    def totalpotential(self):
        totalpotential = 0.
        for planet in self.planets:
            for otherplanet in self.planets:
                if planet != otherplanet:
                    distancebetween = otherplanet.position - planet.position
                    totalpotential += (self.G*planet.mass*otherplanet.mass)/(np.linalg.norm(distancebetween))
        return totalpotential

    def totalmom(self):
        totalmom = 0.
        for planet in self.planets:
            totalmom += planet.Momentum()
        return totalmom

    """Creating a function that calculates the total energy of the whole simulation by summing the total kinetic energy
    and total potential energy of the whole system"""

    def TotalEnergy(self):
        totalEnergy = 0.
        for planet in self.planets:
            totalEnergy = self.totalkinetic() + self.totalpotential()
        return totalEnergy

    def getEnergy(self, sol, planets_mass, G, N, v_com):
        """
        Get kinetic energy (KE) and potential energy (PE) of simulation
        pos is N x 3 matrix of positions
        vel is N x 3 matrix of velocities
        mass is an N x 1 vector of masses
        G is Newton's Gravitational constant
        KE is the kinetic energy of the system
        PE is the potential energy of the system
        """

        v_x = np.array([sol[(N*3)::3]])
        v_y = np.array([sol[(N*3)+1::3]])
        v_z = np.array([sol[(N*3)+2::3]])

        v = np.vstack((v_x, v_y, v_z))
        
        v_com = np.tile(v_com, [N, 1])
        v_com = v_com.T

        vel = np.array([np.linalg.norm(v, axis=0)]).T
        # print(vel.shape)
        # Kinetic Energy:
        KE = 0.5 * planets_mass * vel**2

        total_KE = 0.5 * np.sum(np.sum(planets_mass * vel**2))
                
        virial_KE = np.average(0.5 * planets_mass * vel**2)

        # Potential Energy:

        # positions r = [x,y,z] for all particles

        x = np.array([sol[0:N*3:3]])
        y = np.array([sol[1:N*3:3]])
        z = np.array([sol[2:N*3:3]])

        # matrix that stores all pairwise particle separations: r_j - r_i
        dx = x.T - x
        dy = y.T - y
        dz = z.T - z

        	# matrix that stores 1/r for all particle pairwise particle separations
        inv_r = np.sqrt(dx**2 + dy**2 + dz**2)
        inv_r[inv_r>0] = 1.0/inv_r[inv_r>0]

        	# sum over upper triangle, to count each interaction only once
        # PE = G * np.sum(np.triu(-(mass*mass.T)*inv_r,1),axis=0)
        PE = G * np.sum(-(planets_mass*planets_mass.T)*inv_r,axis=0)
        total_PE = G * np.sum(np.sum(np.triu(-(planets_mass*planets_mass.T)*inv_r,1)))

        r = np.vstack((x,y,z))

        linear_momentum = planets_mass.flatten() * (v-v_com)

        L_linear = np.linalg.norm(linear_momentum, axis=0)

        L_angular = np.full((N,3),0, dtype=float)

        angular_m = []

        for i in range(N):
            L_angular[i,:] = np.cross(np.array([r[:,i]]), np.array([linear_momentum[:,i]])).flatten()
            angular_m =  np.sum(L_angular, axis=1)

        total_angular = np.sum(angular_m)
        total_linear = np.sum(L_linear)
        total_linear_x = np.sum(linear_momentum, 1)[0]
        total_linear_y = np.sum(linear_momentum, 1)[1]
        total_linear_z = np.sum(linear_momentum, 1)[2]

        # L = np.sum(np.sum(np.triu(mass * vel * np.sqrt(dx**2 + dy**2 + dz**2),1)))

        for planet in self.planets:
            for index in range(N):
                if index == self.planets.index(planet):
                    planet.KE = np.vstack((planet.KE, KE[index]))
                    planet.PE = np.vstack((planet.PE, PE[index]))
                    planet.linear_m = np.vstack((planet.linear_m, linear_momentum[:,index]))
                    planet.angular_m = np.vstack((planet.angular_m, angular_m[index]))

        return total_KE, total_PE, total_angular, total_linear, total_linear_x, total_linear_y, total_linear_z;