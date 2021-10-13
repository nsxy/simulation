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
    pnl = s.diff()
    ms = s.cummax()
    dd = 1 - s / ms
    p = Performance(pnl.mean(), pnl.std(), np.asarray(dd.cummax()))
    logging.info('average profit: {:>16.4f}\nstandard deviation: {:>12.4f}\nmax drawdown: {:>18.4f}\n'.format(p.avg, p.std, p.mdd))
    return p
