# %%
from init_objects import *
import argparse
import scipy.integrate
from matplotlib import pyplot as plt
import numpy as np
import time
from solar import SolarSystem
import scipy as sci
import os
import sys
from render import render_orbit_animation
plt.rc('mathtext', fontset="cm")

# %% Command line options

parser = argparse.ArgumentParser(description="N-body simulation of the Solar System and three-body choreographies")
parser.add_argument("--no-gui", action="store_true",
                    help="skip the Tk GUI and run straight from the options below (works on headless machines)")
parser.add_argument("--config", default="Solar_System",
                    help="configuration to simulate when --no-gui is used, e.g. Solar_System, Figure_8, Butterfly_I")
parser.add_argument("--solver", help="scipy solve_ivp method: RK45, RK23, DOP853, Radau, BDF, LSODA (default depends on --config)")
parser.add_argument("--G", type=float, help="gravitational constant (default depends on --config)")
parser.add_argument("--time-period", type=float, help="length of one time period (default depends on --config)")
parser.add_argument("--n-periods", type=float, help="number of time periods to simulate")
parser.add_argument("--iterations", type=float, help="iterations per time period")
parser.add_argument("--rtol", type=float, help="relative tolerance of the ODE solver (default depends on --config)")
parser.add_argument("--atol", type=float, help="absolute tolerance of the ODE solver (default depends on --config)")
parser.add_argument("--animate", action="store_true", help="also render the orbit animation to video")
parser.add_argument("--fps", type=int, default=30, help="animation frame rate")
parser.add_argument("--frames", type=int, default=300, help="number of frames in the animation")
args, _ = parser.parse_known_args()  # tolerate extra argv from IDEs / interactive kernels

# Sensible starting values for each configuration (same as the README table).
# SI units for the real Solar System, G = 1 units for the three-body choreographies.
presets = {
    'Solar_System': dict(G=6.6743015e-11, time_period=31536000, n_periods=100, iterations=25,
                         solver="RK45", rtol=1e-3, atol=1e-6),
    'Figure_8':     dict(G=1, time_period=6.32591398, n_periods=0.5, iterations=25,
                         solver="RK45", rtol=1e-3, atol=1e-6),
}
choreography_periods = {
    'Butterfly_I': 6.235641, 'Butterfly_II': 7.0039, 'Butterfly_III': 13.8658,
    'moth_I': 14.8939, 'moth_II': 28.6703, 'moth_III': 25.8406, 'bumblebee': 63.5345,
    'goggles': 10.4668, 'dragonfly': 21.2710, 'yarn': 55.5018, 'yin_yang_I_a': 17.3284,
}
for name, period in choreography_periods.items():
    # These orbits are unstable: at rtol=1e-3 the energy drifts past 1% within the first
    # tenth of a period, so they get a high-order solver with tight tolerances.
    presets[name] = dict(G=1, time_period=period, n_periods=1, iterations=200,
                         solver="DOP853", rtol=1e-9, atol=1e-9)

# %% Initialising all the planets, suns and objects that could be used in the simulation

if args.no_gui:
    preset = presets.get(args.config, dict(G=1, time_period=10, n_periods=1, iterations=200,
                                           solver="DOP853", rtol=1e-9, atol=1e-9))
    planets = [args.config]
    # command line values win, anything not given falls back to the configuration's preset
    settings = {key: getattr(args, key) if getattr(args, key) is not None else preset[key]
                for key in ["G", "time_period", "n_periods", "iterations", "solver", "rtol", "atol"]}
    settings["animate"] = args.animate
else:
    """Code to create and run GUI, from which you can change the configuration of the simulation"""
    import tkinter as tk
    import n_body_app

    root = tk.Tk()
    root.title("N Body Simulation")
    root.geometry('400x300')
    app = n_body_app.n_body_app(root)
    root.mainloop()

    planets = app.planets

    if len(app.ODE) > 1:
        print("Only one ODE solver must be selected! Using", app.ODE[0])
    if len(app.ODE) == 0:
        app.ODE = ["RK45"]
        print("The defult ODE solver will be used as none were selected")

    settings = dict(
        G=float(app.G.get()), time_period=float(app.time_period.get()),
        n_periods=float(app.n_time_period.get()), iterations=float(app.iterations.get()),
        rtol=float(app.rtol.get()), atol=float(app.atol.get()), solver=app.ODE[0],
        animate=app.animate.get() or args.animate)

print(planets)

individual_bodies = {body.name: body for body in
                     [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, External_Planet]}

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

# Previously this relied on an AttributeError from the configuration lists to reach the
# fallback branch, and choosing a single planet crashed with a KeyError. Explicit lookup instead.
if len(planets) == 0:
    objects = thisdict['Solar_System']
    print("The defult configuration - the solar system - has been initiated")
elif planets[0] in thisdict:
    if len(planets) > 1:
        print("More than one configuration chosen, only", planets[0], "will be simulated")
    objects = thisdict[planets[0]]
else:
    unknown = [p for p in planets if p not in individual_bodies]
    if unknown:
        sys.exit(f"Unknown planet / configuration: {unknown}. Choose from {list(individual_bodies) + list(thisdict)}")
    objects = [individual_bodies[p] for p in planets]
    if len(objects) < 2:
        sys.exit("At least two objects need to be selected for an N-body simulation")
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
G = float(settings["G"])  # 6.67408e-11

# Reference quantities - to convert the emphemeris data from nasa to SI units
years = float(settings["n_periods"])  # 100

