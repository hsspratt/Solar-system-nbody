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
mpl.rcParams['animation.ffmpeg_path'] = r'/Users/harry/Desktop/Desktop – Harry’s MacBook Pro/Quick N-Body/ffmpeg'

# %% Initialising all the planets, suns and objects that could be used in the simulation

""" Using the objects class to input alol the initial variables and initiliase the planets """

au = 149597870.700e3
v_factor = 1731460
maxint = (4*au)**(1/2)

Sun = Objects('Sun',
              1988500e24,
              np.array([-6.534087946884256E-03, 6.100454846284101E-03, 1.019968145073305E-04]),
              np.array([-6.938967653087248E-06, -5.599052606952444E-06, 2.173251724105919E-07]),
              np.array([0,0,0]))

Earth = Objects('Earth',
                5.97219e24,
                np.array([1.103149414301009E-01, 9.834091037591375E-01, 5.617876135133732E-05]),
                np.array([-1.737759726478284E-02, 1.972610167033268E-03, 8.664696160974217E-07]),
                np.array([0,0,0]))

Moon = Objects('Moon',
                7.349e22,
                np.array([1.102098327438270E-01, 9.809689058999859E-01, 2.529448125222282E-05]),
                np.array([-1.675883798190850E-02, 1.924205370134019E-03, -5.631205054459148E-05]),
                np.array([0,0,0]))

Jupiter = Objects('Jupiter',
                  1898.13e24,
                  np.array([2.932487231769548E+00, -4.163444383137574E+00, -4.833604407653648E-02]),
                  np.array([6.076788230491844E-03, 4.702729516645153E-03, -1.554436340872727E-04]),
                  np.array([0,0,0]))

Mars = Objects('Mars',
               6.4171e23,
               np.array([8.134621210079180E-01, 1.246863741423589E+00, 5.988005015395813E-03]),
               np.array([-1.115056230684616E-02, 8.900864244780916E-03, 4.602296502333571E-04]),
               np.array([0,0,0]))

Venus = Objects('Venus',
               48.685e23,
               np.array([-6.617430552711726E-01, -2.949635370329196E-01, 3.377990088634703E-02]),
               np.array([8.298887450533079E-03, -1.847842625652145E-02, -7.325856707752017E-04]),
               np.array([0,0,0]))

