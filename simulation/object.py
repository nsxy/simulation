# coding=utf-8
import logging
import numpy as np
from typing import List
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from simulation.utils import calcPerformance


class MCSimulation(ABC):
    '''Monte Carlo Simulation for the position management

    balance: init balance 
    initPos: init position
    '''
    def __init__(self, InitBalance: float, InitPos: float, N: int, K: int) -> None:
        '''
        InitBalance: init balance
        InitPos: init position
        N: total num of simulation
        K: local cum num of trading
        '''
        self.__balance = InitBalance
        self.__initPos = InitPos
        self.__totalCount = N
        self.__accmuCount = K

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def initPos(self) -> float:
        return self.__initPos

    @abstractmethod
    def game(self) -> List[float]:
        # abstract method implemented in the child class
        logging.error('not implemented func for child class')
        raise NotImplementedError('Need implemented for child class')

    def run(self) -> None:
        '''public method to get internal pnl and balance
        calc data in the method
        '''
        self._pnl = [self.game() for _ in range(self.__totalCount)]
        self.__pnl = np.array([sum(x) for x in self._pnl])
        self._balances = np.cumsum(np.insert(sum(self._pnl, []), 0, self.__balance))    ## each trading
        self.__balances = np.cumsum(np.insert(self.__pnl, 0, self.__balance))           ## each gamer

        pnl = np.array(sum(self._pnl, []))
        cnt = len(pnl)
        self.__groupInt = cnt // self.__accmuCount
        if cnt % self.__accmuCount:
            subsetInt = self.__groupInt * self.__accmuCount
            partialPnL = np.split(pnl[:subsetInt], self.__groupInt)
        else:
            partialPnL = np.split(pnl, self.__groupInt)
        
        self._partialPnL = np.mean(partialPnL, axis=1)
        self._partialBalance = np.cumsum(np.insert(self._partialPnL, 0, self.__balance))

    def getStat(self) -> None:
        '''get performance for the simulation
        plot for the PnL and Drawdown
        
        #TODO(): update the plots
        '''
        if not hasattr(self, '_pnl'):
            self.run()
        logging.info('calc performance:')
        p = calcPerformance(self._balances)
        logging.info('calc gamer performance:')
        ps = calcPerformance(self.__balances)
        logging.info('calc partial performance:')
        partialP = calcPerformance(self._partialBalance)
        partialWRatio = np.sum(self._partialPnL > 0) / self.__groupInt
        if np.sum(self._partialPnL < 0) < 1:
            partialPLR = np.Infinity
        else:
            partialPLR = -np.sum(self._partialPnL[self._partialPnL > 0]) / np.sum(self._partialPnL[self._partialPnL < 0])
        logging.info('partial winning ratio: {:.4f}, profit loss ratio: {:.4f}'.format(partialWRatio, partialPLR))

        ax1 = plt.subplot(231)
        ax1.plot(self._balances)
        plt.xlim(0, len(self._balances))
        plt.grid(axis='y')
        plt.title('PnL')

        ax2 = plt.subplot(232)
        ax2.plot(self.__balances)
        plt.xlim(0, self.__totalCount)
        plt.grid(axis='y')
        plt.title('Gamer PnL')
        
        ax3 = plt.subplot(233)
        ax3.plot(self._partialBalance)
        plt.xlim(0, self.__groupInt)
        plt.grid(axis='y')
        plt.title('Partial PnL')

        ax4 = plt.subplot(234)
        ax4.plot(-p.dd)
        plt.xlim(0, len(p.dd))
        plt.grid(axis='y')
        plt.title('MaxDrawDown')

        ax5 = plt.subplot(235)
        ax5.plot(-ps.dd)
        plt.xlim(0, self.__totalCount)
        plt.grid(axis='y')
        plt.title('Gamer MaxDrawDown')

        ax6 = plt.subplot(236)
        ax6.plot(-partialP.dd)
        plt.xlim(0, self.__totalCount // self.__accmuCount)
        plt.grid(axis='y')
        plt.title('Partial MaxDrawDown')
        plt.show()