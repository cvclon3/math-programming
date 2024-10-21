from . import Data, Transport, Answer, Solver
import numpy as np


def find_base_x(mtx):
    """ 
    Нахождение индексов бозесных переменных
    """
    vectors_to_find = np.identity(3)
    found = np.all(np.isin(mtx.T, vectors_to_find), axis=1)
    true_indices = np.where(found)[0]
    return true_indices

def init_Symb_arr_(data):
    """
    Определение навых переменных в зависимости от знака
    """
    mtx = data.Ai_mtx.copy()
    size_ = data.Ai_mtx_.shape[0]
    for i in range(data.Symb_arr_.shape[0]):   
        cols = np.zeros(size_)
        if data.Symb_arr_[i] == '>=':
            cols[i] = -1
        if data.Symb_arr_[i] == '<=':
            cols[i] = 1
        mtx = np.column_stack((mtx, cols))
    return mtx
    


def prepare_data(data: Data) -> Transport:
    mtx = init_Symb_arr_(data)
    print(find_base_x(mtx))
    

    

            