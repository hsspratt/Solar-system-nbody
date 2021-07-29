# %%

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


def gravitational_potential(mass, positions, xx, yy):
    
    m1 = mass[0]
    m2 = mass[1]

    r_m1 = positions[0]
    r_m2 = positions[1]
    
    G = 1 # G = 6.674*10**(-11)
    reduced_mass = (mass[0]*mass[1]/sum(mass))
    distance_between = np.sqrt((r_m1[0] - r_m2[0])**2
                               +(r_m1[1] - r_m2[1])**2)

    m1 = mass[0]/mass[0]
    m2 = mass[1]/mass[0]
    
    r_m1 = positions[0]
    r_m2 = positions[1]
    
    r_position = np.sqrt(abs(xx**2+yy**2))
    
    # PE = G*(m1/(r_position-r_m1) + m2/(r_position-r_m2))
    
    total_PE = G*(m1/np.sqrt((xx - r_m1[0])**2 + (yy - r_m1[1])**2)
                  + m2/np.sqrt((xx - r_m2[0])**2 + (yy - r_m2[1])**2))
    
    rotational_PE = 1/2*(xx**2 + yy**2)
    
    effective_PE = total_PE + rotational_PE

    return effective_PE

top = 1

x = np.linspace(-2, 2, 30)
y = np.linspace(-2, 2, 30)

xx, yy = np.meshgrid(x,y)

mass = np.array([1.989e30, 1.989e30])
positions = np.array([[-1, 0], [1, 0]])


M = 10
m = 1
R = 10
z = gravitational_potential(mass, positions,xx,yy)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(x, y, -z, 50)
ax.invert_xaxis()
ax.set_xlabel(r'$x$', fontsize=15)
ax.set_ylabel(r'$y$', fontsize=15)
if top == 1:
    ax.view_init(elev=90., azim=90)
    ax.w_zaxis.line.set_lw(0.)
    ax.set_zticks([])
    ax.dist = 7
else:
    ax.set_zlabel(r'$z$', fontsize=15)
ax.set_title('Plot of the Gravitational Potential for $\mu=%.2f$' %
             (M,), fontsize=16)

plt.show()

# %%
