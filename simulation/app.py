# coding=utf-8
import logging
import numpy as np
from typing import List

from simulation import MCSimulation


##  Example for call simulation

class childSim(MCSimulation):
    '''
    子类实现相关加仓算法
    盈利情况下，出现亏损或达到最大连续加仓次数退出
    亏损情况下，出现盈利或达到最大连续加仓次数退出

    InitBalance: 初始资金
    InitPos: 初始仓位
    N: 总模拟次数
    K: 局部次数
    A: 最大连续加仓次数
    X: 加仓倍数
    Flag: 盈利 (PROFIT) 亏损情况(LOSS)
    '''
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int, A: int, X: int) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__A = A
        self.__X = X

    def simu(self) -> float:
        '''
        '''
        return np.random.uniform(-1, 1) * 0.01
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * self.simu()
        count = 0
        balance = self.balance + a
        pos = self.initPos
        logging.info('first trade')
        logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        ret = [a]
        while(a < 0):
            count += 1
            pos *= self.__X    
            if count > self.__A:
                break
            a = self.balance * pos * self.simu()
            balance += a
            ret.append(a)
            logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
    
        logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
        return ret