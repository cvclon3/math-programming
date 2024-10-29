import numpy as np
import solver4 as s
from solver_init_funcs import prepare_data
import solver_m_problem as sm
import solver_init_funcs

Ai = np.array([
    [2, 1, 1],
    [3, 8, 2],
    [10, 2, 1],
])

Bi = np.array([2, 8, 1])
Symb = np.array(['<=', '>=', '>='])
Cond = 'min'

Zi = np.array([3, 12, 3])

np.set_printoptions(threshold=np.inf, linewidth=np.inf)


data = s.Data(Ai, Bi, Zi, Symb, Cond)

transp = prepare_data(data)

print("PRE START")
print(transp.table_)

print("START")
p = 0
while not sm.is_m_solved(obj=transp) and p < 10:
    min_colls_i, err = sm.get_allowed_cols(transp)
    # print(f'len_colls_i {len(min_colls_i)}')
    # if err == 11:
    #     break
    print(f'cols err: {err}')
    # print(min_colls_i)
    coll_i, row_i, err = sm.get_allowed_rows(transp, cols=min_colls_i)
    print(f'rows err: {err}')
    print(coll_i, row_i)
    transp = sm.New_Table_(obj=transp, row=row_i, col=coll_i)

    # print(f'real: {transp.table_.real}')
    # print(f'imag: {transp.table_.imag}')
    print(transp.table_)

    print(f"оптимальный план{transp.answer_}")
    p += 1

    

optimal_plan = np.zeros(transp.table_.shape[1] - 2, dtype=np.complex128)
for i in range(transp.answer_.shape[0]):
    optimal_plan[transp.answer_[i]] = transp.table_[1:-1, 1][i]
    
print(optimal_plan.real)