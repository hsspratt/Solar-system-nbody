# %%
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy import interpolate
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
import n_body_app
import copy
plt.rc('mathtext', fontset="cm")


# %% Initialising all the planets, suns and objects that could be used in the simulation

""" Using the objects class to input all the initial variables and initiliase the planets """

au = 149597870.700e3
v_factor = 1731460

Sun = Objects('Sun',
              1988500e24,
              au*np.array([-6.534087946884256E-03,
                       6.100454846284101E-03, 1.019968145073305E-04]),
              v_factor*np.array([-6.938967653087248E-06, -
                       5.599052606952444E-06, 2.173251724105919E-07]),
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


root = tk.Tk()
root.title("N Body Simulation")
root.geometry('400x300')
app = n_body_app.n_body_app(root)
root.mainloop()

planets = app.planets

print(planets)
objects = []

x = [F8_1, F8_2, F8_3, AC1, AC2, Sun,  Mercury, Venus,
     Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

for i in range(len(x)):
    if str(x[i].name) in planets:
        objects.append(x[i])


""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""
# objects = planets
# [Sun, Earth, Mars, Venus, Mercury] # , Jupiter,Saturn,Neptune,Uranus]
# objects = [Sun, Earth, Venus, Uranus, Neptune, Saturn, Mercury, Mars, Jupiter]
solarsystem = TestSolarSystem(objects)


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

m_nd = 1.989e+30  # kg #mass of the sun
r_nd = 5.326e+12  # m #distance between stars in Alpha Centauri
v_nd = 30000  # m/s #relative velocity of earth around the sun
t_nd = 79.91*365*24*3600*0.51  # s #orbital period of Alpha Centauri

if app.K.get() == 1:
    K1=G*t_nd*m_nd/(r_nd**2*v_nd)
    K2=v_nd*t_nd/r_nd
else:
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

r_com_sol = np.empty((iterations,N*3))

for i in range(N):
    r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rcom_sol

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
plotKE.savefig('planets_KE.png', bbox_inches='tight')
# plotKE.clf()

plotPE = plt.figure(2)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.PE[1:], colours[i], label=solarsystem.planets[i].name)
    plt.xlabel("Potential energy of planets in the solar system")
    plt.ylabel("Potential energy (J)")
    plt.legend()
    plotKE.show()
plotPE.show()
plotPE.savefig('planets_PE.png', bbox_inches='tight')
# plotPE.clf()

plotTotal = plt.figure(3)
plt.plot(t, KE, label="Kinetic energy")
plt.plot(t, PE, label="Potential energy")
plt.plot(t, total, label="Total energy")
plt.xlabel("Total energy of planets in the solar system over time")
plt.ylabel("Energy (J)")
plt.legend()
plotTotal.show()
plotTotal.savefig('Total_Energy_System.png', bbox_inches='tight')
# plotTotal.clf()

plotOrbits = plt.figure(4)
for i in range(N):
    plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], colours[i], label=solarsystem.planets[i].name)
    plt.legend()
plotOrbits.show()
plotOrbits.savefig('Orbits_System.png', bbox_inches='tight')
# plotOrbits.clf()

