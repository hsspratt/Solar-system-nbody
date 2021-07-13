import numpy as np
from SlimObjects import Objects
import copy
import time
from solar import TestSolarSystem
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
import scipy as sci
import time
import matplotlib as mpl
import random

# import NGUI

# mpl.rcParams['animation.ffmpeg_path'] = r'/Users/harry/Desktop/Desktop – Harry’s MacBook Pro/Quick N-Body/ffmpeg'

# %% Initialising all the planets, suns and objects that could be used in the simulation

""" Using the objects class to input alol the initial variables and initiliase the planets """

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

Saturn = Objects('Saturn',
               5.6834e26,
               np.array([5.409527551219896E+00, -8.387647661909122E+00, -6.952095229728303E-02]),
               np.array([4.377905875627875E-03, 3.010222250503800E-03, -2.269189986953596E-04]),
               np.array([0,0,0]))

Neptune = Objects('Neptune',
               5.6834e26,
               np.array([5.409527551219896E+00, -8.387647661909122E+00, -6.952095229728303E-02]),
               np.array([4.377905875627875E-03, 3.010222250503800E-03, -2.269189986953596E-04]),
               np.array([0,0,0]))

Uranus = Objects('Uranus',
               86.813e24,
               np.array([1.538595512099490E+01, 1.241875975077764E+01, -1.532033630108008E-01]),
               np.array([-2.499218584280511E-03, 2.877287547390077E-03, 4.308752491196167E-05]),
               np.array([0,0,0]))

# =============================================================================
# planet_dictionary = {
#     'Sun' : Sun,
#     'Earth': Earth,
#     'Mars': Mars,
#     'Venus': Venus,
#     'Mercury': Mercury,
#     'Jupiter': Jupiter,
#     'Saturn': Saturn,
#     'Neptune': Neptune,
#     'Uranus': Uranus,
#     'Moon': Moon
#     }
# =============================================================================


""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""
objects = [F8_1, F8_2, F8_3]
"""
print(NGUI.List)
for planet in NGUI.List:
    objects.append(planet_dictionary[planet])
"""
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

# Reference quantities
au = 1
v_factor = 1
year_s = 50

# Define times
tStart = 0e0
years = 6.32591398
iterations_year = 200
iterations_total = years*iterations_year
t_End = years*year_s
max_steps = t_End/(iterations_total*4)
t=tStart
domain = (t, t_End)

K1=1
K2=1

initial = np.full((1, 6), 0, dtype=float)
name = ""
mass = np.full((1, 1), 0, dtype=float)

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
iterations = len(three_body_sol['t']) # Find how many values of t were used


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

r_com_sol = r_sol - g

"""
for i in range(N):
    r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rcom_sol
"""

# [for i in range(N) r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rearth_sol]

# [x for x in (for i in range(N) r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rearth_sol)]

colours = ['black','g','b','gold','y','m','c','r','lime']
# [plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], color=colours[i], label=solarsystem.planets[i].name) for i in range(N)]; plt.legend()

end=time.time()
print("Time for the integration script is: " , end-start)

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

print("Time for the plotting script is: " , end-start)

# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc

fig, ax = plt.subplots()

line, = ax.plot(r_com_sol[:,0], r_com_sol[:,1], "-")
line1, = ax.plot(r_com_sol[0,0], r_com_sol[0,1], "ro")
line2, = ax.plot(r_com_sol[0,3], r_com_sol[0,4], "bo")
line3, = ax.plot(r_com_sol[0,6], r_com_sol[0,7], "go")

def connect(i):
    start=max((i-5,0))
    line1.set_data(r_com_sol[start:i,0],r_com_sol[start:i,1])
    return line1,

def connect1(i):
    start=max((i-5,0))
    line2.set_data(r_com_sol[start:i,3],r_com_sol[start:i,4])
    return line2,

def connect2(i):
    start=max((i-5,0))
    line3.set_data(r_com_sol[start:i,6],r_com_sol[start:i,7])
    return line3,

ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ani = animation.FuncAnimation(fig, connect, np.arange(1, 100), interval=100)
ani1 = animation.FuncAnimation(fig, connect1, np.arange(1, 100), interval=100)
ani2 = animation.FuncAnimation(fig, connect2, np.arange(1, 100), interval=100)

plt.show()

# %%

r_sol_anim=r_sol[::1,:].copy()

head = np.full((iterations,N*3),0)


#Set initial marker for planets, that is, blue,red and green circles at the initial positions
for i in range(N):
    head[:,i*3]=[ax.scatter(r_sol_anim[0,i*3],r_sol_anim[0,1+i*3],r_sol_anim[0,2+i*3],color=colours[i],marker="o",s=100,label=solarsystem.planets[i].name)]

#Create a function Animate that changes plots every frame (here "i" is the frame number)
def Animate(i,head):
    #Remove old markers
    head[0].remove()

    #Plot the orbits (every iteration we plot from initial position to the current position)
    for i in range(N):
        trace=ax.plot(r_sol_anim[:i,0+i*3],r_sol_anim[:i,1+i*3],r_sol_anim[:i,2+i*3],color=colours[i],label=solarsystem.planets[i].name)


    #Plot the current markers
    for i in range(N):
        head[0]=ax.scatter(r_sol_anim[i-1,0],r_sol_anim[i-1,1],r_sol_anim[i-1,2],color=colours[i],marker="o",s=100,label=solarsystem.planets[i].name)


    return trace,head

#Add a few bells and whistles
ax.set_xlabel("x-coordinate",fontsize=14)
ax.set_ylabel("y-coordinate",fontsize=14)
ax.set_zlabel("z-coordinate",fontsize=14)
# ax.set_xlim(-2.5e11, 2.5e11)
# ax.set_ylim(-2.5e11, 2.5e11)
# ax.set_zlim(-2.5e11, 2.5e11)
ax.set_box_aspect([1,1,1])
ax.set_title("Visualization of orbits of stars in a N-body system",fontsize=14)

for i in range(N):
    anim=animation.FuncAnimation(fig,Animate, save_count=200, repeat=False,blit=False,fargs=(head))


