#coding:utf-8
import numpy as np
import random
from matplotlib import pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def model(X, theta):
    # 预测函数  得到预测结果  矩阵相乘
    return sigmoid(np.dot(X, theta))

def cost(data, theta):
    # 计算损失函数 按照公式
    cols = data.shape[1]
    X = data[:, 0:cols-1]
    y = data[:, cols-1:]
    left = np.multiply(-y, np.log(model(X, theta)))  # 左边的连乘
    right = np.multiply((1 - y), np.log(1 - model(X, theta))) # 右边的连乘
    return np.sum(left - right) / (len(X))

def gradient(X, y, theta):
    # 求解梯度 grad为 theta梯度的更新值
    grad = np.zeros(theta.shape)
    error = (model(X, theta) - y).ravel()
    for j in range(len(theta.ravel())):
        temp = np.multiply(error, X[:,j])
        grad[j, 0] = np.sum(temp) / len(X)
    return grad

def shuffleData(data, batchSize):
    # 洗牌 防止数据有一定的排列规律
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[0:batchSize, 0:cols-1]
    y = data[0:batchSize, cols-1:]
    return X, y

def train(data, theta, batchSize, alpha, max_iter):
    # 最主要的函数 梯度下降求解
    # batchSize：为1代表随机梯度下降  为整体值表示批量梯度下降  为某一数值时表示小批量梯度下降
    # alpha 学习率
    grad = np.zeros(theta.shape) # 计算的梯度
    for i in range(max_iter):
        X, y = shuffleData(data, batchSize)# 洗牌 防止数据有一定的排列规律
        grad = gradient(X, y, theta)
        theta = theta - alpha * grad # 参数更新
        print('theta0:{0}, theta1:{1}, theta2:{2}'.format(theta[0,0], theta[1,0], theta[2,0]))
        print('loss is {0}'.format( cost(data, theta) )) # 计算新的损失

def gen_sample_data(num):
    theta = np.array([-3, 1, 1])
    theta = theta.reshape(len(theta), 1)
    x_array_1 = np.random.random((num, 1)) * 4
    x_array_2 = np.random.random((num, 1)) * 4
    ones = np.ones((num, 1))
    x_array = np.append(ones, x_array_1, axis=1)
    x_array = np.append(x_array, x_array_2, axis=1)
    y_array = model(x_array, theta)
    y_array[y_array >= 0.5] = 1
    y_array[y_array < 0.5] = 0
    y_array = y_array.reshape(len(y_array), 1)
    data_array = np.append(x_array, y_array, axis=1)
    return data_array, theta


def run():
    #data_array是一个num *3 的矩阵(X1,X2,Y1)，theta是一个3*1的矩阵
    data_array, theta = gen_sample_data(100)
    lr = 0.001
    max_iter = 10000
    batchSize = 50
    train(data_array, theta, batchSize, lr, max_iter)


if __name__ == '__main__':
    run()