plotLm = plt.figure(5)
plt.plot(t, linear)
plt.xlabel("Total linear momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plotLm.show()
plotLm.savefig('Linear_Momentum_System.png', bbox_inches='tight')
# plotLm.clf()

plotAm = plt.figure(6)
plt.plot(t, angular)
plt.xlabel("Total angular momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plotAm.show()
plotAm.savefig('Angular_Momentum_System.png', bbox_inches='tight')
# plotAm.clf()

end = time.time()

print("Time for calculating enrgy and plotting is:   " , end-start)


total_off = ((total-total[0])/total)*100
total_cor = [i for i in total_off if i >= 1]

if len(total_cor) == 0:
    print("This orbit looks stable. The change in error from the beginiing to end is: ", total_off[-1],"%")
else:
    print("The stablility of the orbit seems to be only valid up till the ", len(total_cor), " time step")


# %%
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc

fig, ax = plt.subplots()

line, = ax.plot(r_sol[:,0], r_sol[:,1], "-")
line1, = ax.plot(r_sol[0,0], r_sol[0,1], "ro")
line2, = ax.plot(r_sol[0,3], r_sol[0,4], "bo")
line3, = ax.plot(r_sol[0,6], r_sol[0,7], "go")

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
"""
# %%
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import matplotlib as mpl
import random
mpl.rcParams['animation.ffmpeg_path'] = r'/Users/harry/Documents/GitHub/N-Body-Simulation-Summer/ffmpeg'

# h = np.full((N*3,iterations),0)
h = np.empty((iterations, N, 3))

for i in range(3):
    h[:,:,i] = r_sol[:,i::3]

data = h

fig = plt.figure()
# fig = plt.figure(figsize=plt.figaspect(1)*2)

ax = p3.Axes3D(fig)
# ax.set_box_aspect([1,1,1])
# ax = plt.gca(projection='3d', proj_type = 'ortho')

# Plot the first position for all particles
#h = ax.plot(*data[0].T, marker='.', linestyle='None')[0]
# Equivalent to
# h = ax.plot(data[0, :, 0], data[0, :, 1], data[0, :, 2],
#             marker='.', linestyle='None')[0]

# Setting the axes properties
ax.set_xlim3d([-1.5, 1.5])
ax.set_xlabel('X')

ax.set_ylim3d([-1, 1])
ax.set_ylabel('Y')

ax.set_zlim3d([-0.5, 0.5])
ax.set_zlabel('Z')
ax.set_title('3D Test')

colormap = plt.cm.tab20c
colors = [colormap(i) for i in np.linspace(0, 1, N)]
h_particles = [ax.plot(*data[:1, i].T, marker='o', c=colors[i], ls='None')[0]
               for i in range(N)]

h_particles = [ax.plot(*data[0:, i].T, marker='o', c=colors[i], ls='None')[0] for i in range(N)]


def update_particles(num):

    for i, h in enumerate(h_particles):

        # h_particles[i].remove()

        # trace = [ax.plot(*data[:num, i].T, maker='-', c=colors[i], ls='None') for i in range(N)]

        # h_particles[i][0] = [ax.plot(*data[:num-1, i].T, marker='.', c=colors[i], ls='None')[0] for i in range(N)]

        h.set_xdata(data[num-5:num, i, 0])
        h.set_ydata(data[num-5:num, i, 1])
        h.set_3d_properties(data[num-5:num, i, 2])
    return h_particles, trace

prtcl_ani = animation.FuncAnimation(fig, update_particles, frames=301, interval=10)
"""
# %%
"""
# data
measured_time = t
measures = r_com_sol

# Interpolate it to new time points
linear_interp = [None]*3*N

for i in range(3*N):
    linear_interp = interp1d(measured_time, measures[:,i])
    
# linear_interp = interp1d(measured_time, measures)
interpolation_time = np.linspace(0, t_End, iterations)
linear_results = np.empty([iterations, 3*N])

for i in range(3*N):
    linear_results = linear_interp(interpolation_time)[i]
    
# cubic_interp = interp1d(measured_time, measures, kind='cubic')
# cubic_results = cubic_interp(interpolation_time)

# Plot the data and the interpolation
plt.figure(figsize=(6, 4))
plt.plot(measured_time, measures, 'o', ms=6, label='measures')
plt.plot(interpolation_time, linear_results, label='linear interp')
plt.plot(interpolation_time, cubic_results, label='cubic interp')
plt.legend()
plt.show()
"""
# %%

anim_r_com_sol = r_com_sol[0::1,:].copy()
data_len = anim_r_com_sol.shape[0]

x = np.array(range(anim_r_com_sol.shape[0]))

# define new x range, we need 7 equally spaced values
xnew = np.linspace(x.min(), x.max(), 9)

# apply the interpolation to each column
f = interp1d(x, anim_r_com_sol, axis=0)

# get final result
print(f(xnew))

# %%

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import matplotlib as mpl
import subprocess


data = np.empty((data_len, N, 3))

for i in range(3):
    data[:,:,i] = anim_r_com_sol[:,i::3]

fig = plt.figure()

ax = p3.Axes3D(fig)
# ax.set_xlim3d([-1.5, 1.5])
ax.set_xlabel('X')

# ax.set_ylim3d([-1, 1])
ax.set_ylabel('Y')

# ax.set_zlim3d([-0.5, 0.5])
ax.set_zlabel('Z')
ax.set_title('3D Test')

cm = plt.cm.get_cmap('tab10')
colours = cm.colors


h_particles = [ax.plot(*data[:1, i].T, marker='o', c=colours[i], ls='None')[0] for i in range(N)]
trace = [ax.plot(data[:1,i,0], data[:1,i,1], data[:1,i,2], c=colours[i])[0] for i in range(N)]

def update_particles(num):
    print(num, " out of ", iterations)
    global h_particles
    global trace

    for p in h_particles:
            p.remove()

    for t in trace:
        t.remove()

    trace = [ax.plot(data[:num,i,0], data[:num,i,1], data[:num,i,2], c=colours[i])[0] for i in range(N)]

    h_particles = [ax.plot(*data[num-1:num, i].T, marker='o', c=colours[i], ls='None')[0] for i in range(N)]

    return h_particles, trace

prtcl_ani = animation.FuncAnimation(fig, update_particles, frames=data_len, interval=1, blit=False,repeat=False)

prtcl_ani.save("Failedmp4_1.mp4", dpi=450)


# %%
"""
import matplotlib.pyplot as plt

fig = plt.figure()

plt.xlim(-10,10)
plt.ylim(-10,10)

#step 1: background blue dot
plt.plot(0,0,marker='o',color='b')

#step 2: additional black dots
points_list = [(1,2),(3,4),(5,6)]
for point in points_list:
    plt.plot(point[0],point[1],marker='o',color='k')
"""
# %%
"""
kind = ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next']
fig = plt.figure()
ax = fig.subplots()
x = np.linspace(0, 100,10)
y = 3*x**2 - np.exp(0.1*x)
x_new = np.linspace(0, 100, 100)

for i in kind:
    #interpolation step
    f = interpolate.interp1d(x, y, kind = i)
      #y array that contains the interpolated data points
    y_interp = f(x_new)
    ax.plot(x_new, y_interp, alpha = 0.5, label = i)
ax.scatter(x,y)
plt.legend()
plt.show()
"""
# %%

