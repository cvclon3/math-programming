from solver4 import Data, Transport, Answer, Solver
import numpy as np

'''
TODO:
- доделать функцию проверки столбца на условие ограниченности
'''

'''
https://habr.com/ru/articles/474286/
Замечание: Фактически, мы выражаем старые базисные переменные из каждого уравнения системы 
ограничений через остальные переменные и смотрим, в каком уравнении возрастание новой базисной 
переменной быстрее всего даст 0. Попадание в такую ситуацию означает, что мы «наткнулись» 
на новую вершину. Именно поэтому нулевые и отрицательные элементы не рассматриваются, 
т.к. получение такого результата означает, что выбор такой новой базисной переменной будет 
уводить нас из области, вне которой решений не существует.


Поскольку в последнем столбце присутствует несколько минимальных элементов 1, то номер 
строки выбираем по правилу Креко. Метод Креко заключается в следующем. Элементы строк, 
имеющие одинаковые наименьшие значения min=1, делятся на предполагаемые разрешающие элементы, 
а результаты заносятся в дополнительные строки. За ведущую строку выбирается та, в которой 
раньше встретится наименьшее частное при чтении таблицы слева направо по столбцам.
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

    # C[b] - C с индексом b
    ref_plan = table_[1:-1, 0]

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
    ref_plan = table_[-1, 2:]
    allowed_cols_index_ = -1

    if obj.get_cond() == 'min':
        allowed_cols_index_ = np.argwhere(ref_plan.imag == np.max(ref_plan.imag))
        for j in range(allowed_cols_index_.shape[0]):
            if ref_plan[allowed_cols_index_[j]].imag <= 0:
                err_ = 11

    elif obj.get_cond() == 'max':
        allowed_cols_index_ = np.where(ref_plan.imag == np.min(ref_plan.imag))[0]

        for j in range(allowed_cols_index_.shape[0]):
            if ref_plan[allowed_cols_index_[j]].imag >= 0:
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
        26 - хз как такое решать
        '''
    table_ = obj.table_.copy()
    A0_ = table_[1:-1, 1].copy()
    mtx_ = table_[1:-1, 2:].copy()

    assert obj.get_cond() == 'min' or obj.get_cond() == 'max', "Error in [M] get_allowed_rows"

    # Ошибка 23
    # Возникает здесь
    min_index = get_col_row(A0_=A0_, mtx_=mtx_, allowed_cols_indexes_=kwargs['cols'])

    # print(f'RR min_index: {min_index}')

    # return tuple([min_index[0], min_index[1], 0])

    if min_index.shape[0] == 1:
        return tuple([min_index[0][0], min_index[0][1], 0])

    if min_index.shape[0] > 1:
        # # Получаем только индексы столбцов
        # min_index_cols = min_index[:, 0]

        if len(set(min_index[:, 0])) == 1:
            return np.append(kreco_rule(min_index=min_index, mtx=mtx_), 24)
        else:
            return tuple([-1, -1, 26])

        # # Ошибка 24
        # # Получаем уже новые проверенные индексы
        # res = get_col_row_2(mtx=mtx_, allowed_cols_indexes=min_index_cols)
        # if res.shape[0] > 1:
        #     err_ = 24
        # # Ошибка 25
        # elif res.shape[0] < 1:
        #     err_ = 25
        #
        # res = res[0]

        # return tuple([res[0], res[2], err_])

    # Ошибка 23
    if min_index.shape[0] < 1:
        return tuple([-1, -1, 23])


def get_col_row(A0_: np.ndarray, mtx_: np.ndarray, allowed_cols_indexes_: np.ndarray) -> np.ndarray:
    '''
    Код для поиска разрешающей строки
    Возвращает пары чисел - столбец,строка
    '''
    A0: np.ndarray = A0_.copy()
    mtx: np.ndarray = mtx_.copy()
    allowed_cols_indexes: np.ndarray = allowed_cols_indexes_.copy()

    all_simplex_res = np.zeros(shape=(allowed_cols_indexes.shape[0], A0.shape[0]), dtype=np.complex128)

    # print(all_simplex_res)

    for i in range(allowed_cols_indexes.shape[0]):
        for j in range(A0.shape[0]):
            if A0.T[j] == 0 and mtx.T[allowed_cols_indexes[i], j] > 0:
                all_simplex_res[i, j] = 1e-8
            elif A0.T[j] == 0 and mtx.T[allowed_cols_indexes[i], j] < 0:
                all_simplex_res[i, j] = np.inf
            else:
                all_simplex_res[i, j] = A0.T[j] / mtx.T[allowed_cols_indexes[i], j]

    all_simplex_res = np.where(np.isnan(all_simplex_res), np.inf, all_simplex_res)
    # ВОТ ТУТ было <=
    all_simplex_res = np.where(all_simplex_res < 0, np.inf, all_simplex_res)

    min_elem = np.min(all_simplex_res.real)
    if np.isinf(min_elem):
        return np.array([-1, -1])

    # min_index = np.argwhere(all_simplex_res == min_elem)
    # print(f'all_simplex_res1 : {all_simplex_res.real}')
    # print(f'min_index1 : {min_index}')


    # if len(set(min_index[:, 0])) == 1:
    #
    #     # print("AAAAAAAA")
    #     min_index_old = min_index.copy()
    #
    #     for i in range(min_index.shape[0]):
    #         min_index[i, 0] = allowed_cols_indexes[min_index[i, 0]]
    #
    #     kreco_rule = np.zeros(shape=(min_index.shape[0], mtx.shape[1]), dtype=np.complex128)
    #     for i in range(min_index.shape[0]):
    #         kreco_rule[i] = mtx[min_index[i, 1]] / mtx[min_index[i, 0], min_index[i, 1]]
    #
    #     kreco_rule = np.where(np.isnan(kreco_rule), np.inf, kreco_rule)
    #     kreco_rule = np.where(kreco_rule <= 0, np.inf, kreco_rule)
    #
    #     for j in range(kreco_rule.shape[1]):
    #         kreco_rule_min_index = np.where(kreco_rule == np.min(kreco_rule[:, j]))[0]
    #         if kreco_rule_min_index.shape[0] == 1:
    #             print('AAAAAA', [min_index[j, 0], min_index_old[kreco_rule_min_index[0], 1]])
    #             return np.array([min_index[j, 0], min_index_old[kreco_rule_min_index[0], 1]])
    #
    #     return np.array([-1, -1])
    #     # for i in range(allowed_cols_indexes.shape[0]):
    #     #     all_simplex_res[i] = all_simplex_res[i] / mtx.T[allowed_cols_indexes[i]]


    # min_elem = np.min(all_simplex_res.real)
    min_index = np.argwhere(all_simplex_res == min_elem)

    print(f'all_simplex_res1 : {all_simplex_res.real}')
    print(f'min_index1 : {min_index}')

    for i in range(min_index.shape[0]):
        min_index[i, 0] = allowed_cols_indexes[min_index[i, 0]]

    return min_index


