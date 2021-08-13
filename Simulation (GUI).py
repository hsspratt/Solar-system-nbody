# %%
from init_objects import *
from mpl_toolkits.mplot3d.axes3d import Axes3D
import pandas as pd
import subprocess
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import scipy.integrate
from matplotlib import cm
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from Objects import Objects
import copy
import time
from solar import SolarSystem
from scipy.integrate import solve_ivp
import scipy as sci
import matplotlib as mpl
import tkinter as tk
import n_body_app
import os
import sys
plt.rc('mathtext', fontset="cm")

# %% Initialising all the planets, suns and objects that could be used in the simulation

"""Code to create and run GUI, from which you can change the configuration of the simulation"""

root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')
app = n_body_app.n_body_app(root)
root.mainloop()


planets = app.planets

print(planets)
objects = []

x = [Sun,  Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, External_Planet
     , Butterfly_I, Butterfly_II, Butterfly_III, moth_I, moth_II, moth_III, bumblebee, 
     pythag, pythag_I, Solar_System, Figure_8, goggles, yarn, yin_yang_I_a, Flower_in_circle, dragonfly
     ]

thisdict = {
    'Butterfly_I': Butterfly_I,
    'Butterfly_II': Butterfly_II,
    'Butterfly_III': Butterfly_III,
    'moth_I': moth_I,
    'moth_II': moth_II,
    'moth_III': moth_III,
    'bumblebee': bumblebee,
    'pythag': pythag,
    'pythag_I': pythag_I,
    'Solar_System': Solar_System,
    'Figure_8': Figure_8,
    'goggles': goggles,
    'yarn': yarn,
    'yin_yang_I_a': yin_yang_I_a,
    'Flower_in_circle': Flower_in_circle,
    'dragonfly': dragonfly
    }

try:
    for i in range(len(x)):
        if str(x[i].name) in planets:
            objects.append(x[i])
except AttributeError:
    if len(x) > 0:
        pass
    pass
    if len(planets) == 0:
        objects = thisdict['Solar_System']
        print("The defult configuration - the solar system - has been initiated")
    if len(planets) == 1:
        objects = thisdict[planets[0]]
    print(len(objects), " objects have been initialised into the simulation")

""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""
""" Using the objects class to input all the initial variables and initiliase the planets """

solarsystem = SolarSystem(objects)

# %% Define constants
start=time.time()
"""
Defining the constant needed for the calculations. The initial positions and velocities needed to be converted
to m and m/s respectivly as the JPL NASA website provides it in AU and AU/Day. Other constants in clude the time
for the simulation which can be adjusted, and the number of iterations
"""

# Define universal gravitation constant
G = float(app.G.get())  # 6.67408e-11

# Reference quantities - to convert the emphemeris data from nasa to SI units
years = float(app.n_time_period.get())  # 100

# Define times
tStart = 0e0
time_period = float(app.time_period.get())  # 60*60*24*365
n_time_periods = years
iterations_year =  float(app.iterations.get()) # 25
iterations_total = n_time_periods*iterations_year
t_End = time_period*n_time_periods
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
where_are_NaNs = np.isnan(r_com)
r_com[where_are_NaNs] = 0

# Finds centre of mass of velocity
momentum = np.array([0,0,0])
for i in range(N):
    momentum = momentum + planets_mass[i]*planets_vel[i]
v_com=(momentum)/(sum(planets_mass))
where_are_NaNs = np.isnan(v_com)
v_com[where_are_NaNs] = 0

# Flattens the array as thats the form solve_ivp takes it in

planets_pos = planets_pos.flatten()
planets_vel = planets_vel.flatten()
init_params=np.hstack((planets_pos, planets_vel))

# %% Solve the equation for Gravity for the n body system

# ## Get constantys from GUI

if len(app.ODE) > 1:
            print("Only one ODE solver must be selected!")
if len(app.ODE) == 0:
    app.ODE = ["RK45"]
    print("The defult ODE solver will be used as none were selected")

