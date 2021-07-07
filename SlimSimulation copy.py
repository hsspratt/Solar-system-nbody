
import numpy as np
from Objects import Objects
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

mpl.rcParams['animation.ffmpeg_path'] = r'/Users/harry/Desktop/Desktop – Harry’s MacBook Pro/Quick N-Body/ffmpeg'

# %% Initialising all the planets, suns and objects that could be used in the simulation

""" Using the objects class to input alol the initial variables and initiliase the planets """

Star1 = Objects('Star1',
                1.1,
                np.array([-0.5,0,0]),
                np.array([0.01,0.01,0]),
                np.array([0,0,0]))

Star2 = Objects('Star2',
               0.907,
               np.array([0.5,0,0]),
               np.array([-0.05,0,-0.1]),
               np.array([0,0,0]))

Star3 = Objects('Star3',
               1.0,
               np.array([0,1,0]),
               np.array([0,-0.01,0]),
               np.array([0,0,0]))

""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""
objects = [Star1, Star2, Star3]
solarsystem = TestSolarSystem(objects)


# %% Define constants
start=time.time()
"""
Defining the constant needed for the calculations. The initial positions and velocities needed to be converted
to m and m/s respectivly as the JPL NASA website provides it in AU and AU/Day. Other constants in clude the time
for the simulation which can be adjusted, and the number of iterations
"""

# Define universal gravitation constant
G = 6.67408e-11

# Reference quantities
# =============================================================================
# au = 149597870.700e3
# v_factor = 1731460
# year_s = 31557600.e0
# =============================================================================

# =============================================================================
# m_nd=1988500e24 #kg #mass of the sun
# r_nd=au #m #distance between stars in Alpha Centauri
# v_nd=30000 #m/s #relative velocity of earth around the sun
# t_nd=1*365*24*3600 #s #orbital period of Alpha Centauri
# =============================================================================

m_nd=1.989e+30 #kg
r_nd=5.326e+12 #m
v_nd=30000 #m/s
t_nd=79.91*365*24*3600*0.51 #s

#Net constants
K1=G*t_nd*m_nd/(r_nd**2*v_nd)
K2=v_nd*t_nd/r_nd

# =============================================================================
# K1=G*t_nd*m_nd/(r_nd**2*v_nd)
# K2=v_nd*t_nd/r_nd
#
# =============================================================================
# Define times
tStart = 0e0
years = 20
iterations = 35000
t_End = years
max_steps = t_End/(iterations)
t=tStart
domain = (t, t_End)

initial = np.full((1, 6), 0, dtype=float)
name = ""
mass = np.full((1, 1), 0, dtype=float)

N = len(objects) # Find the number of objects in the Solar list

planets_initial_non = np.full([N, 6],0, dtype=float)

# Creates an array for all the particles used so that the initial positions and velocities are know
for i in range(len(solarsystem.planets)):
    planets_initial_non[i] = solarsystem.planets[i].init_non

planets_pos = planets_initial_non[:,0:3]
planets_vel = planets_initial_non[:,3:6]

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
three_body_sol = sci.integrate.solve_ivp(fun=Objects.ThreeBodyEquations,t_span=domain,y0=init_params,args=(G,planets_mass,N,K1,K2),max_step=max_steps)
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


for i in range(N):
    r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rcom_sol


# [for i in range(N) r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rearth_sol]

# [x for x in (for i in range(N) r_com_sol[:,i*3:(i+1)*3] = r_sol[:,i*3:(i+1)*3] - rearth_sol)]

colours = ['black','g','b','gold','y','m','c','r','lime']
[plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], color=colours[i], label=solarsystem.planets[i].name) for i in range(N)]; plt.legend()

# #Animate
#Make the figure
fig=plt.figure(figsize=(11,8))
ax=fig.add_subplot(111,projection="3d")

#Create new arrays for animation, this gives you the flexibility
#to reduce the number of points in the animation if it becomes slow
#Currently set to select every 4th point

