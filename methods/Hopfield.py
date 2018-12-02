import numpy as np


class Hopfield(object):
    """
    连续型——Hopfield神经网络求解TSP
    1、初始化权值（A,D,U0）
    2、计算N个城市的距离矩阵dxy
    3、初始化神经网络的输入电压Uxi和输出电压Vxi
    4、利用动力微分方程计算：dUxi/dt
    5、由一阶欧拉方法更新计算：Uxi(t+1) = Uxi(t) + dUxi/dt * step
    6、由非线性函数sigmoid更新计算：Vxi(t) = 0.5 * (1 + th(Uxi/U0))
    7、计算能量函数E
    8、检查路径是否合法
    """

    def __init__(self, n, u0, step, func=lambda x:1):
        self.N = n
        self.U0 = u0
        self.step = step
        self.dist_func = func
        self.A = n * n
        self.D = n / 2

    def calc_du(self, V, distance):
        """
        动态方程计算微分方程du
        :param distance: 距离矩阵
        :return: 导数du
        """
        N = self.N
        a = np.sum(V, axis=0) - 1
        b = np.sum(V, axis=1) - 1
        t1 = np.zeros((N, N))
        t2 = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                t1[i, j] = a[j]
        for i in range(N):
            for j in range(N):
                t2[j, i] = b[j]
        c_1 = V[:, 1:N]
        c_0 = np.zeros((N, 1))
        c_0[:, 0] = V[:, 0]
        c = np.concatenate((c_1, c_0), axis=1)
        c = np.dot(distance, c)
        return -self.A * (t1 + t2) - self.D * c

    def calc_U(self, U, du, step):
        """
        更新神经网络的输入电压U
        :param du: 电压导数
        :param step: 步长
        :return: 输入电压
        """
        return U + du * step

    def calc_V(self, U, U0):
        """
        # 更新神经网络的输出电压V
        :param U0: 初始电压
        :return: 输出电压
        """
        return 1 / 2 * (1 + np.tanh(U / U0))

    def calc_energy(self, V, distance):
        """
        计算当前网络的能量
        :param distance: 距离矩阵
        :return: 能量
        """
        t1 = np.sum(np.power(np.sum(V, axis=0) - 1, 2))
        t2 = np.sum(np.power(np.sum(V, axis=1) - 1, 2))
        idx = [i for i in range(1, self.N)]
        idx = idx + [0]
        Vt = V[:, idx]
        t3 = distance * Vt
        t3 = np.sum(np.sum(np.multiply(V, t3)))
        e = 0.5 * (self.A * (t1 + t2) + self.D * t3)
        return e

    def check_path(self, V):
        """
        检查路径的正确性
        :return: 路径
        """
        N = self.N
        route = []
        for i in range(N):
            mm = np.max(V[:, i])
            for j in range(N):
                if V[j, i] == mm:
                    route += [j]
                    break
        return route

    def train(self, num_iter, distance):
        """
        训练网络
        :param num_iter: 迭代次数
        :param distance: 距离矩阵
        :return: 最佳路径，网络能量
        """
        U = 1 / 2 * self.U0 * np.log(self.N - 1) + (2 * (np.random.random((self.N, self.N))) - 1)
        V = self.calc_V(U, self.U0)
        energys = np.array([0.0 for x in range(num_iter)])
        best_distance = np.inf
        best_route = []

        for i in range(num_iter):
            du = self.calc_du(V, distance)
            U = self.calc_U(U, du, self.step)
            V = self.calc_V(U, self.U0)
            energys[i] = self.calc_energy(V, distance)
            route = self.check_path(V)
            if len(np.unique(route)) == self.N:
                route.append(route[0])
                dis = self.dist_func(route)
                if dis < best_distance:
                    best_distance = dis
                    best_route = route
                    print("iter {}: dist:{}, energy:{}".format(i, best_distance, energys[i]))
                    print("route: {}".format(best_route))
                    # H_path = []
                    # [H_path.append((route[i], route[i + 1])) for i in range(len(route) - 1)]
        return best_route, energys
