# %%
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
plt.rc('mathtext', fontset="cm")
# %% Initialising all the planets, suns and objects that could be used in the simulation

""" Using the objects class to input all the initial variables and initiliase the planets """

au = 149597870.700e3
v_factor = 1731460

Sun = Objects('Sun',
              1988500e24,
              au*np.array([-6.534087946884256E-03,
                       6.100454846284101E-03, 1.019968145073305E-04]),
              v_factor*np.array([-2.499218584280511E-03,
                          2.877287547390077E-03, 4.308752491196167E-05]),
              np.array([0, 0, 0]))

Another_Sun = Objects('Another_Sun',
              1988500e24,
                      2*au*np.array([1.538595512099490E+01,
                                   1.241875975077764E+01, -1.532033630108008E-01]),
                      2*v_factor*np.array([-2.499218584280511E-03,
                                         2.877287547390077E-03, 4.308752491196167E-05]),
              np.array([0, 0, 0]))

Earth = Objects('Earth',
                5.97219e24,
                au*np.array([1.103149414301009E-01,
                         9.834091037591375E-01, 5.617876135133732E-05]),
                v_factor*np.array([-1.737759726478284E-02,
                         1.972610167033268E-03, 8.664696160974217E-07]),
                np.array([0, 0, 0]))

Moon = Objects('Moon',
               7.349e22,
               au*np.array([1.102098327438270E-01,
                        9.809689058999859E-01, 2.529448125222282E-05]),
               v_factor*np.array([-1.675883798190850E-02,
                        1.924205370134019E-03, -5.631205054459148E-05]),
               np.array([0, 0, 0]))

Jupiter = Objects('Jupiter',
                  1898.13e24,
                  au*np.array([2.932487231769548E+00, -
                           4.163444383137574E+00, -4.833604407653648E-02]),
                  v_factor*np.array([6.076788230491844E-03,
                           4.702729516645153E-03, -1.554436340872727E-04]),
                  np.array([0, 0, 0]))

Mars = Objects('Mars',
               6.4171e23,
               au*np.array([8.134621210079180E-01,
                        1.246863741423589E+00, 5.988005015395813E-03]),
               v_factor*np.array([-1.115056230684616E-02,
                        8.900864244780916E-03, 4.602296502333571E-04]),
               np.array([0, 0, 0]))

Venus = Objects('Venus',
                48.685e23,
                au*np.array([-6.617430552711726E-01, -
                         2.949635370329196E-01, 3.377990088634703E-02]),
                v_factor*np.array([8.298887450533079E-03, -
                         1.847842625652145E-02, -7.325856707752017E-04]),
                np.array([0, 0, 0]))

Mercury = Objects('Mercury',
                  3.302e23,
                  au*np.array([-1.327900416813791E-01, -
                           4.423196833692000E-01, -2.495947572187113E-02]),
                  v_factor*np.array([2.142560067381590E-02, -
                           6.223078359939026E-03, -2.473884150860611E-03]),
                  np.array([0, 0, 0]))

Saturn = Objects('Saturn',
                 5.6834e26,
                 au*np.array([5.409527551219896E+00, -
                          8.387647661909122E+00, -6.952095229728303E-02]),
                 v_factor*np.array([4.377905875627875E-03,
                          3.010222250503800E-03, -2.269189986953596E-04]),
                 np.array([0, 0, 0]))

Neptune = Objects('Neptune',
                  5.6834e26,
                  au*np.array([5.409527551219896E+00, -
                           8.387647661909122E+00, -6.952095229728303E-02]),
                  v_factor*np.array([4.377905875627875E-03,
                           3.010222250503800E-03, -2.269189986953596E-04]),
                  np.array([0, 0, 0]))

Uranus = Objects('Uranus',
                 86.813e24,
                 au*np.array([1.538595512099490E+01,
                          1.241875975077764E+01, -1.532033630108008E-01]),
                 v_factor*np.array([-2.499218584280511E-03,
                          2.877287547390077E-03, 4.308752491196167E-05]),
                 np.array([0, 0, 0]))

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

Objects_I_pos = [-1, 0, 0]
Objects_II_pos = [1, 0, 0]
Objects_III_pos = [0, 0, 0]