# Define times
tStart = 0e0
time_period = float(settings["time_period"])  # 60*60*24*365
n_time_periods = years
iterations_year = float(settings["iterations"])  # 25
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

# ## Get constants from the GUI / command line

rtol = float(settings["rtol"])
atol = float(settings["atol"])  # previously read from the rtol box by mistake
integrator = settings["solver"]

# ## Run the solve_ivp solver
three_body_sol = sci.integrate.solve_ivp(fun=SolarSystem.ThreeBodyEquations, t_span=domain, y0=init_params, args=(
    G, planets_mass, N, K1, K2), max_step=max_steps, rtol=rtol, atol=atol, method=integrator)
if not three_body_sol.success:
    sys.exit(f"The ODE solver failed: {three_body_sol.message}")
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

save_results_to = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Plots Generated", "")
os.makedirs(save_results_to, exist_ok=True)

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
plotPE.legend(loc='center right', bbox_to_anchor=(0.90, 0.5))  # was plotKE.legend() inside the loop
plotPE.show()
plotPE.savefig(save_results_to + "planets_PE.png", bbox_inches='tight')

plotTotal = plt.figure(3)
plt.plot(t, KE.flatten(), label="Kinetic energy",linewidth=0.9)
plt.plot(t, PE.flatten(), label="Potential energy", linewidth=0.9)
plt.plot(t, total, label="Total energy", linewidth=0.9)
plt.plot(t, np.full((1, len(t)), virial)[0,:], label=r"Virial: $2\langle KE \rangle + \langle PE \rangle$", linewidth=0.9)
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
plt.ylabel("Linear momentum ($kgms^{-1}$)")
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

threeD_plot = plt.figure(figsize=plt.figaspect(1)*2)
# Matplotlib >= 3.6 removed fig.gca(projection=...) and the ax.dist / get_proj hacks;
# set_box_aspect squashes the z axis (4:4:1) the supported way.
ax = threeD_plot.add_subplot(projection='3d', proj_type='ortho')
ax.set_box_aspect((4, 4, 1), zoom=1.2)
ax.view_init(elev=45/2, azim=45)
line = [ax.plot(r_com_sol[:, i*3], r_com_sol[:, i*3+1], r_com_sol[:,i*3+2], c=(colours)[i], label=solarsystem.planets[i].name, linewidth=0.9)[0] for i in range(N)]
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
# z range scales with the orbit size so G = 1 configurations are not flattened
orbit_extent = np.max(np.abs(r_com_sol))
ax.set_zlim([-orbit_extent/8, orbit_extent/8])
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
plt.ylabel("Linear momentum ($kgms^{-1}$)")
plotLx.legend(loc='upper left', bbox_to_anchor=(0.12, 0.80))
plotLx.show()
plotLx.show()
plotLx.savefig(save_results_to +'planets_momentum_x.png',dpi=600, bbox_inches='tight')

plotL_xyz = plt.figure(8)
plt.plot(t, linear_x.flatten(),linewidth=0.9, label='$x$')
plt.plot(t, linear_y.flatten(), linewidth=0.9, label='$y$')
plt.plot(t, linear_z.flatten(), linewidth=0.9, label='$z$')
plt.xlabel("Components of linear momentum over time", fontsize='9')
plt.ylabel("Linear momentum ($kgms^{-1}$)")
plotL_xyz.legend(loc='center left', bbox_to_anchor=(0.15, 0.75))
plotL_xyz.show()
plotL_xyz.savefig(save_results_to +'Linear_Momentum_System_components.png',dpi=600, bbox_inches='tight')

plot_planetsAngular = plt.figure(11)
for planet in solarsystem.planets:
    i = solarsystem.planets.index(planet)
    plt.plot(t[1:], planet.angular_m[1:-1, 0], (colours)[i],
             label=solarsystem.planets[i].name, linewidth=0.9)
plt.title("Angular momentum of individual planets over time", fontsize='9')
plt.xlabel("Time")
plt.ylabel("Angular momentum ($kgm^2s^{-1}$)")
plot_planetsAngular.legend(loc='upper left', bbox_to_anchor=(0.12, 0.90))
plot_planetsAngular.show()
plot_planetsAngular.savefig(save_results_to + 'planets_momentum_angular.png', dpi=600, bbox_inches='tight')

end = time.time()

print("Time for calculating enrgy and plotting is:   " , end-start)

"""Crudely evaluates when the orbit and physics is no longer valid"""

# Energy drift relative to the starting energy; a drift of more than 1% either way is
# treated as the point where the integration can no longer be trusted.
total_off = ((total-total[0])/abs(total[0]))*100
drifted = np.flatnonzero(np.abs(total_off) >= 1)

if len(drifted) == 0:
    print("This orbit looks stable. The change in energy from the beginning to end is: ", total_off[-1],"%")
else:
    print("Energy drifted by more than 1% at time step", drifted[0], "of", len(total_off),
          "(t = %.4g). Try tighter tolerances, e.g. --rtol 1e-9 --atol 1e-9 --solver DOP853" % t[drifted[0]])

# %% Animation - tick "Render animation" in the GUI, or pass --animate on the command line

if settings["animate"]:
    render_orbit_animation(t, r_com_sol, [planet.name for planet in solarsystem.planets],
                           save_results_to + "Orbit_Animation.mp4",
                           fps=args.fps, n_frames=args.frames)

if not args.no_gui:
    plt.show()  # keep the plot windows open until they are closed
