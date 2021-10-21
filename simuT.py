# coding=utf-8
import logging
import numpy as np
from enum import Enum
from typing import List

from simulation import MCSimulation


WRatio = 1                      ## 百分比 止盈率
LRatio = -1                     ## 百分比 止损率
WLRatio = 0.5                  ## 胜率

def simu() -> float:
    return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
    # return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
    # return np.random.uniform(-1, 1) * 0.01


class FLAG(Enum):
    LOSS = 0
    PROFIT = 1


class childSim1_0(MCSimulation):
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
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int, A: int, X: int, Flag: FLAG) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__A = A
        self.__X = X
        self.__Flag = Flag

    def simu(self) -> float:
        '''
        随机产生投资收益  暂时使用全局 simu 函数
        '''
        # return np.random.uniform(-1, 1) * 0.01
        return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
        # return (-2 + 4 * np.random.binomial(1, 0.5)) * 0.01
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * simu()
        count = 0
        balance = self.balance + a
        pos = self.initPos
        logging.info('first trade')
        logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        ret = [a]

        if self.__Flag == FLAG.PROFIT:
            while(a > 0):
                count += 1
                pos *= self.__X
                if count > self.__A:
                    break
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        else:
            while(a < 0):
                count += 1
                pos *= self.__X    
                if count > self.__A:
                    break
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        
        logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
        # return balance - self.balance
        return ret


class childSim1_1(MCSimulation):

    '''
    子类实现相关加仓算法
    保证在连续 A 次 Flag 情况下退出 

    InitBalance: 初始资金
    InitPos: 初始仓位
    N: 总模拟次数
    K: 局部次数
    A: 最大连续加仓次数
    X: 加仓倍数
    Flag: 盈利 (PROFIT) 亏损情况(LOSS)
    '''
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int, A: int, X: int, Flag: FLAG) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__A = A
        self.__X = X
        self.__Flag = Flag

    def simu(self) -> float:
        '''
        暂时使用全局 simu 函数
        '''
        # return np.random.uniform(-1, 1) / 100
        return (-2 + 4 * np.random.binomial(1, 0.55)) * 0.01
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * simu()
        count = 0
        balance = self.balance + a
        pos = self.initPos
        ret = [a]
        logging.info('first trade')
        logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))

        if self.__Flag == FLAG.PROFIT:
            while(True):
                if a > 0:
                    count += 1
                    pos *= self.__X
                else:
                    count = 0
                    pos = self.initPos
                
                if count > self.__A:    ##  or balance < 0
                    logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
                    # return balance - self.balance
                    return ret
                
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        else:
            while(True):
                if a < 0:
                    count += 1
                    pos *= self.__X
                else:
                    count = 0
                    pos = self.initPos
                
                if count > self.__A:    ##  or balance < 0
                    logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
                    # return balance - self.balance
                    return ret
                
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))


class childSim1_2(MCSimulation):

    '''
    子类实现相关加仓算法
    保证在连续 A 次 Flag 情况下退出 

    InitBalance: 初始资金
    InitPos: 初始仓位
    N: 总模拟次数
    K: 局部次数
    A: 最大连续加仓次数
    X: 加仓倍数
    Flag: 盈利 (PROFIT) 亏损情况(LOSS)
    '''
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int, A: int, X: int, Flag: FLAG) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__A = A
        self.__X = X
        self.__Flag = Flag

    def simu(self) -> float:
        '''
        暂时使用全局 simu 函数
        '''
        return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
        # return np.random.uniform(-1, 1) / 100
        # return (-2 + 4 * np.random.binomial(1, 0.55)) * 0.01
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * simu()
        count = 0
        balance = self.balance + a
        pos = self.initPos
        ret = [a]
        logging.info('first trade')
        logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))

        if self.__Flag == FLAG.PROFIT:
            while(True):
                if a > 0:
                    count += 1
                    pos *= self.__X
                else:
                    count = 0
                    # pos = self.initPos    ## 仓位不回归
                
                if count > self.__A:    ##  or balance < 0
                    logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
                    # return balance - self.balance
                    return ret
                
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        else:
            while(True):
                if a < 0:
                    count += 1
                    pos *= self.__X
                else:
                    count = 0
                    # pos = self.initPos    ## 仓位不回归
                
                if count > self.__A:    ##  or balance < 0
                    logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
                    # return balance - self.balance
                    return ret
                
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))


