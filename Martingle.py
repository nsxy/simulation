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
    
class Position():
    '''
    initBalance: init balance
    pos: position
    R: Time for reborn
    '''
    def __init__(self, initBalance, pos, R:int=50):
        self.initBalance = initBalance
        self.__balance = initBalance
        self.__pos = pos
        self.__R = R
        self.__t = 0
        
    @property
    def balance(self) -> float:
        return self.__balance
    
    @property
    def pos(self) -> float:
        return self.__pos
    
    @pos.setter
    def pos(self, value):
        self.__pos = value
    
    @property
    def timeRemain(self) -> int:
        return self.__t
    
    def getReturn(self, market) -> float:
        '''
        market: The current marketing price
        --------------------
        The operation will stop if you sign the account "dead", and will cost {R:int=50} times to reborn
        --------------------
        return: The return with current balance, position and market
        '''
        if 0 < self.__t:
            logging.info("Im dead and waiting for reborn, {:d} remained".format(self.__t))
            self.__t -= 1
            if self.__t == 0:
                if 0 < market:
                    logging.info("Im back!")
                else:
                    logging.info("Market is not positive, one more wait!")
                    self.__t += 1
            return 0
                    
        pnl = self.initBalance * self.__pos * market
        self.__balance = pnl + self.__balance
        return pnl
    
    def dead(self):
        self.__t = self.__R
        
        
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
    Flag: 盈利 (PROFIT) 或 亏损(LOSS) 加仓
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

    def game(self, mainBrunch=True) -> List[float]:
        # init status
        p = Position(self.balance, self.initPos, self.__R)
        count = 0
        ret = []
        logging.info('first trade')
        while True:
            # marketing price
            market = simu()
            # calc returns
            pnl = p.getReturn(market)  # return 0 if trigger 斗转星移
            if pnl:
                ret.append(pnl)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(p.pos, pnl, p.balance))
                # 策略
                if (pnl > 0)!=self.__Flag.value or self.__L <= count:
                    logging.info('return total pnl: {:.2f}'.format(p.balance - self.balance))
                    return ret
                else:
                    count += 1
                    p.pos *= self.__X  # 仓位调整
                    
                if self.__A == count:  # trigger 斗转星移 
                    p.dead()
                    
                    
                    
                
if __name__ == '__main__':
    m = Martingale(Flag=FLAG.LOSS,L=7)  # double the position when loss
    m.getStat()