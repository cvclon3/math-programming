import numpy as np
import solver4 as s
from solver_init_funcs import prepare_data
import solver_m_problem as sm
import solver_init_funcs

Ai = np.array([
    [2, 1, 1],
    [3, 0, 2],
    [0, 0, 1],
])

Bi = np.array([2, 8, 1])
Symb = np.array(['=', '<=', '>='])
Cond = 'min'

Zi = np.array([3, 2, 3])

np.set_printoptions(threshold=np.inf, linewidth=np.inf)


data = s.Data(Ai, Bi, Zi, Symb, Cond)

trans = prepare_data(data)

min_colls_i, err = sm.get_allowed_cols(trans)
print(min_colls_i)
coll_i, row_i, err = sm.get_allowed_rows(trans, cols=min_colls_i)
print(coll_i, row_i)