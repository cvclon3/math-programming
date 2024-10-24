from solver4 import Data, Transport, Answer, Solver
import numpy as np

'''
TODO:
- доделать функцию проверки столбца на условие ограниченности
'''


# def get_allowed_indexes(obj: Transport) -> tuple[int, int, int]:
#     '''
#     # Возвращаем номер разрешающего столбца!!!!!!
#
#     Коды ошибок:
#     0 - OK
#     1 - М задача
#     '''
#     if is_m_solved(obj):
#         return tuple([-1, -1, 1])
#
#     err_ = 0
#
#     allowed_cols_indexes_, err_ = get_allowed_cols(obj=obj)
#
#     allowed_rows_index_, allowed_cols_index_, err_ = get_allowed_rows(obj=obj, cols=allowed_cols_indexes_)
#
#     return tuple([0, 0, 0])


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
        ПРИМЕР ИСПОЛЬЗОВАНИЯ:
        ...
        allowed_cols_indexes = get_allowed_cols(obj=Transport)
        #!!! Второй аргумент обязательно должен быть 'cols'
        allowed_rows_indexes = get_allowed_rows(obj=Transport, cols=allowed_cols_indexes)
        ...

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
        23 - не смог найти разрешающую строку (см. Ошибка 23)
        24 - нашел больше одной разрешающей строки2 (см. Ошибка 24)
        25 - не смог найти разрешающую строку2 (см. Ошибка 25)
        '''
    table_ = obj.table_.copy()
    A0_ = table_[1:-1, 1].copy()
    mtx_ = table_[1:-1, 2:]

    assert obj.get_cond() == 'min' or obj.get_cond() == 'max', "Error in [M] get_allowed_rows"

    # Ошибка 23
    # Возникает здесь
    min_index = get_col_row(A0=A0_, mtx=mtx_, allowed_cols_indexes=kwargs['cols'])

    if min_index.shape[0] == 1:
        return tuple([min_index[0][0], min_index[0][1], 0])

    if min_index.shape[0] > 1:
        # Получаем только индексы столбцов
        min_index_cols = min_index[:, 0]

        # Ошибка 24
        # Получаем уже новые проверенные индексы
        res = get_col_row_2(mtx=mtx_, allowed_cols_indexes=min_index_cols)
        if res.shape[0] > 1:
            err_ = 24
        # Ошибка 25
        elif res.shape[0] < 1:
            err_ = 25

        res = res[0]

        return tuple([res[0], res[2], err_])

    # Ошибка 23
    if min_index.shape[0] < 1:
        return tuple([-1, -1, 23])


def get_col_row(A0: np.ndarray, mtx: np.ndarray, allowed_cols_indexes: np.ndarray) -> np.ndarray:
    '''
    Код для поиска разрешающей строки
    Возвращает пары чисел - столбец,строка
    '''
    all_simplex_res = np.zeros(shape=(allowed_cols_indexes.shape[0], A0.shape[0]))

    # print(all_simplex_res)

    for i in range(allowed_cols_indexes.shape[0]):
        if allowed_cols_indexes[i] == i:
            all_simplex_res[i] = np.full(shape=(A0.shape[1],), fill_value=np.inf)
        else:
            all_simplex_res[i] = A0.T[0] / mtx.T[allowed_cols_indexes[i]]

    all_simplex_res = np.where(np.isnan(all_simplex_res), np.inf, all_simplex_res)
    all_simplex_res = np.where(all_simplex_res <= 0, np.inf, all_simplex_res)

    # print(all_simplex_res)
    min_index = np.argwhere(all_simplex_res == np.min(all_simplex_res))

    for i in range(min_index.shape[0]):
        min_index[i][0] = allowed_cols_indexes[min_index[i][0]]

    return min_index


def get_col_row_2(mtx: np.ndarray, allowed_cols_indexes: np.ndarray) -> np.ndarray:

    all_simplex_res = np.zeros(shape=(allowed_cols_indexes.shape[0], mtx.shape[1], mtx.shape[0]))

    # print(all_simplex_res)

    for i in range(allowed_cols_indexes.shape[0]):
        for j in range(mtx.shape[1]):
            if allowed_cols_indexes[i] == j:
                all_simplex_res[i, j] = np.full(shape=(mtx.shape[0],), fill_value=np.inf)
            else:
                all_simplex_res[i, j] = mtx.T[j]/mtx.T[allowed_cols_indexes[i]]

    all_simplex_res = np.where(np.isnan(all_simplex_res), np.inf, all_simplex_res)
    all_simplex_res = np.where(all_simplex_res <= 0, np.inf, all_simplex_res)

    # print(all_simplex_res)
    min_index = np.argwhere(all_simplex_res == np.min(all_simplex_res))

    for i in range(min_index.shape[0]):
        min_index[i][0] = allowed_cols_indexes[min_index[i][0]]

    return min_index
