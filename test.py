# %%

import scipy as sci
from scipy import optimize
import numpy as np

mass = np.array([1.989e30, 0.1989e30])
m = mass[0]/(mass[0]+mass[1])

def L1_function(r):
    m=0.5
    r0 = 3*m**2 - 3*m + 1
    r1 = 1*m**4 - 2*m**3 + 1*m**2 - 4*m + 2
    r2 = -4*m**3 + 6*m**2 - 2*m + 1
    r3 = 6*m**2 - 6*m + 1
    r4 = -4*m + 2
    r5 = 1

    return r5*r**5 + r4*r**4 + r3*r**3 + r2*r**2 + r1*r + r0

print(sci.optimize.newton(L1_function, 0, args=(m)))
print(sci.optimize.bisect(L1_function,-2,2,args=m))

# %%