rtol = float(app.rtol.get())
atol = float(app.rtol.get())
integrator = app.ODE

# ## Run the solve_ivp solver
three_body_sol = sci.integrate.solve_ivp(fun=SolarSystem.ThreeBodyEquations, t_span=domain, y0=init_params, args=(
    G, planets_mass, N, K1, K2), max_step=max_steps, rtol=rtol, atol=atol, method=integrator[0])
t = three_body_sol['t']
iterations = len(three_body_sol['t']) # Find how many values of t were used

# ## Store the position solutions into three distinct arrays
r_sol = np.full((N*3,iterations),0)
r_sol = three_body_sol['y'][0:N*3,:]
r_sol = r_sol.T

# ## Chaanges the reference apoint to about that of the COM
momentum_com = np.full((iterations,3),0, dtype=float)

for i in range(N):
    momentum_com += planets_mass[i]*r_sol[:,i*3:(i+1)*3]

rcom_sol = momentum_com/sum(planets_mass)
where_are_NaNs = np.isnan(rcom_sol)
rcom_sol[where_are_NaNs] = 0
rearth_sol = r_sol[:,3:6]

r_com_sol = np.empty((iterations,N*3))

for i in range(N):
    r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rcom_sol

g = np.hstack((rcom_sol, rcom_sol,rcom_sol))

end=time.time()
print("Time for intialising data and integrating is: " , end-start)

# %% Analysis
start = time.time()
for planet in solarsystem.planets:
    planet.KE = np.full((1,1),0,dtype=float)
    planet.PE = np.full((1,1),0,dtype=float)
    planet.linear_m = np.full((1,3),0,dtype=float)
    planet.angular_m = np.full((1,1),0,dtype=float)

KE = []
PE = []
angular = []
linear = []
linear_x = []
linear_y = []
linear_z = []


colours = ['black','g','b','gold','y','m','c','r','lime','navy']

for col in range(iterations):
    sol = three_body_sol['y'][:,col]
    temp_KE, temp_PE, temp_angular, temp_linear, temp_linear_x, temp_linear_y, temp_linear_z = SolarSystem.getEnergy(
        solarsystem, sol, planets_mass, G, N, v_com)
    KE.append(temp_KE)
    PE.append(temp_PE)
    angular.append(temp_angular)
    linear.append(temp_linear)
    linear_x.append(temp_linear_x)
    linear_y.append(temp_linear_y)
    linear_z.append(temp_linear_z)
    
KE = np.array([KE])
PE = np.array([PE])
angular = np.array([angular])
linear = np.array([linear])
linear_x = np.array([linear_x])
linear_y = np.array([linear_y])
linear_z = np.array([linear_z])

"""Defining the energies which are the sum of other to plot"""
total = (KE+PE).flatten()

virial = (2*np.average(KE)+np.average(PE)).flatten()

save_results_to = sys.path[0] + "/Plots Generated/"

plotKE = plt.figure(1)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.KE[1:,0], colours[i], label=solarsystem.planets[i].name, linewidth=0.9)
plt.title("Kinetic energy of individual planets", fontsize='9')
plt.xlabel(r"Time ($s$)")
plt.ylabel(r"Kinetic energy ($J$)")
plotKE.legend(loc='center right', bbox_to_anchor=(0.90, 0.5))
plotKE.show()
plotKE.savefig(save_results_to + 'planets_KE.png', dpi=600, bbox_inches='tight')

plotPE = plt.figure(2)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.PE[1:,0], (colours)[i], label=solarsystem.planets[i].name, linewidth=0.9)
    plt.title("Potential energy of individual planets over $%.2f$ time periods" % (n_time_periods,),fontsize='9')
    plt.xlabel("Time ($s$)")
    plt.ylabel("Potential energy ($J$)")
    plotKE.legend()
    plotKE.show()
plotPE.show()
plotPE.savefig(save_results_to + "planets_PE.png", bbox_inches='tight')

