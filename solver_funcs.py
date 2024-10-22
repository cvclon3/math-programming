from solver4 import Data, Transport, Answer, Solver
import numpy as np




def sum_base_vars(mtx, baseI):
    """
    finding sum base variables
    """
    sum = np.zeros(mtx.shape[0])
    for i in baseI:
        sum = sum + mtx.T[int(i)]
    return sum

def find_base_x(mtx):
    """ 
    Нахождение индексов бозесных переменных
    """
    cols_size = mtx.shape[1]
    mtx_ = mtx.copy()

    for i in range(mtx.shape[0]):
        for j in range(mtx.shape[1]):
            if mtx[i, j] != 0 and mtx[i, j] != 1:
                mtx_[i, j] = np.inf
    mtx_ = mtx_.T
    res = np.array([], dtype=int)
    sum = np.zeros(mtx.shape[0])
    ones = np.ones(mtx.shape[0])
    for i in range(cols_size):
        sum_in_cols = np.sum(mtx_[i])
        if sum_in_cols == 1:
            if np.all(sum + mtx_[int(i)] <= ones):
                res = np.append(res, i)
                sum = sum + mtx_[int(i)]

    return res

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
            mtx = np.column_stack((mtx, cols))
            data.Zi_mtx_ = np.append(data.Zi_mtx_, 0)

        if data.Symb_arr_[i] == '<=':
            cols[i] = 1
            mtx = np.column_stack((mtx, cols))
            data.Zi_mtx_ = np.append(data.Zi_mtx_, 0)

    return mtx

def add_amega_vars(data, mtx, amegaI):
    print(mtx.real)
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
    arrCA = np.zeros((len(mtx_) + 1, 2), dtype=complex).tolist()

    for i in range(len(baseI_in_extended_mtx)):
        index_of_one = np.where(mtx_.T[baseI_in_extended_mtx[i]] == 1)[0]

        arrCA[i + 1][1] = Bi_mtx_[int(i)]
        arrCA[index_of_one[0] + 1][0] = mtx[0][baseI_in_extended_mtx[i]]
    return np.concatenate((arrCA,  mtx), axis=1)


def delta_i(arr):
    for i in range(arr.shape[1] - 1):
        arrI = 0
        for j in range(arr.shape[0] - 2):
            arrI += arr[j + 1][i + 1] * arr[j + 1][0]
        arr[-1][i + 1] = arrI - arr[0][i + 1]
    return arr


def prepare_data(data: Data) -> Transport:
    mtx = init_Symb_arr_(data)
    #Добаавление иксов в зависимости от знака
    baseI = find_base_x(mtx)
    #Нахождение базесных переменных
    sum = sum_base_vars(mtx, baseI)
    print(sum)
    extended_mtx = add_amega_vars(data, mtx, sum)

    baseI_in_extended_mtx = find_base_x(extended_mtx)
    print(baseI_in_extended_mtx)
    mtx = np.vstack((data.Zi_mtx_, extended_mtx))
    print(mtx)
    mtx = add_left_part(mtx, baseI_in_extended_mtx, data.Bi_mtx_)
    print(mtx.real)
    mtx = np.vstack((mtx, np.zeros(mtx.shape[1])))
    print(delta_i(mtx))

    

            