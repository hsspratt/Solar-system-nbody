# %%
import numpy as np
from SlimObjects import Objects
import copy
import time
from slimsolar import TestSolarSystem
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
import scipy as sci
import time
import matplotlib as mpl
import random
# plt.switch_backend('Qt5Agg')
# from ExampleGUI import MyApp
import tkinter as tk
# import NGUI
# from SolarGUI import GUIplanets

# %% Initialising all the planets, suns and objects that could be used in the simulation

""" Using the objects class to input all the initial variables and initiliase the planets """

F8_1 = Objects('F8_1',
               1,
               np.array([-0.97000436, 0.24308753, 0]),
               np.array([0.4662036850, 0.4323657300, 0]),
               np.array([0,0,0]))

F8_2 = Objects('F8_2',
                1,
                np.array([0.97000436, -0.24308753, 0]),
                np.array([0.4662036850, 0.4323657300, 0]),
                np.array([0,0,0]))

F8_3 = Objects('F8_3',
                1,
                np.array([0,0,0]),
                np.array([-0.93240737, -0.86473146, 0]),
                np.array([0,0,0]))

F8_planet = Objects('F8_planet',
                  0.001,
                  np.array([-0.33, --0.3, 0]),
                  np.array([0,0,0]),
                  np.array([0,0,0]))

AC1 = Objects('AC1',
               1.1,
               np.array([-0.5,0,0]),
               np.array([0.01,0.01,0]),
               np.array([0,0,0]))

AC2 = Objects('AC2',
               0.907,
               np.array([0.5,0,0]),
               np.array([-0.05,0,-0.1]),
               np.array([0,0,0]))

AC_star = Objects('AC_star',
               1.0,
               np.array([0,1,0]),
               np.array([0,-0.01,0]),
               np.array([0,0,0]))

""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""
objects = [F8_1, F8_2, F8_3]
# [Sun, Earth, Mars, Venus, Mercury] # , Jupiter,Saturn,Neptune,Uranus]
solarsystem = TestSolarSystem(objects)


# %% Define constants
start=time.time()
"""
Defining the constant needed for the calculations. The initial positions and velocities needed to be converted
to m and m/s respectivly as the JPL NASA website provides it in AU and AU/Day. Other constants in clude the time
for the simulation which can be adjusted, and the number of iterations
"""

# Define universal gravitation constant
G = 1

# Reference quantities - to convert the emphemeris data from nasa to SI units
au = 1
v_factor = 1
year_s = 50

# Define times
tStart = 0e0
time_period = 6.32591398
iterations_year = 200
iterations_total = time_period*iterations_year
t_End = time_period*year_s
max_steps = t_End/(iterations_total*4)
t=tStart
domain = (t, t_End)

# Non-Dimensionalization constants
K1=1
K2=1

initial = np.full((1, 6), 0, dtype=float)
mass = np.full((1, 1), 0, dtype=float)

name = ""

N = len(objects) # Find the number of objects in the Solar list

planets_initial = np.full([N, 6],0, dtype=float)

# Creates an array for all the particles used so that the initial positions and velocities are know
for i in range(len(solarsystem.planets)):
    planets_initial[i] = solarsystem.planets[i].init

planets_pos = planets_initial[:,0:3]
planets_vel = planets_initial[:,3:6]

# Create an array with all the masses
planets_mass = np.full((N, 1),0, dtype=float)

for i in range(len(solarsystem.planets)):
    planets_mass[i] = solarsystem.planets[i].mass

# Finds the centre of mass
moment_of_mass = np.array([0,0,0])
for i in range(N):
    moment_of_mass = moment_of_mass + planets_mass[i]*planets_pos[i]
r_com=(moment_of_mass)/(sum(planets_mass))

# Finds centre of mass of velocity
momentum = np.array([0,0,0])
for i in range(N):
    momentum = momentum + planets_mass[i]*planets_vel[i]
v_com=(momentum)/(sum(planets_mass))

# Flattens the array as thats the form solve_ivp takes it in

planets_pos = planets_pos.flatten()
planets_vel = planets_vel.flatten()
init_params=np.hstack((planets_pos, planets_vel))

