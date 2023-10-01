# coding: utf-8
# @Author:Afun
# 模拟退火解费马点
import math
import random as r
import matplotlib.pyplot as plt


class My_Fermat_Point():  # 解费马点的类
    def __init__(self, width, height, list_points, initial_distance=float("inf")):
        self.width = width  # 地图宽度
        self.height = height  # 地图高度
        self.list_points = list_points  # 顶点坐标列表
        self.optimal_x = None  # 最优解x坐标
        self.optimal_y = None  # 最优解y坐标
        self.min_total_distance = initial_distance  # 最小距离
        self.distance_history = []  # 存储每一步的距离

    def get_map(self):
        """
        :return: 一个二维数组，表示地图
        """
        graph = [[0 for x in range(self.width + 2)] for y in range(self.height + 2)]
        for i in self.list_points:
            graph[i[0]][i[1]] = 1
        return graph

    def display(self, graph):
        """
        :param graph: 二维数组，表示的是地图
        :return: 无，只是打印二维数组，比较直观
        """
        for i in graph:
            print(i)

    def count_distance(self, x1, x2, y1, y2):
        """

        :param x1,x2,y1,y2: 两个点的坐标
        :return: 返回两点的距离
        """
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_total_distance(self, x, y):
        """

        :param x,y: 一个点的坐标，每走一步会计算该点到所有顶点的距离
        :return: 返回（x,y）到所有顶点的距离和
        """
        total_distance = 0
        for point in self.list_points:
            total_distance += self.count_distance(x, point[0], y, point[1])
        return total_distance

    def find_optimal_solution(self):
        """
        :return: 无，找到最优解
        """
        self.min_total_distance = float("inf")
        optimal_x, optimal_y = None, None

        for x in range(1, self.height + 1):
            for y in range(1, self.width + 1):
                total_distance = self.get_total_distance(x, y)
                if total_distance < self.min_total_distance:
                    self.min_total_distance = total_distance
                    optimal_x, optimal_y = x, y

        self.optimal_x = optimal_x
        self.optimal_y = optimal_y

    def run(self, T, alpha):
        """

        :param T: 初始温度
        :param alpha: 降温系数
        :return: 最优解的坐标(x,y)和该点到所有顶点的距离
        """
        current_x, current_y = self.optimal_x, self.optimal_y
        current_distance = self.get_total_distance(current_x, current_y)

        path_x = [current_x]
        path_y = [current_y]
        distance_history = [current_distance]  # 存储距离历史记录

        while T > 0.5:
            if current_x == 0 or current_x == self.height + 1 or current_y == 0 or current_y == self.width + 1:
                T = T * alpha
                continue

            next_distances = {}
            next_distances[1] = self.get_total_distance(current_x, current_y - 1)  # 上移
            next_distances[2] = self.get_total_distance(current_x, current_y + 1)  # 下移
            next_distances[3] = self.get_total_distance(current_x - 1, current_y)  # 左移
            next_distances[4] = self.get_total_distance(current_x + 1, current_y)  # 右移

            Px = int(T)
            Pa = r.randint(0, 100)
            if Pa > Px:  # 开发
                min_distance = min(next_distances.values())
                next_directions = [k for k, v in next_distances.items() if v == min_distance]
                next_step = next_directions[r.randint(0, len(next_directions) - 1)]
            else:  # 勘探，随机朝四个方向移动
                next_step = r.randint(1, 4)
            if next_step == 1:
                current_x = current_x
                current_y = current_y - 1
            elif next_step == 2:
                current_x = current_x
                current_y = current_y + 1
            elif next_step == 3:
                current_x = current_x - 1
                current_y = current_y
            elif next_step == 4:
                current_x = current_x + 1
                current_y = current_y

            path_x.append(current_x)
            path_y.append(current_y)

            current_distance = self.get_total_distance(current_x, current_y)
            distance_history.append(current_distance)  # 将这一步的结果保存以便后续的绘图

            if current_distance < self.min_total_distance:
                self.min_total_distance = current_distance
                self.optimal_x = current_x
                self.optimal_y = current_y

            T = alpha * T  # 降温

        return path_x, path_y, distance_history

    def plot_result(self, path_x, path_y, distance_history):
        """

        :param path_x,path_y:(x,y)的坐标路径
        :param distance_history:每一步的总距离
        :return:无，只是绘制结果图
        """
        # 创建子图
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(8, 8))
        ax1.set_title('Fermat Point Map')

        # 绘制费马点地图
        ax1.imshow(self.get_map(), cmap='Blues', origin='lower', extent=(0.5, self.width + 0.5, 0.5, self.height + 0.5))
        ax1.set_xticks(range(1, self.width + 1))
        ax1.set_yticks(range(1, self.height + 1))
        ax1.grid(color='gray', linestyle='-', linewidth=0.5)

        # 绘制最优解路径
        ax1.plot(path_y, path_x, marker='o', markersize=4, color='red')

        # 显示最优解坐标
        ax1.annotate(
            'Optimal Solution: ({}, {}), Distance: {}'.format(self.optimal_x, self.optimal_y, self.min_total_distance),
            xy=(self.optimal_y, self.optimal_x), xycoords='data',
            xytext=(-50, 20), textcoords='offset points',
            arrowprops=dict(facecolor='black', arrowstyle="->"))

        ax2.set_title('Distance vs Time')

        # 绘制距离随时间变化的图表
        ax2.plot(range(len(distance_history)), distance_history, color='blue')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Distance')

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    list_points = [(1, 6), (6, 3), (1, 1), (6, 6)]  # 顶点坐标，可以修改
    initial_distance = float("inf")  # 初始距离设为无穷大，以便后续更新
    my_fermat_point = My_Fermat_Point(10, 10, list_points, initial_distance)
    graph = my_fermat_point.get_map()  # 创建地图
    my_fermat_point.display(graph)  # 显示矩阵地图
    my_fermat_point.find_optimal_solution()  # 找最优解
    path_x, path_y, distance_history = my_fermat_point.run(100, 0.99)

    print("Optimal Solution: ({}, {})".format(my_fermat_point.optimal_x, my_fermat_point.optimal_y))

    my_fermat_point.plot_result(path_x, path_y, distance_history)  # 绘制结果图
