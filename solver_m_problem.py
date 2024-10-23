from solver4 import Data, Transport, Answer, Solver
import numpy as np


def get_allowed_indexes(obj: Transport) -> tuple(int, int, int):
    '''
    # Возвращаем номер разрешающего столбца!!!!!!

    Коды ошибок:
    0 - OK
    1 - М задача
    '''
    if is_m_solved(obj):
        return tuple([-1, 1])

    err_ = 0

    if obj.get_cond() == 'min':
        allowed_cols_indexes_, err_ = get_allowed_cols(obj=obj)

        allowed_rows_index_, allowed_cols_index_, err_ = get_allowed_rows(obj=obj)


    elif obj.get_cond() == 'max':
        pass


def is_m_solved(obj: Transport) -> bool:
    '''
    Проверяем решена ли М задача
    '''
    table_ = obj.table_.copy()

    # Опорный план
    ref_plan = table_[-1]

    # Если в опорном плане не содержится комплексных переменных - М переменных
    # то это значит что М задача решена
    return np.sum(np.abs(ref_plan.imag)) == 0


def get_allowed_cols(obj: Transport) -> tuple[np.ndarray, int]:
    '''
    Возвращаем номер разрешающего столбца

    Коды ошибок
    0 - OK
    11 - в задаче на минимум нет положительных значенией
    12 - в задаче на максимум нет отрицательных значенией
    '''
    err_ = 0
    assert obj.get_cond() == 'min' or obj.get_cond() == 'max', "Error in [M] get_allowed_cols"

    table_ = obj.table_.copy()
    ref_plan = table_[-1]
    allowed_cols_index_ = -1

    if obj.get_cond() == 'min':
        allowed_cols_index_ = np.where(ref_plan.imag == np.max(ref_plan.imag))[0]

        if ref_plan[allowed_cols_index_] < 0:
            err_ = 11

    elif obj.get_cond() == 'max':
        allowed_cols_index_ = np.where(ref_plan.imag == np.min(ref_plan.imag))[0]

        if ref_plan[allowed_cols_index_] > 0:
            err_ = 12

    return tuple([allowed_cols_index_, err_])


def get_allowed_rows(obj: Transport, **kwargs) -> tuple[int, int, int]:
    '''
        Возвращаем номер разренающей строки

        Аргументы:
        - obj: Transport
        **kwargs
        - 'cols': np.ndarray

        Ретурним
        1) int - allowed_cols_index
        2) int - allowed_rows_index
        3) int - error code


        Коды ошибок
        0 - OK
        21 - в задаче на минимум нет положительных значенией
        22 - в задаче на максимум нет отрицательных значенией
        '''
    err_ = 0
    table_ = obj.table_.copy()
    A0_ = table_[1:-1, 1].copy()
    mtx_ = table_[1:-1, 2:]
    allowed_cols_index_ = -1,
    allowed_rows_index_ = -1
    simplex_rel = -1

    assert obj.get_cond() == 'min' or obj.get_cond() == 'max', "Error in [M] get_allowed_rows"

    min_index = get_col_row(A0=A0_, mtx=mtx_, allowed_cols_indexes=kwargs['cols'])

    if min_index.shape[0] == 1:
        return tuple(min_index[0], min_index[1], 0)

    if min_index.shape[0] > 1:
        pass

    if min_index.shape[0] < 1:
        pass


def get_col_row(A0: np.ndarray, mtx: np.ndarray, allowed_cols_indexes: np.ndarray) -> np.ndarray:
    all_simplex_res = np.zeros(shape=(allowed_cols_indexes.shape[0], A0.shape[0]))

    print(all_simplex_res)

    for i in range(allowed_cols_indexes.shape[0]):
        if allowed_cols_indexes[i] == i:
            all_simplex_res[i] = np.full(shape=(A0.shape[1],), fill_value=np.inf)
        else:
            all_simplex_res[i] = A0.T[0] / mtx.T[allowed_cols_indexes[i]]

    all_simplex_res = np.where(np.isnan(all_simplex_res), np.inf, all_simplex_res)
    all_simplex_res = np.where(all_simplex_res <= 0, np.inf, all_simplex_res)

    print(all_simplex_res)
    min_index = np.argwhere(all_simplex_res == np.min(all_simplex_res))

    return min_index


# def get_col_row_2(mtx: np.ndarray, allowed_cols_indexes: np.ndarray) -> np.ndarray:
#
#     all_simplex_res = np.zeros(shape=(allowed_cols_indexes.shape[0], mtx.shape[1], mtx.shape[0]))
#
#     print(all_simplex_res)
#
#     for i in range(allowed_cols_indexes.shape[0]):
#         for j in range(mtx.shape[1]):
#             if allowed_cols_indexes[i] == j:
#                 all_simplex_res[i, j] = np.full(shape=(mtx.shape[0],), fill_value=np.inf)
#             else:
#                 all_simplex_res[i, j] = mtx.T[j]/mtx.T[allowed_cols_indexes[i]]
#
#     all_simplex_res = np.where(np.isnan(all_simplex_res), np.inf, all_simplex_res)
#     all_simplex_res = np.where(all_simplex_res <= 0, np.inf, all_simplex_res)
#
#     print(all_simplex_res)
#     min_index = np.argwhere(all_simplex_res == np.min(all_simplex_res))
#
#     min_index = np.array(min_index).flatten()[:3]
#     print(min_index)
#     print(f'индекс разрешающего столбца: {allowed_cols_indexes[min_index[0]]}')
#     print(f'индекс разрешающей строки: {min_index[-1]}')
#     print(f'минимальный элемент: {all_simplex_res[min_index[0], min_index[1], min_index[2]]}')
