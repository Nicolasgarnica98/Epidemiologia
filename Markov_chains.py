import numpy as np
from numpy.lib.shape_base import _apply_along_axis_dispatcher

p = np.array([[0.05,0.95],
              [0.10,0.90]])

p = np.power(p,1)
p = np.append(p,[[3.00,3.00]],axis=0)
print(p)