# =============================================================================
# r1_sol=three_body_sol['y'][0:3,:] # r1_sol=three_body_sol[:,:3]
# r2_sol=three_body_sol['y'][3:6,:] # r2_sol=three_body_sol[:,3:6]
# r3_sol=three_body_sol['y'][6:9,:] # r3_sol=three_body_sol[:,6:9]
# r4_sol=three_body_sol['y'][9:12,:] # r3_sol=three_body_sol[:,6:9]
# r5_sol=three_body_sol['y'][12:15,:] # r3_sol=three_body_sol[:,6:9]
# r6_sol=three_body_sol['y'][15:18,:] # r3_sol=three_body_sol[:,6:9]
# r7_sol=three_body_sol['y'][18:21,:] # r3_sol=three_body_sol[:,6:9]
# r8_sol=three_body_sol['y'][21:24,:] # r3_sol=three_body_sol[:,6:9]
# r9_sol=three_body_sol['y'][24:27,:] # r3_sol=three_body_sol[:,6:9]
#
#
# r1_sol = r1_sol.T
# r2_sol = r2_sol.T
# r3_sol = r3_sol.T
# r4_sol = r4_sol.T
# r5_sol = r5_sol.T
# r6_sol = r6_sol.T
# r7_sol = r7_sol.T
# r8_sol = r8_sol.T
# r9_sol = r9_sol.T
#
# for i in range(N):
# #     r1_sol_anim=r1_sol[::200,:].copy()
#     r2_sol_anim=r2_sol[::5,:].copy()
#     r3_sol_anim=r3_sol[::5,:].copy()
# =============================================================================

end=time.time()
print(end-start)

# %% Analysis

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
# =============================================================================
# PE, KE, angular, linear = np.apply_along_axis(TestSolarSystem.getEnergy, 1, arr=three_body_sol['y'], mass=planets_mass, G=G, N=N)
#
# total_KE = np.sum(KE)
# =============================================================================


total = (np.array([KE])+np.array([PE])).flatten()

# TestSolarSystem.test(solarsystem)

# plt.plot(three_body_sol['t'], L)

t = three_body_sol['t']


plot1 = plt.figure(1)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.KE[1:], colours[i], label=solarsystem.planets[i].name)
    plt.xlabel("Kinetic energy of planets in the solar system")
    plt.ylabel("Kinetic energy (J)")
    plt.legend()
plot1.show()

plot2 = plt.figure(2)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t, planet.PE[1:], colours[i], label=solarsystem.planets[i].name)
    plt.xlabel("Potential energy of planets in the solar system")
    plt.ylabel("Potential energy (J)")
    plt.legend()
plot2.show()

plot3 = plt.figure(3)
plt.plot(t, KE, label="Kinetic energy")
plt.plot(t, PE, label="Potential energy")
plt.plot(t, total, label="Total energy")
plt.xlabel("Total energy of planets in the solar system over time")
plt.ylabel("Energy (J)")
plt.legend()
plot3.show()

plot4 = plt.figure(4)
for i in range(N):
    plt.plot(r_com_sol[:,i*3], r_com_sol[:,1+i*3], colours[i], label=solarsystem.planets[i].name)
    plt.legend()
plot4.show()