butterfly_I  = [0.30689, 0.12551, 0, 6.2356]
butterfly_II = [0.39295, 0.09758, 0, 7.0039]
bumblebee = [0.18428, 0.58719, 0, 63.5345]
moth_I = [0.46444, 0.39606, 0, 14.8939]
moth_II = [0.43917, 0.45297, 0, 28.6703]
butterfly_III = [0.40592, 0.23016, 0, 13.8658]
moth_III = [0.38344, 0.37736, 0, 25.8406]
goggles = [0.08330, 0.12789, 0, 10.4668]
butterfly_IV = [0.350112, 0.07934, 0, 79.4759]
dragonfly = [0.08058, 0.58884, 0, 21.2710]
yarn = [0.55906, 0.34919, 55.5018]
yin_yang_I_a = [0.51394, 0.30474, 0, 17.3284]
yin_yang_I_b = [0.28270, 0.32721, 0, 10.9626]
yin_yang_II_a = [0.41682, 0.33033, 0, 55.7898]
yin_yang_II_b = [0.41734, 0.31310, 0, 54.2076]


Butterfly_I_1 = Objects('Butterfly I - Planet 1',
                        1,
                        np.array(Objects_I_pos),
                        np.array([butterfly_I[0], butterfly_I[1], butterfly_I[2]]),
                        np.array([0, 0, 0]))

Butterfly_I_2 = Objects('Butterfly I - Planet 2',
                        1,
                        np.array(Objects_II_pos),
                        np.array([butterfly_I[0], butterfly_I[1], butterfly_I[2]]),
                        np.array([0, 0, 0]))

Butterfly_I_3 = Objects('Butterfly I - Planet 3',
                        1,
                        np.array(Objects_III_pos),
                        np.array([-2*butterfly_I[0], -2*butterfly_I[1], butterfly_I[2]]),
                        np.array([0, 0, 0]))

Butterfly_II_1 = Objects('Butterfly II - Planet 1',
                        1,
                        np.array(Objects_I_pos),
                        np.array([butterfly_II[0], butterfly_II[1], butterfly_II[2]]),
                        np.array([0, 0, 0]))

Butterfly_II_2 = Objects('Butterfly II - Planet 2',
                        1,
                        np.array(Objects_II_pos),
                        np.array([butterfly_II[0], butterfly_II[1], butterfly_II[2]]),
                        np.array([0, 0, 0]))

Butterfly_II_3 = Objects('Butterfly II - Planet 3',
                        1,
                        np.array(Objects_III_pos),
                        np.array([-2*butterfly_II[0],-2*butterfly_II[1], butterfly_II[2]]),
                        np.array([0, 0, 0]))

Butterfly_III_1 = Objects('Butterfly III - Planet 1',
                        1,
                        np.array(Objects_I_pos),
                        np.array([butterfly_III[0], butterfly_III[1], butterfly_III[2]]),
                        np.array([0, 0, 0]))

Butterfly_III_2 = Objects('Butterfly III - Planet 2',
                        1,
                        np.array(Objects_II_pos),
                        np.array([butterfly_III[0], butterfly_III[1], butterfly_III[2]]),
                        np.array([0, 0, 0]))

Butterfly_III_3 = Objects('Butterfly III - Planet 3',
                        1,
                        np.array(Objects_III_pos),
                        np.array([-2*butterfly_III[0],-2*butterfly_III[1], butterfly_III[2]]),
                        np.array([0, 0, 0]))

bumblebee_1 = Objects('bumblebee I - Planet 1',
                        1,
                        np.array(Objects_I_pos),
                        np.array([bumblebee[0], bumblebee[1], bumblebee[2]]),
                        np.array([0, 0, 0]))

bumblebee_2 = Objects('bumblebee I - Planet 2',
                         1,
                         np.array(Objects_II_pos),
                         np.array([bumblebee[0], bumblebee[1], bumblebee[2]]),
                         np.array([0, 0, 0]))

bumblebee_3 = Objects('bumblebee I - Planet 3',
                        1,
                        np.array(Objects_III_pos),
                        np.array([-2*bumblebee[0], -2*bumblebee[1], bumblebee[2]]),
                        np.array([0, 0, 0]))

