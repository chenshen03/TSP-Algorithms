# _*_ coding:utf-8 _*_

import numpy as np


class SA(object):
    """
    模拟退火算法
    """
    
    def __init__(self, n, T=280, L_len=100, alpha=0.92, energy_fun=lambda S:1):
        self.n = n
        self.T = T                      # 初始温度
        self.L = L_len * self.n         # 每个温度下的迭代次数
        self.alpha = alpha             # 温度下降缩减因子
        self.S = np.arange(self.n)      # 初始状态
        self.energy = energy_fun

    def neighbors(self, S):
        """
        采用两点交换法从状态S的邻域中随机选择
        :param S: 当前状态
        :return: 随机选择的状态
        """
        S_neibor = np.copy(S)
        u = np.random.randint(0, self.n)
        v = np.random.randint(0, self.n)
        while u == v:
            v = np.random.randint(0, self.n)
        S_neibor[u], S_neibor[v] = S_neibor[v], S_neibor[u]
        return S_neibor

    def neighbors2(self, S):
        """
        采用2交换法从状态S的邻域中随机选择
        :param S: 当前状态
        :return: 随机选择的状态
        """
        S_neibor = np.copy(S)
        u = np.random.randint(0, self.n)
        v = np.random.randint(0, self.n)
        if u > v:
            u, v = v, u
        while u == v:
            v = np.random.randint(0, self.n)
        temp = S_neibor[u:v]
        S_neibor[u:v] = temp[::-1]
        return S_neibor

    def anneal(self):
        """
        一步退火过程
        :return:
        """
        print('search on T:{}'.format(self.T))
        for i in range(self.L):
            E_pre = self.energy(self.S)
            S_now = self.neighbors2(self.S)
            E_now = self.energy(S_now)
            if (E_now < E_pre) or (np.exp((E_pre - E_now) / self.T) >= np.random.rand()):
                self.S = S_now

    def search(self):
        """
        模拟退火搜索过程
        :return: 搜索结束后的解
        """
        Ts = []
        Es = []
        while self.T >= 0.1:
            print('search on T:{}'.format(self.T))
            for i in range(self.L):
                E_pre = self.energy(self.S)
                S_now = self.neighbors2(self.S)
                E_now = self.energy(S_now)
                if (E_now < E_pre) or (np.exp((E_pre - E_now) / self.T) >= np.random.rand()):
                    self.S = S_now

            Ts.append(self.T)
            E_now = self.energy(self.S)
            Es.append(E_now)
            print(E_now)

            # 判断是否达到终止状态
            self.T = self.T * self.alpha
        print(self.S)
        print('finished\n')

        return Ts, Es

