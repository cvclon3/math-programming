from solver4 import Data, Transport, Info
import numpy as np


def sum_base_vars(mtx, base_i):
    """
    Нахождение суммы всех базисных векторов
    """
    # Инициализируем нулевой массив с количеством элементов, равным количеству строк в mtx
    sum_ = np.zeros(mtx.shape[0])

    # Проходим по каждому индексу в векторе базисных векторов
    for i in base_i:
        # Добавляем соответствующий столбец матрицы mtx к сумме
        sum_ = sum_ + mtx.T[int(i)]

    # Возвращаем полученную сумму
    return sum_


def find_base_x(mtx):
    """ 
    Нахождение индексов базисных переменных
    """
    # Получаем количество столбцов в матрице
    cols_size = mtx.shape[1]

    # Получаем количество строк в матрице
    row_size = mtx.shape[0]

    # Копируем исходную матрицу для модификации
    mtx_ = mtx.copy()

    # Обходим все элементы матрицы
    for i in range(row_size):
        for j in range(cols_size):
            # Если элемент не равен 0 и не равен 1, заменяем его на бесконечность
            if mtx[i, j] != 0 and mtx[i, j] != 1:
                mtx_[i, j] = 2
    # Транспонируем матрицу
    mtx_ = mtx_.T

    # Инициализируем массив для хранения индексов базисных переменных
    res = np.array([], dtype=int)

    # Инициализируем массив для суммирования
    sum_ = np.zeros(row_size)

    # Создаем массив, заполненный единицами
    ones = np.ones(row_size)

    # Обходим каждый столбец
    for i in range(cols_size):
        # Суммируем элементы в текущем столбце
        sum_in_cols = np.sum(mtx_[i])

        # Если сумма в столбце равна 1
        if sum_in_cols == 1:
            # Проверяем, что сумма не превышает единичный вектор
            if np.all(sum_ + mtx_[int(i)] <= ones):
                # Добавляем индекс текущего столбца в результат
                res = np.append(res, i)
                # Обновляем сумму
                sum_ = sum_ + mtx_[int(i)]
    # Возвращаем массив индексов базисных переменных
    return res


def init_symb_arr_(data):
    """
    Определение новых переменных в зависимости от знака
    """
    # Копируем матрицу из объекта data
    mtx = data.Ai_mtx_.copy()

    # Получаем количество строк в матрице
    size_ = data.Ai_mtx_.shape[0]

    # Проходим по всем элементам массива символов
    for i in range(data.Symb_arr_.shape[0]):
        # Инициализируем массив для новых столбцов
        cols = np.zeros(size_)

        # Если символ равен '>=', добавляем новый столбец со значениями -1
        if data.Symb_arr_[i] == '>=':
            cols[i] = -1

            # Добавляем новый столбец в матрицу
            mtx = np.column_stack((mtx, cols))

            # Добавляем 0 в опорный план
            data.Zi_mtx_ = np.append(data.Zi_mtx_, 0)

        # Если символ равен '<=', добавляем новый столбец со значениями 1
        if data.Symb_arr_[i] == '<=':
            cols[i] = 1

            # Добавляем новый столбец в матрицу
            mtx = np.column_stack((mtx, cols))

            # Добавляем 0 в опорный план
            data.Zi_mtx_ = np.append(data.Zi_mtx_, 0)
    # Если символ равен '=', то ничего не делаем.
    # Возвращаем модифицированную матрицу
    return mtx


def add_amega_vars(data, mtx, sum_amega_i):
    """
    Добавление в симплексную таблицу недостающих базисных переменных (амега)
    и добавление каэфициентов в опорный план
    """
    # Копируем матрицу для модификации
    mtx_ = mtx.copy()

    # Получаем количество переменных амега
    size_ = sum_amega_i.shape[0]

    # Создаем единичную матрицу размером (size_ x size_)
    vectors_to_find = np.identity(size_)

    # Проходим по всем элементам sum_amega_i
    for i in range(size_):
        # Если элемент равен 0, добавляем новый столбец в матрицу
        if sum_amega_i[i] == 0:
            mtx_ = np.column_stack((mtx_, vectors_to_find[i]))

            # В зависимости от условия, добавляем в Zi_mtx_ соответствующее значение
            if data.Cond_ == "min":
                data.Zi_mtx_ = np.append(data.Zi_mtx_, 1j)  # Добавляем 1j для минимизации
                continue
            data.Zi_mtx_ = np.append(data.Zi_mtx_, -1j)  # Добавляем -1j для максимизации

    # Возвращаем модифицированную матрицу
    return mtx_


def add_left_part(mtx, base_i_in_extended_mtx, bi_mtx_):
    # Копируем матрицу mtx без первой строки
    mtx_ = mtx.copy()[1:]

    # Инициализируем список для arrCA
    arrCA = np.zeros((len(mtx_) + 1, 2)).tolist()

    # Проходим по всем индексам базисных переменных
    for i in range(len(base_i_in_extended_mtx)):
        # Находим индекс строки, где в матрице mtx_ есть 1 в указанном столбце
        index_of_one = np.where(mtx_.T[base_i_in_extended_mtx[i]] == 1)[0]

        # Заполняем второй элемент массива arrCA значением из Bi_mtx_
        arrCA[i + 1][1] = bi_mtx_[int(i)]

        # Заполняем первый элемент arrCA значением из первой строки mtx
        arrCA[index_of_one[0] + 1][0] = mtx[0][base_i_in_extended_mtx[i]]

    # Возвращаем объединенную матрицу, состоящую из arrCA и mtx
    return np.concatenate((arrCA,  mtx), axis=1)


def delta_i(arr):
    """
    Опеределение значений индексной строки
    """
    # Проходим по всем столбцам, кроме последнего
    for i in range(arr.shape[1] - 1):
        arr_i = 0  # Инициализируем переменную для накопления суммы

        # Проходим по всем строкам, кроме первого и последнего
        for j in range(arr.shape[0] - 2):
            # Накопление суммы произведений i-того столбца и соответствующего первого столбца
            arr_i += arr[j + 1][i + 1] * arr[j + 1][0]

        # Вычитаем из суммы элемент соответствующий номеру столбца
        arr[-1][i + 1] = arr_i - arr[0][i + 1]

    # Возвращаем модифицированный массив
    return arr


def prepare_data(data: Data) -> Transport:
    # Создаем класс info который будет содержать основную информацию о задаче
    info = Info(cond=data.Cond_, ineq_num=data.Ai_mtx_.shape[0], var_num=data.Ai_mtx_.shape[0])

    mtx = init_symb_arr_(data)
    #Добаавление иксов в зависимости от знака
    baseI = find_base_x(mtx)
    #Нахождение базисных переменных
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
    mtx = delta_i(mtx)
    print(mtx)

    res = Transport(info=info, table=mtx, answer=baseI_in_extended_mtx)

    return res

            