moth_I_1 = Objects('moth I - Planet 1',
                      1,
                      np.array(Objects_I_pos),
                      np.array([moth_I[0], moth_I[1], moth_I[2]]),
                      np.array([0, 0, 0]))

moth_I_2 = Objects('moth I - Planet 2',
                      1,
                      np.array(Objects_II_pos),
                      np.array([moth_I[0], moth_I[1], moth_I[2]]),
                      np.array([0, 0, 0]))

moth_I_3 = Objects('moth I - Planet 3',
                      1,
                      np.array(Objects_III_pos),
                      np.array([-2*moth_I[0], -2*moth_I[1], moth_I[2]]),
                      np.array([0, 0, 0]))

moth_II_1 = Objects('moth II - Planet 1',
                   1,
                   np.array(Objects_I_pos),
                   np.array([moth_II[0], moth_II[1], moth_II[2]]),
                   np.array([0, 0, 0]))

moth_II_2 = Objects('moth II - Planet 2',
                   1,
                   np.array(Objects_II_pos),
                   np.array([moth_II[0], moth_II[1], moth_II[2]]),
                   np.array([0, 0, 0]))

moth_II_3 = Objects('moth II - Planet 3',
                   1,
                   np.array(Objects_III_pos),
                   np.array([-2*moth_II[0], -2*moth_II[1], moth_II[2]]),
                   np.array([0, 0, 0]))

moth_III_1 = Objects('moth III - Planet 1',
                   1,
                   np.array(Objects_I_pos),
                   np.array([moth_III[0], moth_III[1], moth_III[2]]),
                   np.array([0, 0, 0]))

moth_III_2 = Objects('moth III - Planet 2',
                   1,
                   np.array(Objects_II_pos),
                   np.array([moth_III[0], moth_III[1], moth_III[2]]),
                   np.array([0, 0, 0]))

moth_III_3 = Objects('moth III - Planet 3',
                   1,
                   np.array(Objects_III_pos),
                   np.array([-2*moth_III[0], -2*moth_III[1], moth_III[2]]),
                   np.array([0, 0, 0]))

Butterfly_I = [Butterfly_I_1, Butterfly_I_2, Butterfly_I_3]
Butterfly_II = [Butterfly_II_1, Butterfly_II_2, Butterfly_II_3]
Butterfly_III = [Butterfly_III_1, Butterfly_III_2, Butterfly_III_3]
bumblebee = [bumblebee_1, bumblebee_2, bumblebee_3]
moth_I = [moth_I_1, moth_I_2, moth_I_3]
moth_II = [moth_II_1, moth_II_2, moth_II_3]
moth_III = [moth_III_1, moth_III_2, moth_III_3]

root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')
app = n_body_app.n_body_app(root)
root.mainloop()


planets = app.planets

print(planets)
objects = []

x = [F8_1, F8_2, F8_3, F8_planet, AC1, AC2, AC_star, Sun,  Mercury, Venus,
     Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Another_Sun, Butterfly_I, Butterfly_II,
     Butterfly_III, moth_I, moth_II, moth_III, bumblebee]
try:
    for i in range(len(x)):
        if str(x[i].name) in planets:
            objects.append(x[i])
except AttributeError:
    if planets == ['Butterfly_I']:
        objects = Butterfly_I
    if planets == ['Butterfly_II']:
        objects = Butterfly_III
    if planets == ['Butterfly_III']:
        objects = Butterfly_III
    if planets == ['moth_I']:
        objects = moth_I
    if planets == ['moth_II']:
        objects = moth_II
    if planets == ['moth_III']:
        objects = moth_III
    if planets == ['bumblebee']:
        objects = bumblebee
    else:
        print("Planets could not be initiallised")

""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""
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

# rtol = float(app.rtol.get())
# atol = float(app.rtol.get())

# ## Run the solve_ivp solver
three_body_sol = sci.integrate.solve_ivp(fun=Objects.ThreeBodyEquations,t_span=domain,y0=init_params,args=(G,planets_mass,N,K1,K2), max_step=max_steps) # rtol=rtol, atol=atol
t = three_body_sol['t']
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

r_com_sol = np.empty((iterations,N*3))

