import numpy as np
import solver4 as s
from solver_init_funcs import prepare_data
import solver_m_problem as sm
import solver_init_funcs

Ai = np.array([
    [2, 1, 1],
    [3, 8, 2],
    [0, 0, 1],
])

Bi = np.array([2, 8, 1])
Symb = np.array(['<=', '>=', '>='])
Cond = 'min'

Zi = np.array([3, 2, 3])

np.set_printoptions(threshold=np.inf, linewidth=np.inf)


data = s.Data(Ai, Bi, Zi, Symb, Cond)

transp = prepare_data(data)

print("START")
while not sm.is_m_solved(obj=transp):
    min_colls_i, err = sm.get_allowed_cols(transp)
    # print(min_colls_i)
    coll_i, row_i, err = sm.get_allowed_rows(transp, cols=min_colls_i)
    # print(coll_i, row_i)
    transp = sm.New_Table_(obj=transp, row=row_i, col=coll_i)

    print(transp.table_.real)
print(transp.answer_)

    

optimal_plan = np.zeros(transp.table_.shape[1] - 2)
for i in range(transp.answer_.shape[0]):
    optimal_plan[transp.answer_[i]] = transp.table_[1:-1, 1][i]
    
print(optimal_plan)