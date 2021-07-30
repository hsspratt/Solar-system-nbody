# %%
import scipy as sci
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
# %%

# function to find the closest point in an array to match up two arrays
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# calculates the effective potential to be plotted on the graph
def gravitational_potential(mass, positions, xx, yy):

    """Initialises the mass and positions"""
    m1 = mass[0]
    m2 = mass[1]

    m1 = mass[0]/(mass[0]+mass[1])
    m2 = mass[1]/(mass[0]+mass[1])

    r_m1 = positions[0]
    r_m2 = positions[1]

    G = 1

    total_PE = G*(m1/np.sqrt((xx - r_m1[0])**2 + (yy - r_m1[1])**2)
                  + m2/np.sqrt((xx - r_m2[0])**2 + (yy - r_m2[1])**2))

    rotational_PE = 1/2*(xx**2 + yy**2)

    effective_PE = total_PE + rotational_PE

    return effective_PE

top = 1
limit = 3

x = np.linspace(-limit, limit, 70)
y = np.linspace(-limit, limit, 70)

xx, yy = np.meshgrid(x, y)

mass = np.array([1.989e30, 1.989e30/(20)])
m = mass[1]/(mass[0]+mass[1])
positions = np.array([[-1+m, 0], [m, 0]])
positions_x = np.array([positions[0][0], positions[1][0]])
distance_between = abs(positions[0]-positions[1])

# The follwing functions calculate the first three Lagrange points

def L1_function(r,m):
    m=m
    r0 = 3*m**2 - 3*m + 1
    r1 = 1*m**4 - 2*m**3 + 1*m**2 - 4*m + 2
    r2 = -4*m**3 + 6*m**2 - 2*m + 1
    r3 = 6*m**2 - 6*m + 1
    r4 = -4*m + 2
    r5 = 1

    return r5*r**5 + r4*r**4 + r3*r**3 + r2*r**2 + r1*r + r0

def L2_function(r,m):
    m=m
    r0 = -2*m**3 + 3*m**2 - 3*m + 1
    r1 = 1*m**4 - 2*m**3 + 5*m**2 - 4*m + 2
    r2 = -4*m**3 + 6*m**2 - 4*m + 1
    r3 = 6*m**2 - 6*m + 1
    r4 = -4*m + 2
    r5 = 1

    return r5*r**5 + r4*r**4 + r3*r**3 + r2*r**2 + r1*r + r0

def L3_function(r,m):
    r0 = -3*m**2 + 3*m - 1
    r1 = 1*m**4 - 2*m**3 + 1*m**2 + 4*m - 2
    r2 = -4*m**3 + 6*m**2 - 2*m - 1
    r3 = 6*m**2 - 6*m + 1
    r4 = -4*m + 2
    r5 = 1

    return r5*r**5 + r4*r**4 + r3*r**3 + r2*r**2 + r1*r + r0

# Uses the mesh grid of xx & yy to create a contour graph for the PE
z = gravitational_potential(mass, positions, xx, yy)

# prints the positions of the Lagrange points
print("L1:",sci.optimize.bisect(L1_function, -limit, limit, args=m))
print("L2:",sci.optimize.bisect(L2_function, -limit, limit, args=m))
print("L3:",sci.optimize.bisect(L3_function, -2, 2, args=m))

"""Calculating and plotting the Lagrange Points"""
L1 = sci.optimize.bisect(L1_function, -limit, limit, args=m)
L2 = sci.optimize.bisect(L2_function, -limit, limit, args=m)
L3 = sci.optimize.bisect(L3_function, -limit, limit, args=m)
L4 = np.average(positions_x)
L5 = np.average(positions_x)

L1_x = find_nearest(x, L1)
L2_x = find_nearest(x, L2)
L3_x = find_nearest(x, L3)
L4_x = find_nearest(x, L4)
L5_x = find_nearest(x, L5)

L4_y =  (np.sqrt(3)*distance_between[0])/2
L5_y = -(np.sqrt(3)*distance_between[0])/2

L1_z = z[np.where(x == L1_x), np.where(x == L1_x)]
L2_z = z[np.where(x == L2_x), np.where(x == L2_x)]
L3_z = z[np.where(x == L3_x), np.where(x == L3_x)]
L4_z = z[np.where(y == L4_x), np.where(x == L4_x)]
L5_z = z[np.where(y == L5_x), np.where(x == L5_x)]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(x, y, -z, 50)
ax.invert_xaxis()
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)

ax.scatter3D(2*L4-L1, 0, -L1_z, label="L1", s=65)
ax.scatter3D(-L4+L2, 0, -L2_z, label="L2", s=65)
ax.scatter3D(L4-L3, 0, -L3_z, label="L3", s=65)
ax.scatter3D(L4, L4_y, -L4_z, label="L4", s=65)
ax.scatter3D(L5, L5_y, -L5_z, label="L5", s=65)
ax.legend(loc="lower left")

if top == 1:
    ax.view_init(elev=90., azim=90)
    ax.w_zaxis.line.set_lw(0.)
    ax.set_zticks([])
    ax.dist = 7
else:
    ax.set_zlabel(r'$z$', fontsize=15)
ax.set_title('Plot of the Effective Potential for $\mu$ = %.2f' %
             (m,), fontsize=16)

plt.show()