plotTotal = plt.figure(3)
plt.plot(t, KE.flatten(), label="Kinetic energy",linewidth=0.9)
plt.plot(t, PE.flatten(), label="Potential energy", linewidth=0.9)
plt.plot(t, total, label="Total energy", linewidth=0.9)
plt.plot(t, np.full((1, len(t)), virial)[0,:], label="$KE + 2PE = 0$", linewidth=0.9)
plt.title("Comparison of KE, PE and total energy of objects over time",fontsize='9')
plt.xlabel("Time ($s$)")
plt.ylabel("Energy ($J$)")
plotTotal.legend(loc='center right', bbox_to_anchor=(0.90, 0.5))
plotTotal.show()
plotTotal.savefig(save_results_to +'Total_Energy_System.png', bbox_inches='tight', dpi=600)

plotOrbits = plt.figure(4)
for i in range(N):
    plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], (colours)[i], label=solarsystem.planets[i].name,linewidth=0.9)
plt.title("Orbits mapped - 2D")
plt.xlabel("$x$ ($m$)")
plt.ylabel("$y$ ($m$)")
plotOrbits.legend(loc='center right', bbox_to_anchor=(0.90, 0.5))
plotOrbits.show()
plotOrbits.savefig(save_results_to +'Orbits_System.png', bbox_inches='tight', dpi=600)

plotLm = plt.figure(5)
plt.plot(t, linear.flatten(), linewidth=0.9)
plt.title("Total linear momentum of objects in the system over time", fontsize='9')
plt.xlabel("Time ($s$)")
plt.ylabel("Linear momentum ($kgms^{-2}$)")
plotLm.legend()
plotLm.show()
plotLm.savefig(save_results_to +'Linear_Momentum_System.png', bbox_inches='tight')

plotAm = plt.figure(6)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t[1:], planet.angular_m[1:-1, 0], (colours)[i],
             label=solarsystem.planets[i].name, linewidth=0.9)
plt.plot(t, angular.flatten(), linewidth=0.9, label='Total')
plt.title("Total angular momentum of objects in the system over time", fontsize='9')
plt.xlabel("Time ($s$)")
plt.ylabel("Angular Momentum ($kgm^2s^{-1}$)")
plotAm.legend()
plotAm.show()
plotAm.savefig(save_results_to +'Angular_Momentum_System.png',dpi=600, bbox_inches='tight')

# threeD_plot = plt.figure(7)
threeD_plot = plt.figure(figsize=plt.figaspect(1)*2)
# ax = p3.Axes3D(threeD_plot)
ax = threeD_plot.gca(projection='3d', proj_type = 'ortho')
x_scale = 4
y_scale = 4
z_scale = 1
scale = np.diag([x_scale, y_scale, z_scale, 1.0])
scale = scale*(1.0/scale.max())
scale[3, 3] = 1.0

def short_proj():
  return np.dot(Axes3D.get_proj(ax), scale)

ax.get_proj = short_proj
ax.view_init(elev=45/2, azim=45)
ax.dist = 7
line = [ax.plot(r_com_sol[:, i*3], r_com_sol[:, i*3+1], r_com_sol[:,i*3+2], c=(colours)[i], label=solarsystem.planets[i].name, linewidth=0.9)[0] for i in range(N)]
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
ax.set_zlim([-0.5e12,0.5e12])
ax.set_title("Static 3D Orbit")
threeD_plot.legend(loc='center right')
threeD_plot.show()
threeD_plot.savefig(save_results_to +'3D static plot.png',dpi=600, bbox_inches='tight')
plt.clf()

plotLx = plt.figure(7)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.linear_m[:-1, 0], (colours)[i], label=solarsystem.planets[i].name, linewidth=0.9)
plt.title("$x$ component of linear momentum over time", fontsize='9')
plt.xlabel("Time")
plt.ylabel("Linear momentum ($kgms^{-2}$)")
plotLx.legend(loc='upper left', bbox_to_anchor=(0.12, 0.80))
plotLx.show()
plotLx.show()
plotLx.savefig(save_results_to +'planets_momentum_x.png',dpi=600, bbox_inches='tight')