class childSim2(MCSimulation):

    '''
    子类实现相关加仓算法
    在连续 A 次 Flag 情况下或达到最大开仓次数退出 

    InitBalance: 初始资金
    InitPos: 初始仓位
    N: 总模拟次数
    K: 局部次数
    A: 最大连续加仓次数
    B: 最大开仓次数
    X: 加仓倍数
    Flag: 盈利 (PROFIT) 亏损情况(LOSS)
    '''
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int, A: int, B: int, X: int, Flag: FLAG) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__A = A
        self.__B = B
        self.__X = X
        self.__Flag = Flag

    def simu(self) -> float:
        '''
        暂时使用全局 simu 函数
        '''
        return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
        # return np.random.uniform(-1, 1) / 100
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * simu()
        count = 0
        balance = self.balance + a
        pos = self.initPos
        ret = [a]
        logging.info('first trade')
        logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))

        if self.__Flag == FLAG.PROFIT:
            for _ in range(1, self.__B):
                if a > 0:
                    count += 1
                    pos *= self.__X
                else:
                    count = 0
                    pos = self.initPos
                
                if count > self.__A:
                    break
                
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        else:
            for _ in range(1, self.__B):
                if a < 0:
                    count += 1
                    pos *= self.__X
                else:
                    count = 0
                    pos = self.initPos
                
                if count > self.__A:
                    break
                
                a = self.balance * pos * simu()
                balance += a
                ret.append(a)
                logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        
        logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
        # return balance - self.balance
        return ret


class SimV3(MCSimulation):
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int, X: int) -> None:
        super().__init__(InitBalance, InitPos, N, K)
        self.__X = X
    
    def simu(self) -> float:
        return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * simu()
        balance = self.balance + a
        pos = self.initPos
        ret = [a]
        logging.info('first trade')
        logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))

        if a > 0:
            logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
            return ret
        
        pos = self.initPos * self.__X
        while (True):

            a = self.balance * pos * simu()
            balance += a
            ret.append(a)
            logging.info('pos: {:.0%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))

            if a < 0:
                pos *= self.__X
            elif balance > self.balance:
                logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
                return ret


class SimV4(MCSimulation):

    multi = {1: 0.1, 2: 0.1, 3: 10}

    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int) -> None:
        super().__init__(InitBalance, InitPos, N, K)
    
    def simu(self) -> float:
        return (LRatio + (WRatio - LRatio) * np.random.binomial(1, WLRatio)) * 0.01
    
    def game(self) -> List[float]:
        a = self.balance * self.initPos * simu()
        balance = self.balance + a
        pos = self.initPos
        ret = [a]
        logging.info('first trade')
        logging.info('pos: {:.1%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
        
        cnt = 0
        while (a < 0):
            cnt += 1
            pos *= (SimV4.multi.get(cnt, 2) + 1)
            a = self.balance * pos * simu()
            balance += a
            ret.append(a)
            logging.info('pos: {:.2%}, pnl: {:.2f}, balance: {:.2f}.'.format(pos, a, balance))
    
        logging.info('return total pnl: {:.2f}'.format(balance - self.balance))
        return ret


if __name__ == '__main__':

    # c  = childSim1_0(10000, 0.002, 10000, 100, 30, 2, FLAG.LOSS)
    # c  = childSim1_1(10000, 0.002, 1000, 100, 3, 2, FLAG.PROFIT)
    # c  = childSim1_2(10000, 0.002, 1000, 100, 2, 2, FLAG.PROFIT)
    # c  = childSim2(10000, 0.002, 10000, 100, 10, 20, 2, FLAG.LOSS)
    # c  = SimV3(10000, 0.002, 1000, 100, 2)
    c  = SimV4(10000, 0.002, 10000, 100)
    c.getStat()
    # kws = {'max_contious_buy_cnt': 2, 'winning_rate': WLRatio, 'WRatio': WRatio, 'LRatio': -LRatio, 
    #         'multiple': 2, 'flag': FLAG.PROFIT, 'total_strategy_num': 20}
    # c.generateDF(1, kws)
    # c.generateGDF(1, 1000, kws)