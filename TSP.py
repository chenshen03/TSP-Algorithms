# _*_ coding:utf-8 _*_

import numpy as np
from datas.citydata import china_citys
from tools.plot import figure, plot_city, plot_iter_curve
from methods.GA import GA
from methods.SA import SA


class TSP(object):
    """
    旅行商问题
    """

    def __init__(self, plot=1):
        self.init_citys()
        self.n = len(self.citys)
        self.init_dist()
        self.best_path = None
        self.plot = plot

    def init_citys(self):
        """
        加载城市数据
        :return: 城市数据
        """
        self.citys = china_citys()


    def init_dist(self):
        """
        根据城市数据计算每个城市间的距离
        :return: 城市的距离矩阵
        """
        self.Dist = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(i, self.n):
                self.Dist[i][j] = self.Dist[j][i] = np.linalg.norm(self.citys[i] - self.citys[j])

    def calculate_dist(self, path):
        """
        计算路径path下的城市总距离
        :param path: 完成TSP问题的一个城市路径
        :return: 城市总距离
        """
        dist_sum = 0.0
        for i in range(self.n - 1):
            dist_sum = dist_sum + self.Dist[path[i]][path[i + 1]]
        dist_sum = dist_sum + self.Dist[path[self.n - 1]][path[0]]
        return dist_sum

    def match_fun(self, gene):
        """
        遗传算法中的适应性计算函数
        :return: 适应性函数
        """
        return 1.0 / self.calculate_dist(gene)

    def search(self, method='SA'):
        """
        利用method解决TSP问题
        :param method: 采用的算法
        :return:
        """

        if self.plot: figure()

        scores = []

        # 模拟退火算法
        if method == 'SA':
            sa = SA(self.n, energy_fun=self.calculate_dist)
            # sa.search()

            while sa.T >= 0.1:
                sa.anneal()

                score = sa.energy(sa.S)
                scores.append(score)
                print('search on T:{}'.format(sa.T))
                print(score)

                if self.plot:
                    # plot_city(self.citys, sa.S)
                    pass

                # 温度衰减
                sa.T = sa.T * sa.alpha

            self.best_path = sa.S

        # 遗传算法
        elif method == 'GA':
            ga = GA(self.n, 100, 0.8, 0.05, self.match_fun)
            # ga.evolution()

            while ga.generation < 3000:
                ga.generate_next()

                score = 1.0 / ga.best.score
                scores.append(score)
                print("generation: {}".format(ga.generation))
                print(score)

                if (ga.generation%30 == 0) and self.plot:
                    # plot_city(self.citys, ga.best.gene)
                    pass

            self.best_path =  ga.best.gene

        print(self.best_path)

        if self.plot:
            plot_iter_curve(scores, 'China Citys')
            plot_city(self.citys, self.best_path)


if __name__ == '__main__':
    tsp = TSP()
    tsp.search('GA')