#coding:utf-8
import numpy as np
import random

def inference(w, b, x):        # inference, test, predict, same thing. Run model after training
    pred_y = w * x + b
    return pred_y

def eval_loss(w, b, data_array):
    cols = data_array.shape[1]
    x = data_array[:, 0:cols-1]
    y = data_array[:, cols-1:]
    h_y_sqr = 0.5 * (inference(w, b, x) - y) ** 2
    avg_loss = np.sum(h_y_sqr)
    avg_loss /= len(data_array)
    return avg_loss


def cal_step_gradient(batch_x_array, batch_gt_y_array, w, b, lr):
    #batch_x_array, batch_gt_y_array 都是n*1的矩阵
    batch_size = len(batch_x_array)
    avg_db = np.sum(inference(w, b, batch_x_array) - batch_gt_y_array)
    avg_dw = np.sum(np.multiply(batch_x_array, (inference(w, b, batch_x_array) - batch_gt_y_array)))
    avg_dw /= batch_size
    avg_db /= batch_size
    w -= lr * avg_dw
    b -= lr * avg_db
    return w, b

def shuffleData(data, batch_size):
    # 洗牌 防止数据有一定的排列规律
    np.random.shuffle(data)
    cols = data.shape[1]
    x = data[0:batch_size, 0:cols-1]
    y = data[0:batch_size, cols-1:]
    return x, y

def train(data_array, batch_size, lr, max_iter):
    w = 0
    b = 0
    for i in range(max_iter):
        batch_x, batch_y = shuffleData(data_array, batch_size)
        #print('batch_x:{0}, batch_y:{1}'.format(batch_x, batch_y))
        w, b = cal_step_gradient(batch_x, batch_y, w, b, lr)
        print('w:{0}, b:{1}'.format(w, b))
        print('loss is {0}'.format(eval_loss(w, b, data_array)))


def gen_sample_data(num):
    w = random.randint(0, 10) + random.random()		# for noise random.random[0, 1)
    b = random.randint(0, 5) + random.random()
    x_array = np.random.random((num, 1)) * 100
    y_array = inference(w, b, x_array) + random.random() * random.randint(-1, 1)
    data_array = np.append(x_array, y_array, axis=1)
    return data_array, w, b


def run():
    data_array, w, b = gen_sample_data(100)
    lr = 0.00045
    max_iter = 10000
    train(data_array, 50, lr, max_iter)


if __name__ == '__main__':
    run()
