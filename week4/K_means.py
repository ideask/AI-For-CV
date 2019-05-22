# coding = utf-8
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs

# 生成num个二维数据集（二分类），样本中心点[-1,-1], [2,2]


# 两个向量间欧式距离（L2距离）
def disCal(vecA, vecB):
    return sqrt(sum(power((vecA - vecB), 2)))

# 随机从样本数据集中选取k个点作为中心点,不能抽取重复作为中心点！！！
def randChoiceCenter(k, data_array):
    center_point_pos = np.zeros((k, data_array.shape[1]))
    data_index = list(range(data_array.shape[0]))
    for i in range(k):
        randIndex = random.randint(0, len(data_index))
        center_point_pos[i][:] = data_array[data_index[randIndex], :]
        #print('randIndex:{0}'.format(data_index[randIndex]))
        del data_index[randIndex]
    #print(center_point_pos)
    return center_point_pos

def kMeans(k, data_array):
    # 生成k个随机簇点
    center_points = randChoiceCenter(k, data_array)
    # 样本数量
    sample_count = data_array.shape[0]
    # 样本点的簇的分类号，样本点与簇点的最短距离
    cul_assign = np.zeros((sample_count,2))
    # 簇分配变化检测标准位
    assign_change = True
    while assign_change:
        assign_change = False
        # 给数据集中每个数据分配簇的编号（即按与中心点距离最小的来分类）
        for i in range(sample_count):
            min_dis = inf
            min_index = -1
            for j in range(k):
                # 计算样本点与簇的L2距离
                dis = disCal(data_array[i,:], center_points[j, :])
                if min_dis > dis:
                    min_dis = dis
                    min_index = j
            if cul_assign[i][0] != min_index:
                cul_assign[i][0] = min_index
                cul_assign[i][1] = min_dis ** 2
                assign_change = True
           # print(cul_assign)
        # 利用中值来更新中心点的位置
        for z in range(k):
            #print('k:{0}'.format(z))
            #print(data_array[nonzero(cul_assign[:, 0] == z)[0], :])
            #print(mean(data_array[nonzero(cul_assign[:, 0] == z)[0], :], axis = 0))
            center_points[z] = mean(data_array[nonzero(cul_assign[:, 0] == z)[0], :], axis = 0)
    return center_points, cul_assign


# 2维数据聚类效果显示
def datashow(dataSet, k, centroids, clusterAssment):  # 二维空间显示聚类结果
    num, dim = shape(dataSet)  # 样本数num ,维数dim

    if dim != 2:
        print('sorry,the dimension of your dataset is not 2!')
        return 1
    marksamples = ['or', 'ob', 'og', 'ok', '^r', '^b', '<g']  # 样本颜色标记
    if k > len(marksamples):
        print('sorry,your k is too large,please add length of the marksample!')
        return 1
        # 绘所有样本
    for i in range(num):
        markindex = int(clusterAssment[i, 0])  # 矩阵形式转为int值, 簇序号
        # 特征维对应坐标轴x,y；样本图形标记及大小
        plt.plot(dataSet[i, 0], dataSet[i, 1], marksamples[markindex], markersize=5)

    # 绘中心点
    markcentroids = ['o', '*', '^', '+', '.', 'x', 's', 'd', '<', '>', 'p', 'h']  # 聚类中心图形标记
    label = ['0', '1', '2', '3', '4', '5', '6']
    c = ['yellow', 'pink', 'red', 'g', 'c', 'b', 'k']
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], markcentroids[i], markersize=10, label=label[i], c=c[i])
        plt.legend(loc='upper left')
    plt.xlabel('sepal length')
    plt.ylabel('sepal width')
    plt.title('k-means cluster result')  # 标题
    plt.show()

if __name__ == '__main__':
    k = 7;
    data_array, target = make_blobs(n_samples=100, n_features=2, centers=k, cluster_std=1.0, center_box=(-3.0, 3.0))
    center_points, cul_assign = kMeans(k, data_array)
    datashow(data_array, k, center_points, cul_assign)