# %% Solve the equation for Gravity for the n body system

# ## Run the solve_ivp solver
three_body_sol = sci.integrate.solve_ivp(fun=Objects.ThreeBodyEquations,t_span=domain,y0=init_params,args=(G,planets_mass,N,K1,K2), max_step=max_steps)
iterations = len(three_body_sol['t']) # Find how many values of t were used t_eval=np.linspace(tStart, t_End, 100000)


# ## Store the position solutions into three distinct arrays
r_sol = np.full((N*3,iterations),0)
r_sol = three_body_sol['y'][0:N*3,:]
r_sol = r_sol.T

momentum_com = np.full((iterations,3),0, dtype=float)

for i in range(N):
    momentum_com += planets_mass[i]*r_sol[:,i*3:(i+1)*3]

rcom_sol = momentum_com/sum(planets_mass)

rearth_sol = r_sol[:,3:6]

r_com_sol = np.full((iterations,N*3),0)

g = np.hstack((rcom_sol, rcom_sol,rcom_sol))

# r_com_sol = r_sol - g

"""
for i in range(N):
    r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rcom_sol
"""

# [for i in range(N) r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rearth_sol]

# [x for x in (for i in range(N) r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rearth_sol)]

colours = ['black','g','b','gold','y','m','c','r','lime']
# [plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], color=colours[i], label=solarsystem.planets[i].name) for i in range(N)]; plt.legend()

end=time.time()
print("Time for intialising data and integrating is: " , end-start)

# %% Analysis
start = time.time()
for planet in solarsystem.planets:
    planet.KE = np.full((1,1),0,dtype=float)
    planet.PE = np.full((1,1),0,dtype=float)
    planet.linear_m = np.full((1,1),0,dtype=float)
    planet.angular_m = np.full((1,1),0,dtype=float)

KE = []
PE = []
angular = []
linear = []

for col in range(iterations):
    sol = three_body_sol['y'][:,col]
    temp_PE, temp_KE, temp_angular, temp_linear = TestSolarSystem.getEnergy(solarsystem, sol, planets_mass, G, N)
    KE.append(temp_KE)
    PE.append(temp_PE)
    angular.append(temp_angular)
    linear.append(temp_linear)

total = (np.array([KE])+np.array([PE])).flatten()

t = three_body_sol['t']



plotKE = plt.figure(1)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.KE[1:], colours[i], label=solarsystem.planets[i].name)
    plt.xlabel("Kinetic energy of planets in the solar system")
    plt.ylabel("Kinetic energy (J)")
    plt.legend()
plotKE.show()

plotPE = plt.figure(2)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.PE[1:], colours[i], label=solarsystem.planets[i].name)
    plt.xlabel("Potential energy of planets in the solar system")
    plt.ylabel("Potential energy (J)")
    plt.legend()
plotPE.show()

plotTotal = plt.figure(3)
plt.plot(t, KE, label="Kinetic energy")
plt.plot(t, PE, label="Potential energy")
plt.plot(t, total, label="Total energy")
plt.xlabel("Total energy of planets in the solar system over time")
plt.ylabel("Energy (J)")
plt.legend()
plotTotal.show()

plotOrbits = plt.figure(4)
for i in range(N):
    plt.plot(r_sol[:,i*3], r_sol[:,1+i*3], colours[i], label=solarsystem.planets[i].name)
    plt.legend()
plotOrbits.show()

plotLm = plt.figure(5)
plt.plot(t, linear)
plt.xlabel("Total linear momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plotLm.show()

plotAm = plt.figure(6)
plt.plot(t, angular)
plt.xlabel("Total angular momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plotAm.show()

end = time.time()

print("Time for calculating enrgy and plotting is:   " , end-start)


total_off = ((total-total[0])/total)*100
total_cor = [i for i in total if i >= 1]

if len(total_cor) == 0:
    print("This orbit looks stable. The change in error from the beginiing to end is: ", total_off[-1],"%")
else:
    print("The stablility of the orbit seems to be only valid up till the ", len(total_cor), " time step")

