import numpy as np
import solver4 as s

Ai = np.array([
    [2, 1, 1],
    [3, 8, 2],
    [0, 0, 1],
])

Bi = np.array([2, 8, 1])
Symb = np.array(['<=', '>=', '>='])
Cond = 'min'

Zi = np.array([3, 2, 3])