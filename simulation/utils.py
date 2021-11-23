# coding=utf-8
import logging
import numpy as np
import pandas as pd

class Performance(object):
    '''
    avg: average pnl
    std: standard deviation for pnl
    dd: drawdown series
    mdd: max drawdown
    '''
    def __init__(self, avg: float, std: float, dd: np.array) -> None:
        self.__avg = avg
        self.__std = std
        self.__dd = dd
        self.__mdd = np.max(dd)

    @property
    def avg(self) -> float:
        return self.__avg

    @property
    def std(self) -> float:
        return self.__std
    
    @property
    def dd(self) -> np.array:
        return self.__dd
    
    @property
    def mdd(self) -> float:
        return self.__mdd



def calcPerformance(arr: np.array) -> Performance:
    '''
    input: balance series
    '''
    s = pd.Series(arr)
    rs = s / s.shift(1) - 1
    ms = s.cummax()
    dd = 1 - s / ms
    p = Performance(rs.mean(), rs.std(), np.asarray(dd.cummax()))
    totalRtn = arr[len(arr) - 1] / arr[0] - 1
    logging.warning('\nreturn: {:20.4%}\naverage return: {:>16.4%}\nstandard deviation: {:>12.4f}\nmax drawdown: {:>18.4%}\n'.format(totalRtn, p.avg, p.std, p.mdd))
    return p