def get_col_row_2(mtx: np.ndarray, allowed_cols_indexes: np.ndarray) -> np.ndarray:

    all_simplex_res = np.zeros(shape=(allowed_cols_indexes.shape[0], mtx.shape[1], mtx.shape[0]), dtype=np.complex128)

    # print(all_simplex_res)

    for i in range(allowed_cols_indexes.shape[0]):
        for j in range(mtx.shape[1]):
            # for k in range(mtx.shape[0]):
            # if allowed_cols_indexes[i] == j:
            #     all_simplex_res[i, j] = np.full(shape=(mtx.shape[0],), fill_value=np.inf)
            # else:
            #     all_simplex_res[i, j] = mtx.T[j]/mtx.T[allowed_cols_indexes[i]]
            all_simplex_res[i, j] = mtx.T[j]/mtx.T[allowed_cols_indexes[i]]

    all_simplex_res = np.where(np.isnan(all_simplex_res), np.inf, all_simplex_res)
    # И ВОТ ТУТ!!!!
    all_simplex_res = np.where(all_simplex_res < +0, np.inf, all_simplex_res)

    min_elem = np.min(all_simplex_res)
    if np.isinf(min_elem):
        return np.array([-1, -1, -1])

    print(f'all_simplex_res2 :\n {all_simplex_res.real}')
    min_index = np.argwhere(all_simplex_res == min_elem)

    for i in range(min_index.shape[0]):
        min_index[i, 0] = allowed_cols_indexes[min_index[i, 0]]

    return min_index


def kreco_rule(min_index: np.ndarray, mtx: np.ndarray) -> np.ndarray:

    kreco = np.zeros(shape=(min_index.shape[0], mtx.shape[1]), dtype=np.complex128)

    for i in range(min_index.shape[0]):
        for j in range(mtx.shape[1]):
            kreco[i, j] = mtx[min_index[i, 1], j]/mtx[min_index[i, 1], min_index[i, 0]]

    kreco = np.where(np.isnan(kreco), np.inf, kreco)
    kreco = np.where(kreco <= 0, np.inf, kreco)

    print(f'kreco : \n {kreco.real}')

    for j in range(kreco.shape[1]):
        kreco_min_index = np.where(kreco == np.min(kreco[:, j]))[0]
        if kreco_min_index.shape[0] == 1:
            print(f"ANSWER {min_index[kreco_min_index[0]]}")
            return min_index[kreco_min_index[0]]
        print(f'j : {kreco[:, j].real}')

    return None




# def New_Table_(arr, Stb, Str, ansver):
#     table = arr.copy()
#     ans = ansver.copy()

#     table[Str + 1][0] = arr[0][Stb + 2]


#     table[Str + 1][1:] /= table[Str + 1][Stb + 2]
#     for i in range(1, table.shape[0]):
#         if i == Str + 1:
#             continue
#         for j in range(table.shape[1] - 1):
#             if j == Stb + 1:
#                 table[i][j + 1] = 0
#                 continue
#             table[i][j + 1] = arr[i][j + 1] - arr[Str + 1][j + 1] * arr[i][Stb + 2] / arr[Str + 1][Stb + 2]


#     if arr[Str + 1][0].imag != 0:
#         table[-1][ans[Str] + 2] = 0
#     ans[Str] = Stb


#     return table


def New_Table_(obj: Transport, **kwargs):
    table = obj.table_.copy()
    ans = obj.answer_.copy()
    row = kwargs['row']
    col = kwargs['col']

    table[row + 1][1:] /= table[row + 1][col + 2]
    for i in range(1, table.shape[0]):
        if i == row + 1:
            continue
        for j in range(table.shape[1] - 1):
            if j == col + 1:
                table[i][j + 1] = 0
                continue
            table[i][j + 1] = obj.table_[i][j + 1] - obj.table_[row + 1][j + 1] * obj.table_[i][col + 2] / obj.table_[row + 1][col + 2]

    table[row + 1][0] = obj.table_[0][col + 2]

    # if obj.table_[row + 1][0].imag != 0:
    #     table[-1][ans[row] + 2] = 0
    ans[row] = col
    
    new_tranport = Transport(info=obj.Info_, table=table, answer=ans)

    return new_tranport
