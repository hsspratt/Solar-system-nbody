# %%

import numpy as np
from scipy.interpolate import interp1d

# generate some example data
W = 5
H = 10
M = 6

A2 = np.arange(W * M).reshape(W, M)
print(A2)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]]

# the initial column indices for A2
x = np.arange(M)

# we create a scipy.interpolate.interp1d instance
itp_A2 = interp1d(x, A2, kind='linear',axis=1)

# the output column coordinates for A1
xi = np.linspace(0, W, M)
xi = np.arange(W)

# we get the interpolated output by calling the interp1d instance with the
# output coordinates
A1 = itp_A2(xi)
print(A1)
# [[  0.   0.   1.   1.   2.   2.   3.   3.   4.   4.]
#  [  5.   5.   6.   6.   7.   7.   8.   8.   9.   9.]
#  [ 10.  10.  11.  11.  12.  12.  13.  13.  14.  14.]]
# %%

Source = np.array([[0, 1, 1],
          [0, 2, 0],
          [0, 3, 1],
          [0, 4, 0],
          [0, 5, 1]])

x = np.arange(0, Source.shape[0])
fit = interp1d(x, Source, axis=0)
Target = fit(np.linspace(0, Source.shape[0]-1, 7))
# %%

a = np.array([[0, 1, 1],
              [0, 2, 0],
              [0, 3, 1],
              [0, 4, 0],
              [0, 5, 1]])

x = np.array(range(a.shape[0]))

# define new x range, we need 7 equally spaced values
xnew = np.linspace(x.min(), x.max(), 9)

# apply the interpolation to each column
f = interp1d(x, a, axis=0)

# get final result
print(f(xnew))

# %%
