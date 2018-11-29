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


def draw_H_and_E(citys, H_path, energys):
    """
    可视化画出哈密顿回路和能量趋势
    :param citys:
    :param H_path:
    :param energys:
    :return:
    """
    fig = plt.figure()
    # 绘制哈密顿回路
    ax1 = fig.add_subplot(121)
    plt.xlim(0, 7)
    plt.ylim(0, 7)
    for (from_, to_) in H_path:
        p1 = plt.Circle(citys[from_], 0.2, color='red')
        p2 = plt.Circle(citys[to_], 0.2, color='red')
        ax1.add_patch(p1)
        ax1.add_patch(p2)
        ax1.plot((citys[from_][0], citys[to_][0]), (citys[from_][1], citys[to_][1]), color='red')
        # ax1.annotate(to_, xy=citys[to_], xytext=(-8, -4), textcoords='offset points', fontsize=8)
    ax1.axis('equal')
    ax1.grid()
    # 绘制能量趋势图
    ax2 = fig.add_subplot(122)
    ax2.plot(np.arange(0, len(energys), 10), energys[::10], color='red')
    plt.show()