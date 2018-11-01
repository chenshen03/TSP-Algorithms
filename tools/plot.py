# _*_ coding:utf-8 _*_

import numpy as np
import matplotlib.pyplot as plt


def figure():
    """
    打开绘图窗口
    :return:
    """
    plt.figure()


def plot_city(citys, path):
    """
    绘制将城市坐标以及城市之间的连线
    :param citys: 城市点数据
    :param path:  城市路径数据
    :return:
    """
    paths = np.append(path, path[0])
    plt.clf()
    plt.scatter(citys[:, 0], citys[:, 1], color='g')
    plt.plot(citys[paths, 0], citys[paths, 1], 'r')
    # plt.pause(0.001)
    plt.show()


def plot_iter_curve(scores, title=''):
    """
    绘制每次迭代过程中算法表现的曲线
    :param scores: 每次迭代的算法表现
    :return:
    """
    plt.plot(scores)
    plt.title(title)
    plt.xlabel('iter t')
    plt.ylabel('score d')
    plt.show()
