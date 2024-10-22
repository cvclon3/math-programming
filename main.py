import numpy as np
import solver4 as s
from solver_funcs import prepare_data


Ai = np.array([
    [1, 0, 1j],
    [0, 0, 0],
    [0, 1, 0],
])

Bi = np.array([2, 8, 1])
Symb = np.array(['>=', '>=', '>='])
Cond = 'min'

Zi = np.array([3, 2, 3])

data = s.Data(Ai, Bi, Zi, Symb, Cond)

prepare_data(data)