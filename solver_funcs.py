from solver4 import Data, Transport, Answer, Solver
import numpy as np


def find_base_x(mtx):
    """ 
    Нахождение индексов бозесных переменных
    """
    vectors_to_find = np.identity(mtx.shape[0])
    found = np.all(np.isin(mtx.T, vectors_to_find), axis=1)
    true_indices = np.where(found)[0]
    return true_indices

def init_Symb_arr_(data):
    """
    Определение навых переменных в зависимости от знака
    """
    mtx = data.Ai_mtx_.copy()
    size_ = data.Ai_mtx_.shape[0]
    for i in range(data.Symb_arr_.shape[0]):   
        cols = np.zeros(size_)
        if data.Symb_arr_[i] == '>=':
            cols[i] = -1
            data.Zi_mtx_ = np.append(data.Zi_mtx_, 0)
        if data.Symb_arr_[i] == '<=':
            cols[i] = 1
            data.Zi_mtx_ = np.append(data.Zi_mtx_, 0)
        mtx = np.column_stack((mtx, cols))
    return mtx

def sum_base_vars(mtx, baseI):
    """
    finding sum base variables
    """
    sum = np.zeros(baseI.shape[0])
    for i in baseI:
        sum = sum + mtx.T[i]
    return sum

def add_amega_vars(data, mtx, amegaI):
    mtx_ = mtx.copy()
    size_ = amegaI.shape[0]
    vectors_to_find = np.identity(size_)
    for i in range(size_):
        if amegaI[i] == 0:
            mtx_ = np.column_stack((mtx_, vectors_to_find[i]))
            if data.Cond_ == "min":
                data.Zi_mtx_ = np.append(data.Zi_mtx_, 1j)
                continue
            data.Zi_mtx_ = np.append(data.Zi_mtx_, -1j)
    return mtx_

def add_left_part(mtx, baseI_in_extended_mtx, Bi_mtx_):
    mtx_ = mtx.copy()[1:]
    arrCA = [[0], [0]]
    vectors_to_find = np.identity(mtx.shape[0] - 1)
    for i in range(baseI_in_extended_mtx.shape[0]):
        vectors_to_find = np.delete(vectors_to_find, mtx_.T[baseI_in_extended_mtx[i]], axis=0)





def prepare_data(data: Data) -> Transport:
    mtx = init_Symb_arr_(data)
    print(mtx)
    baseI = find_base_x(mtx)
    print(baseI)
    sum = sum_base_vars(mtx, baseI)
    print(sum)
    extended_mtx = add_amega_vars(data, mtx, sum)
    print(extended_mtx)
    print(data.Zi_mtx_)
    baseI_in_extended_mtx = find_base_x(extended_mtx)
    print(baseI_in_extended_mtx)
    mtx = np.vstack((data.Zi_mtx_, extended_mtx))
    print(mtx)
    mtx = add_left_part(mtx, baseI_in_extended_mtx, data.Bi_mtx_)

    

            