plotL_xyz = plt.figure(8)
plt.plot(t, linear_x.flatten(),linewidth=0.9, label='$x$')
plt.plot(t, linear_y.flatten(), linewidth=0.9, label='$y$')
plt.plot(t, linear_z.flatten(), linewidth=0.9, label='$z$')
plt.xlabel("Components of linear momentum over time", fontsize='9')
plt.ylabel("Linear momentum ($kgms^{-2}$)")
plotL_xyz.legend(loc='center left', bbox_to_anchor=(0.15, 0.75))
plotL_xyz.show()
plotL_xyz.savefig(save_results_to +'Linear_Momentum_System_components.png',dpi=600, bbox_inches='tight')

plot_planetsAngular = plt.figure(11)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t[1:], planet.angular_m[1:-1, 0], (colours)[i],
             label=solarsystem.planets[i].name, linewidth=0.9)
plt.title("$x$ component of linear momentum over time", fontsize='9')
plt.xlabel("Time")
plt.ylabel("Angular momentum ($kgms^{-2}$)")
plot_planetsAngular.legend(loc='upper left', bbox_to_anchor=(0.12, 0.90))
plot_planetsAngular.show()
plot_planetsAngular.savefig(save_results_to + 'planets_momentum_angular.png', dpi=600, bbox_inches='tight')

end = time.time()

print("Time for calculating enrgy and plotting is:   " , end-start)

"""Crudely evaluates when the orbit and physics is no longer valid"""

total_off = ((total-total[0])/total)*100
total_cor = [i for i in total_off if i >= 1]

if len(total_cor) == 0:
    print("This orbit looks stable. The change in error from the beginiing to end is: ", total_off[-1],"%")
else:
    print("The stablility of the orbit seems to be only valid up till the ", len(total_cor), " time step")

# %% If animation wanted uncomment this section
"""
cm = plt.cm.get_cmap('tab10')
colours = cm.colors

anim_r_com_sol = r_com_sol[0::20,:].copy()
data_len = anim_r_com_sol.shape[:][0]

x = np.array(range(anim_r_com_sol.shape[:][0]))

# define new x range, we need 7 equally spaced values
xnew = np.linspace(x.min(), x.max(), 9)

# apply the interpolation to each column
f = interp1d(x, anim_r_com_sol, axis=0)

data = np.empty((data_len, N, 3))

for i in range(3):
    data[:,:,i] = anim_r_com_sol[:,i::3]

fig = plt.figure()
ax = p3.Axes3D(fig)
ax.set_xlabel('X')

ax.set_ylabel('Y')

ax.set_zlabel('Z')
ax.set_zlim([-3e12,3e12])


ax.set_title("Animated Orbit ")


h_particles = [ax.plot(*data[:1, i].T, marker='o', c=colours[i], ls='None')[0] for i in range(N)]
trace = [ax.plot(data[:1,i,0], data[:1,i,1], data[:1,i,2], c=colours[i])[0] for i in range(N)]

def update_particles(num):
    print(num, " out of ", len(x))
    global h_particles
    global trace

    for p in h_particles:
            p.remove()

    for t in trace:
        t.remove()

    trace = [ax.plot(data[:num,i,0], data[:num,i,1], data[:num,i,2], c=colours[i])[0] for i in range(N)]

    h_particles = [ax.plot(*data[num-1:num, i].T, marker='o', c=colours[i],label=solarsystem.planets[i].name, ls='None')[0] for i in range(N)]

    return h_particles, trace

prtcl_ani = animation.FuncAnimation(fig, update_particles, frames=data_len, interval=70, blit=False,repeat=False)

# writergif = animation.PillowWriter(fps=30)
# prtcl_ani.save('filename.gif', writer=writergif)
prtcl_ani.save(save_results_to + "Orbit_Animation.mp4", dpi=450)

# ['black','g','b','gold','y','m','c','r','lime']
"""