for i in range(N):
    r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rcom_sol

g = np.hstack((rcom_sol, rcom_sol,rcom_sol))

# cm = plt.cm.get_cmap('tab10')
# colours = cm.colors


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


colours = ['black','g','b','gold','y','m','c','r','lime','navy']

for col in range(iterations):
    sol = three_body_sol['y'][:,col]
    temp_PE, temp_KE, temp_angular, temp_linear = SolarSystem.getEnergy(solarsystem, sol, planets_mass, G, N)
    KE.append(temp_KE)
    PE.append(temp_PE)
    angular.append(temp_angular)
    linear.append(temp_linear)

total = (np.array([KE])+np.array([PE])).flatten()

plotKE = plt.figure(1)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.KE[1:], colours[i], label=solarsystem.planets[i].name)
    plt.xlabel("Kinetic energy of planets in the solar system")
    plt.ylabel("Kinetic energy (J)")
    plt.legend()
plotKE.show()
plotKE.savefig('planets_KE.png', bbox_inches='tight')

plotPE = plt.figure(2)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.PE[1:], (colours)[i], label=solarsystem.planets[i].name)
    plt.xlabel("Potential energy of planets in the solar system")
    plt.ylabel("Potential energy (J)")
    plt.legend()
    plotKE.show()
plotPE.show()
plotPE.savefig('planets_PE.png', bbox_inches='tight')

plotTotal = plt.figure(3)
plt.plot(t, KE, label="Kinetic energy")
plt.plot(t, PE, label="Potential energy")
plt.plot(t, total, label="Total energy")
plt.xlabel("Total energy of planets in the solar system over time")
plt.ylabel("Energy (J)")
plt.legend()
plotTotal.show()
plotTotal.savefig('Total_Energy_System.png', bbox_inches='tight')

plotOrbits = plt.figure(4)
for i in range(N):
    plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], (colours)[i], label=solarsystem.planets[i].name)
    plt.legend()
plotOrbits.show()
plotOrbits.savefig('Orbits_System.png', bbox_inches='tight')

plotEarth = plt.figure(10)
plt.plot(r_com_sol[:,0], r_com_sol[:,1+0])
plt.plot(r_com_sol[:,3], r_com_sol[:,1+3])
plt.legend()
plotEarth.show()
plotOrbits.savefig('Orbits_System.png', bbox_inches='tight')

plotLm = plt.figure(5)
plt.plot(t, linear)
plt.xlabel("Total linear momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plotLm.show()
plotLm.savefig('Linear_Momentum_System.png', bbox_inches='tight')

plotAm = plt.figure(6)
plt.plot(t, angular)
plt.xlabel("Total angular momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plotAm.show()
plotAm.savefig('Angular_Momentum_System.png', bbox_inches='tight')

# threeD_plot = plt.figure(7)
threeD_plot = plt.figure(figsize=plt.figaspect(1)*2)

# ax = p3.Axes3D(threeD_plot)
ax = threeD_plot.gca(projection='3d', proj_type = 'ortho')
line = [ax.plot(r_com_sol[:,i*3], r_com_sol[:,i*3+1], r_com_sol[:,i*3+2], c=(colours)[i])[0] for i in range(N)]
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
ax.set_zlim([-3e12,3e12])
ax.set_title("Static 3D Orbit")
ax.legend()
threeD_plot.show()
threeD_plot.savefig('3D static plot.png', bbox_inches='tight')

end = time.time()

print("Time for calculating enrgy and plotting is:   " , end-start)

"""Crudely evaluates when the orbit and physics is no longer valid"""

total_off = ((total-total[0])/total)*100
total_cor = [i for i in total_off if i >= 1]

if len(total_cor) == 0:
    print("This orbit looks stable. The change in error from the beginiing to end is: ", total_off[-1],"%")
else:
    print("The stablility of the orbit seems to be only valid up till the ", len(total_cor), " time step")

# %%

cm = plt.cm.get_cmap('tab10')
colours = cm.colors

anim_r_com_sol = r_com_sol[0::2,:].copy()
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

prtcl_ani.save("Orbit_Animation.mp4", dpi=450)

# ['black','g','b','gold','y','m','c','r','lime']

# %%
