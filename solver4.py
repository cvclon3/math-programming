import numpy as np


class Data:
    def __init__(self, ai: np.ndarray, bi: np.array, zi: np.array, symb: np.array, cond: str):
        # Элементы основной матрицы
        self.Ai_mtx_ = ai
        
        # Столбец правых частей уравнений
        self.Bi_mtx_ = bi
        
        self.Zi_mtx_ = zi
        self.Symb_arr_ = symb
        self.Cond_ = cond


class Info:
    '''
    Класс содержащий базовые знания о задаче
    такие как усовие (cond - min/max)
    кол-во переменных
    кол-во строк неравенств
    '''
    def __init__(self, cond: str, var_num: int, ineq_num: int):
        # Условие задачи (min or max)
        self.cond_ = cond

        # Кол-во переменных
        self.var_num_ = var_num

        # Кол-во неравенств
        self.ineq_num_ = ineq_num


class Transport:
    '''
    Транспортный класс для таблицы - матрицы
    Также содержит флаги, которые говорят о том решена ли М-задача и обычная задача
    '''
    def __init__(self, info: Info, table: np.ndarray, answer: np.ndarray, is_m_solved: bool = False, is_solved: bool = False):
        # Условие задачи (min or max)
        self.Info_ = info

        # Таблица - матрица
        self.table_: np.ndarray = table

        # Вектор ответов
        self.answer_: np.ndarray = answer
        
        # Флаг, который говорит о том решена ли М-задача
        self.is_m_solved_: bool = is_m_solved
    
        # Флаг, который говорит о том решена ли обычная задача
        self.is_solved: bool = is_solved

    def get_cond(self):
        return self.Info_.cond_


class Answer:
    '''
    Класс, содержащий массив итераций (транспортных классов) - ответ, 
    а также сообщения о различных ошибка или предупреждения (например о том,
    что задача на поиск минимума неограничена снизу)
    '''
    def __init__(self, answer: np.array, msg: list):
        self.answer_ = answer
        self.msg_ = msg


class Solver:
    def __init__(self, data: Data):
        # Условия задачи
        self.data_ = data
        
        # Массив содержащий итерации (транспортные классы) - массив ответов
        self.solution_: np.array[Transport] = np.array(prepare_data(data=self.data_))

    def solve(self) -> Answer:
        '''
        Метод для решения задачи
        Возвращает класс Answer
        '''
        while self.solution_[-1]:

            self.solution_ = np.append(self.solution_, calc_iter(self.solution_[-1]))
            
        return Answer(answer=self.solution_, msg='')



def prepare_data(data: Data) -> Transport:
	pass

def calc_iter(obj: Transport, *args, **kwargs) -> Transport:
     pass

