# coding=utf-8
from simulation import MCSimulation
from enum import Enum
from typing import List
import numpy as np
import logging

WRatio = 2                      ## 百分比 止盈率
LRatio = -2                     ## 百分比 止损率
WLRatio = 0.5                   ## 胜率

def simu() -> float:
    return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01

class FLAG(Enum):
    LOSS = False
    PROFIT = True
    
class Martingale(MCSimulation):
    '''
    子类实现相关加仓算法
    保证在连续 A 次 Flag 情况下transform the risk to the future and wait to reborn 

    InitBalance: 初始资金
    InitPos: 初始仓位
    N: 总模拟次数
    K: 局部次数
    A: 最大连续加仓次数
    X: 加仓倍数
    R: Time for reborn
    L: Reach the limitation stop doubling the position and reinit
    Flag: 盈利 (PROFIT) 亏损情况(LOSS)
    '''
    def __init__(self,
                 InitBalance: float=100, 
                 InitPos: float=0.2, 
                 N: int=10000, 
                 K: int=100, 
                 A: int=5, 
                 X: int=2, 
                 R: int=50,
                 L: int=10,
                 Flag: FLAG=FLAG.LOSS) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__A = A
        self.__X = X
        self.__R = R
        self.__L = L
        self.__Flag = Flag

    def game(self) -> List[float]:
        # init status
        stat = {
            't': 0,
            'count': 0,
            'balance': self.balance,
            'pos': self.initPos
        }
        ret = []
        logging.info('first trade')
        while True:
            if 0 < stat['t']:
                logging.info("Im dead and waiting for reborn, {:d} remained".format(stat['t']))
                if stat['t']:
                    stat['t'] -= 1
                    continue
                else:
                    logging.info("Im back!")
                
            # marketing price
            market = simu()
            # calc returns
            pnl = self.balance * stat['pos'] * market
            ret.append(pnl)
            # update status
            stat['balance'] = pnl + self.balance
            logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(stat['pos'], pnl, stat['balance']))
            if (pnl > 0)!=self.__Flag.value or self.__L <= stat['count']:
                logging.info('return total pnl: {:.2f}'.format(stat['balance'] - self.balance))
                return ret    
            else:
                stat['count'] += 1
                stat['pos'] *= self.__X

            if self.__A == stat['count']: 
                stat['t'] = self.__R
                
if __name__ == '__main__':

    m = Martingale(Flag=FLAG.LOSS)  # double the position when loss
    m.getStat()