plot5 = plt.figure(5)
plt.plot(t, linear)
plt.xlabel("Total linear momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plot5.show()

plot6 = plt.figure(6)
plt.plot(t, angular)
plt.xlabel("Total angular momentum of planets in the solar system over time")
plt.ylabel("")
plt.legend()
plot6.show()


# =============================================================================
# #Set initial marker for planets, that is, blue,red and green circles at the initial positions
# # head1=[ax.scatter(r1_sol_anim[0,0],r1_sol_anim[0,1],r1_sol_anim[0,2],color="darkblue",marker="o",s=100)]
# head2=[ax.scatter(r2_sol_anim[0,0],r2_sol_anim[0,1],r2_sol_anim[0,2],color="tab:red",marker="o",s=100)]
# head3=[ax.scatter(r3_sol_anim[0,0],r3_sol_anim[0,1],r3_sol_anim[0,2],color="tab:green",marker="o",s=100)]
#
# #Create a function Animate that changes plots every frame (here "i" is the frame number)
# def Animate(i,head2,head3):
#     #Remove old markers
# #     head1[0].remove()
#     head2[0].remove()
#     head3[0].remove()
#
#
#     #Plot the orbits (every iteration we plot from initial position to the current position)
# #     trace1=ax.plot(r1_sol_anim[:i,0],r1_sol_anim[:i,1],r1_sol_anim[:i,2],color="darkblue")
#     trace2=ax.plot(r2_sol_anim[:i,0],r2_sol_anim[:i,1],r2_sol_anim[:i,2],color="tab:red")
#     trace3=ax.plot(r3_sol_anim[:i,0],r3_sol_anim[:i,1],r3_sol_anim[:i,2],color="tab:green")
#
#
#     #Plot the current markers
# #     head1[0]=ax.scatter(r1_sol_anim[i-1,0],r1_sol_anim[i-1,1],r1_sol_anim[i-1,2],color="darkblue",marker="o",s=100)
#     head2[0]=ax.scatter(r2_sol_anim[i-1,0],r2_sol_anim[i-1,1],r2_sol_anim[i-1,2],color="tab:red",marker="o",s=100)
#     head3[0]=ax.scatter(r3_sol_anim[i-1,0],r3_sol_anim[i-1,1],r3_sol_anim[i-1,2],color="tab:green",marker="o",s=100)
#
#     return trace2,trace3,head2,head3
#
# #Add a few bells and whistles
# ax.set_xlabel("x-coordinate",fontsize=14)
# ax.set_ylabel("y-coordinate",fontsize=14)
# ax.set_zlabel("z-coordinate",fontsize=14)
# ax.set_xlim([-5e8, 5e8])
# ax.set_ylim([-5e8, 5e8])
# ax.set_zlim([-5e8, 5e8])
# ax.set_title("Visualization of orbits of stars in a N-body system\n",fontsize=14)
#
# #Use the FuncAnimation module to make the animation
# #If used in Jupyter Notebook, animation will not display only a static image will display with this command
# anim=animation.FuncAnimation(fig,Animate,interval=5,repeat=False,blit=False,fargs=(head2,head3),save_count=2000)
#
# # =============================================================================
# # #For Jupyter Notebook, enable to make a Javascript animation
# # matplotlib.rcParams['animation.embed_limit'] = 2**128 #Increase animation embed limit
# # HTML(anim.to_jshtml()) #Convert animation to jsanimation and display
# # =============================================================================
#
# #To save animation to disk, enable this command
# anim.save("ThreeBodyProblem_test.mp4")
#
# print("Writing now")
#
# #To save animation to disk, enable this command
# f = r"/Users/harry/Desktop/Correction Time/ThreeBodyProblem_aroundsun.mp4"
# writermp4 = animation.FFMpegWriter(fps=60)
# anim.save(f, writer=writermp4)
#
# print("done writing")
# =============================================================================
# %%
start=time.time()
# #Animate
#Make the figure
fig=plt.figure(7, figsize=(10,7))
ax=fig.add_subplot(111,projection="3d")

#Create new arrays for animation, this gives you the flexibility
#to reduce the number of points in the animation if it becomes slow
#Currently set to select every 4th point

# =============================================================================
# for i in range(N):
#     r_sol_anim = r_sol[::12,:].copy
# =============================================================================
r1_sol_anim=r1_sol[::1,:].copy()
r2_sol_anim=r2_sol[::1,:].copy()
r3_sol_anim=r3_sol[::1,:].copy()


#Set initial marker for planets, that is, blue,red and green circles at the initial positions
head1=[ax.scatter(r1_sol_anim[0,0],r1_sol_anim[0,1],r1_sol_anim[0,2],color="darkblue",marker="o",s=100,label="Sun")]
head2=[ax.scatter(r2_sol_anim[0,0],r2_sol_anim[0,1],r2_sol_anim[0,2],color="tab:red",marker="o",s=100,label="Earth")]
head3=[ax.scatter(r3_sol_anim[0,0],r3_sol_anim[0,1],r3_sol_anim[0,2],color="tab:green",marker="o",s=100,label="Mars")]

#Create a function Animate that changes plots every frame (here "i" is the frame number)
def Animate(i,head1,head2,head3):
    #Remove old markers
    head1[0].remove()
    head2[0].remove()
    head3[0].remove()


    #Plot the orbits (every iteration we plot from initial position to the current position)
    trace1=ax.plot(r1_sol_anim[:i,0],r1_sol_anim[:i,1],r1_sol_anim[:i,2],color="darkblue",label="Sun")
    trace2=ax.plot(r2_sol_anim[:i,0],r2_sol_anim[:i,1],r2_sol_anim[:i,2],color="tab:red",label="Earth")
    trace3=ax.plot(r3_sol_anim[:i,0],r3_sol_anim[:i,1],r3_sol_anim[:i,2],color="tab:green",label="Mars")


    #Plot the current markers
    head1[0]=ax.scatter(r1_sol_anim[i-1,0],r1_sol_anim[i-1,1],r1_sol_anim[i-1,2],color="darkblue",marker="o",s=100,label="Sun")
    head2[0]=ax.scatter(r2_sol_anim[i-1,0],r2_sol_anim[i-1,1],r2_sol_anim[i-1,2],color="tab:red",marker="o",s=100,label="Earth")
    head3[0]=ax.scatter(r3_sol_anim[i-1,0],r3_sol_anim[i-1,1],r3_sol_anim[i-1,2],color="tab:green",marker="o",s=100,label="Mars")

    return trace1,trace2,trace3,head1,head2,head3

#Add a few bells and whistles
ax.set_xlabel("x-coordinate",fontsize=14)
ax.set_ylabel("y-coordinate",fontsize=14)
ax.set_zlabel("z-coordinate",fontsize=14)
ax.set_box_aspect([1,1,1])
ax.set_title("Visualization of orbits of stars in a N-body system",fontsize=14)

anim=animation.FuncAnimation(fig,Animate, save_count=2000, repeat=False,blit=False,fargs=(head1,head2,head3))


#To save animation to disk, enable this command
# anim.save("ThreeBodyProblem_test.mp4")

print("Writing now")

#To save animation to disk, enable this command
f = r"/Users/harry/Desktop/Desktop – Harry’s MacBook Pro/Quick N-Body/NBodyProblem_shortperiod.mp4"
writermp4 = animation.FFMpegWriter(fps=60)
anim.save(f, writer=writermp4, dpi=400)
end = time.time()
print("done writing, time is : ", end-start)

# %%

fig=plt.figure(figsize=(15,15))
ax=fig.add_subplot(111,projection="3d")
ax.plot(r1_sol[:,0],r1_sol[:,1],r1_sol[:,2],color="darkblue")
ax.plot(r2_sol[:,0],r2_sol[:,1],r2_sol[:,2],color="tab:red")
ax.plot(r3_sol[:,0],r3_sol[:,1],r3_sol[:,2],color="tab:green")
ax.scatter(r1_sol[-1,0],r1_sol[-1,1],r1_sol[-1,2],color="darkblue",marker="o",s=100,label="Alpha Centauri A")
ax.scatter(r2_sol[-1,0],r2_sol[-1,1],r2_sol[-1,2],color="tab:red",marker="o",s=100,label="Alpha Centauri B")
ax.scatter(r3_sol[-1,0],r3_sol[-1,1],r3_sol[-1,2],color="tab:green",marker="o",s=100,label="Alpha Centauri B")
ax.set_xlabel("\nx-coordinate",fontsize=14)
ax.set_ylabel("\ny-coordinate",fontsize=14)
ax.set_zlabel("\nz-coordinate",fontsize=14)
ax.set_title("Visualization of orbits of stars in a two-body system from \n",fontsize=14)
ax.legend(loc="upper left",fontsize=14)