Mercury = Objects('Mercury',
               3.302e23,
               np.array([-1.327900416813791E-01, -4.423196833692000E-01, -2.495947572187113E-02]),
               np.array([2.142560067381590E-02, -6.223078359939026E-03, -2.473884150860611E-03]),
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

star1 = Objects('Star1',
                (5/3)*5e28,
                np.array([1.103149414301009E-01, 9.834091037591375E-01, 5.617876135133732E-05]),
                np.array([-1.737759726478284E-02, 1.972610167033268E-03, 8.664696160974217E-07]),
                np.array([0,0,0]))

Star2 = Objects('Star2',
               (4/3)*5e27,
               np.array([1.538595512099490E+01, 1.241875975077764E+01, -1.532033630108008E-01]),
               np.array([-2.499218584280511E-03, 2.877287547390077E-03, 4.308752491196167E-05]),
               np.array([0,0,0]))

Star3 = Objects('Star3',
               (5/3)*5e27,
               np.array([-6.617430552711726E-01, -2.949635370329196E-01, 3.377990088634703E-02]),
               np.array([8.298887450533079E-03, -1.847842625652145E-02, -7.325856707752017E-04]),
               np.array([0,0,0]))

""" Defining the list of planets which will be used in the simulation, only the above objects can be placed in"""

objects = Planets# [Sun, Mars, Venus, Mercury, Earth] # [Sun, Earth, Mars, Venus, Mercury] # , Jupiter,Saturn,Neptune,Uranus]
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
au = 149597870.700e3
v_factor = 1731460
year_s = 31557600.e0

# Define times
tStart = 0e0
years = 350
iterations = 31500
t_End = years*year_s
max_steps = t_End/iterations
t=tStart
domain = (t, t_End)

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
three_body_sol = sci.integrate.solve_ivp(fun=Objects.ThreeBodyEquations,t_span=domain,y0=init_params,args=(G,planets_mass,N), max_step=max_steps)
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

r1_sol=three_body_sol['y'][0:3,:] # r1_sol=three_body_sol[:,:3]
r2_sol=three_body_sol['y'][3:6,:] # r2_sol=three_body_sol[:,3:6]
r3_sol=three_body_sol['y'][6:9,:] # r3_sol=three_body_sol[:,6:9]
r4_sol=three_body_sol['y'][9:12,:] # r3_sol=three_body_sol[:,6:9]
r5_sol=three_body_sol['y'][12:15,:] # r3_sol=three_body_sol[:,6:9]
r6_sol=three_body_sol['y'][15:18,:] # r3_sol=three_body_sol[:,6:9]
r7_sol=three_body_sol['y'][18:21,:] # r3_sol=three_body_sol[:,6:9]
r8_sol=three_body_sol['y'][21:24,:] # r3_sol=three_body_sol[:,6:9]
r9_sol=three_body_sol['y'][24:27,:] # r3_sol=three_body_sol[:,6:9]


r1_sol = r1_sol.T
r2_sol = r2_sol.T
r3_sol = r3_sol.T
r4_sol = r4_sol.T
r5_sol = r5_sol.T
r6_sol = r6_sol.T
r7_sol = r7_sol.T
r8_sol = r8_sol.T
r9_sol = r9_sol.T

for i in range(N):
#     r1_sol_anim=r1_sol[::200,:].copy()
    r2_sol_anim=r2_sol[::5,:].copy()
    r3_sol_anim=r3_sol[::5,:].copy()

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
start=time.time()
# #Animate
#Make the figure
fig=plt.figure(7, figsize=(11,8))
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
r4_sol_anim=r4_sol[::1,:].copy()
r5_sol_anim=r5_sol[::1,:].copy()
r6_sol_anim=r6_sol[::1,:].copy()
r7_sol_anim=r7_sol[::1,:].copy()
r8_sol_anim=r8_sol[::1,:].copy()
r9_sol_anim=r9_sol[::1,:].copy()

#Set initial marker for planets, that is, blue,red and green circles at the initial positions
head1=[ax.scatter(r1_sol_anim[0,0],r1_sol_anim[0,1],r1_sol_anim[0,2],color="darkblue",marker="o",s=100,label="Sun")]
head2=[ax.scatter(r2_sol_anim[0,0],r2_sol_anim[0,1],r2_sol_anim[0,2],color="tab:red",marker="o",s=100,label="Earth")]
head3=[ax.scatter(r3_sol_anim[0,0],r3_sol_anim[0,1],r3_sol_anim[0,2],color="tab:green",marker="o",s=100,label="Mars")]
head4=[ax.scatter(r4_sol_anim[0,0],r4_sol_anim[0,1],r4_sol_anim[0,2],color="tab:brown",marker="o",s=100,label="Venus")]
head5=[ax.scatter(r5_sol_anim[0,0],r5_sol_anim[0,1],r5_sol_anim[0,2],color="tab:orange",marker="o",s=100,label="Mercury")]
# head6=[ax.scatter(r6_sol_anim[0,0],r6_sol_anim[0,1],r6_sol_anim[0,2],color="tab:gray",marker="o",s=100)]
# head7=[ax.scatter(r7_sol_anim[0,0],r7_sol_anim[0,1],r7_sol_anim[0,2],color="tab:cyan",marker="o",s=100)]
# head8=[ax.scatter(r8_sol_anim[0,0],r8_sol_anim[0,1],r8_sol_anim[0,2],color="tab:purple",marker="o",s=100)]
# head9=[ax.scatter(r9_sol_anim[0,0],r9_sol_anim[0,1],r9_sol_anim[0,2],color="tab:olive",marker="o",s=100)]

#Create a function Animate that changes plots every frame (here "i" is the frame number)
def Animate(i,head1,head2,head3,head4,head5):
    #Remove old markers
    head1[0].remove()
    head2[0].remove()
    head3[0].remove()
    head4[0].remove()
    head5[0].remove()
    # head6[0].remove()
    # head7[0].remove()
    # head8[0].remove()
    # head9[0].remove()

    #Plot the orbits (every iteration we plot from initial position to the current position)
    trace1=ax.plot(r1_sol_anim[:i,0],r1_sol_anim[:i,1],r1_sol_anim[:i,2],color="darkblue",label="Sun")
    trace2=ax.plot(r2_sol_anim[:i,0],r2_sol_anim[:i,1],r2_sol_anim[:i,2],color="tab:red",label="Earth")
    trace3=ax.plot(r3_sol_anim[:i,0],r3_sol_anim[:i,1],r3_sol_anim[:i,2],color="tab:green",label="Mars")
    trace4=ax.plot(r4_sol_anim[:i,0],r4_sol_anim[:i,1],r4_sol_anim[:i,2],color="tab:brown",label="Venus")
    trace5=ax.plot(r5_sol_anim[:i,0],r5_sol_anim[:i,1],r5_sol_anim[:i,2],color="tab:orange",label="Mercury")
    # trace6=ax.plot(r6_sol_anim[:i,0],r6_sol_anim[:i,1],r6_sol_anim[:i,2],color="tab:gray")
    # trace7=ax.plot(r7_sol_anim[:i,0],r7_sol_anim[:i,1],r7_sol_anim[:i,2],color="tab:cyan")
    # trace8=ax.plot(r8_sol_anim[:i,0],r8_sol_anim[:i,1],r8_sol_anim[:i,2],color="tab:purple")
    # trace9=ax.plot(r9_sol_anim[:i,0],r9_sol_anim[:i,1],r9_sol_anim[:i,2],color="tab:olive")


    #Plot the current markers
    head1[0]=ax.scatter(r1_sol_anim[i-1,0],r1_sol_anim[i-1,1],r1_sol_anim[i-1,2],color="darkblue",marker="o",s=100,label="Sun")
    head2[0]=ax.scatter(r2_sol_anim[i-1,0],r2_sol_anim[i-1,1],r2_sol_anim[i-1,2],color="tab:red",marker="o",s=100,label="Earth")
    head3[0]=ax.scatter(r3_sol_anim[i-1,0],r3_sol_anim[i-1,1],r3_sol_anim[i-1,2],color="tab:green",marker="o",s=100,label="Mars")
    head4[0]=ax.scatter(r4_sol_anim[i-1,0],r4_sol_anim[i-1,1],r4_sol_anim[i-1,2],color="tab:brown",marker="o",s=100,label="Venus")
    head5[0]=ax.scatter(r5_sol_anim[i-1,0],r5_sol_anim[i-1,1],r5_sol_anim[i-1,2],color="tab:orange",marker="o",s=100,label="star")
    # head6[0]=ax.scatter(r6_sol_anim[i-1,0],r6_sol_anim[i-1,1],r6_sol_anim[i-1,2],color="tab:gray",marker="o",s=100)
    # head7[0]=ax.scatter(r7_sol_anim[i-1,0],r7_sol_anim[i-1,1],r7_sol_anim[i-1,2],color="tab:cyan",marker="o",s=100)
    # head8[0]=ax.scatter(r8_sol_anim[i-1,0],r8_sol_anim[i-1,1],r8_sol_anim[i-1,2],color="tab:purple",marker="o",s=100)
    # head9[0]=ax.scatter(r9_sol_anim[i-1,0],r9_sol_anim[i-1,1],r9_sol_anim[i-1,2],color="tab:olive",marker="o",s=100)

    return trace1,trace2,trace3,trace4,trace5,head1,head2,head3,head4,head5

#Add a few bells and whistles
ax.set_xlabel("x-coordinate",fontsize=14)
ax.set_ylabel("y-coordinate",fontsize=14)
ax.set_zlabel("z-coordinate",fontsize=14)
ax.set_xlim(-2.5e11, 2.5e11)
ax.set_ylim(-2.5e11, 2.5e11)
ax.set_zlim(-2.5e11, 2.5e11)
ax.set_box_aspect([1,1,1])
ax.set_title("Visualization of orbits of stars in a N-body system",fontsize=14)

anim=animation.FuncAnimation(fig,Animate, save_count=200, repeat=False,blit=False,fargs=(head1,head2,head3,head4,head5))


#Use the FuncAnimation module to make the animation
#If used in Jupyter Notebook, animation will not display only a static image will display with this command
# =============================================================================
# if N == 1:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1))
# if N == 2:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2))
# if N == 3:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3))
# if N == 4:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3,head4))
# if N == 5:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3,head4,head5))
# if N == 6:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3,head4,head5,head6))
# if N == 7:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3,head4,head5,head6,head7))
# if N == 8:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3,head4,head5,head6,head7,head8))
# if N == 9:
#     anim=animation.FuncAnimation(fig,Animate,interval=60, frames=frames, repeat=False,blit=False,fargs=(head1,head2,head3,head4,head5,head6,head7,head8,head9))
# =============================================================================

# =============================================================================
# #For Jupyter Notebook, enable to make a Javascript animation
# matplotlib.rcParams['animation.embed_limit'] = 2**128 #Increase animation embed limit
# HTML(anim.to_jshtml()) #Convert animation to jsanimation and display
# =============================================================================

#To save animation to disk, enable this command
# anim.save("ThreeBodyProblem_test.mp4")

print("Writing now")

#To save animation to disk, enable this command
f = r"/Users/harry/Desktop/Correction time/NBodyProblem.mp4"
writermp4 = animation.FFMpegWriter(fps=24)
anim.save(f, writer=writermp4, dpi=450)
end = time.time()
print("done writing, time is : ", start-end)



