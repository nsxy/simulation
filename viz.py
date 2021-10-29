import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle

sns.set_style(style='darkgrid')

def load_data(f_path):
    with open(f_path, 'rb') as f:
        return pickle.load(f)



if __name__ == '__main__':

    dir = r'data/'

    w = {}
    wo = {}
    for i in range(15,26):
        w[i] = load_data(dir+'K100A5with%d.json'%i)
        wo[i] = load_data(dir+'without%d.json'%i)

    for i in range(15,26):
        min_bal_wo = min(list(map(lambda x:x['balance_c'], wo[i])))
        min_bal_w = min(list(map(lambda x:x['balance_c'], w[i])))
        min_bal = min(min_bal_wo, min_bal_w)
        plt.plot(sum(map(lambda x:x['balance'][:min_bal] ,wo[i]))/len(wo[i]), linewidth=1)
        
        plt.plot(sum(map(lambda x:x['balance'][:min_bal] ,w[i]))/len(w[i]), linewidth=1)
        plt.legend(labels=('without','with_douzhuan'))
        plt.title('最大加仓%d' % i)
        plt.show()

    for i in range(15,26):
        min_bac_wo = min(list(map(lambda x:x['back_c'], wo[i])))
        min_bac_w = min(list(map(lambda x:x['back_c'], w[i])))
        min_bac = min(min_bac_wo, min_bac_w)
        plt.plot(sum(map(lambda x:x['back'][:min_bac] ,wo[i]))/len(wo[i]), linewidth=1)
        
        plt.plot(sum(map(lambda x:x['back'][:min_bac] ,w[i]))/len(w[i]), linewidth=1)
        plt.legend(labels=('without','with_douzhuan'))
        plt.title('最大加仓%d' % i)
        plt.show()