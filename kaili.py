# coding=utf-8
import logging
import numpy as np
import pandas as pd
from typing import List
from matplotlib import pyplot as plt

from simulation import MCSimulation, utils

class KaliSimu(MCSimulation):

    def __init__(self, 
                init_balance: float = 10000,
                simu_count: int = 10000,
                winning_rate: float = 0.52,
                profit_rtn: float = 1.5,
                loss_rtn: float = -1.0,
                ) -> None:
        super().__init__(init_balance, 0.0, simu_count, 100)
        self.__p = winning_rate
        self.__profit_rtn = profit_rtn
        self.__loss_rtn = loss_rtn
        self._balance = init_balance
        self._total_cnt = simu_count
        self.__best_pos = self.__p + self.__loss_rtn * (1 - self.__p) / (self.__profit_rtn)

    def simu(self) -> float:
        '''
        random generate pnl
        '''
        pr = self.__profit_rtn
        lr = self.__loss_rtn
        return (lr + (pr - lr) * np.random.binomial(1, self.__p)) * 0.01
    
    def game(self) -> List[float]:
        
        pos = self.__best_pos
        balance = self._balance
        pnl = [balance]
        for _ in range(self._total_cnt):
            pnl.append(balance * self.simu() * pos)
        ret = np.cumsum(pnl)
        logging.info('return trade')
        return ret

    def set_best_pos(self, pos: float) -> None:
        self.__best_pos = pos

    def run(self, cnt: int=5) -> None:

        ret = [self.game() for _ in range(cnt)]
        dat = pd.DataFrame(ret).T
        dat.columns = ['simu_{}'.format(i) for i in range(cnt)]
        utils.calcPerformance(dat.mean(axis=1))
        dat.plot(grid='on')
        plt.legend(ncol=5)
        plt.show()
        # pos_range = (self.__best_pos + delta * n for n in range(-cnt, cnt+1))
        # pos_range = [x for x in pos_range if x > 0]
        # ret = []
        # for pos in pos_range:
        #     self._balance = self.balance
        #     self.set_best_pos(pos)
        #     ret.append(self.game())
        
        # dat = pd.DataFrame(ret).T
        # dat.columns = ['best_pos_{:.2f}'.format(i) for i in pos_range]
        # dat.plot(grid='on')
        # plt.show()

if __name__ == '__main__':
    k = KaliSimu(simu_count=50000, winning_rate=0.52)
    k.run(20)

