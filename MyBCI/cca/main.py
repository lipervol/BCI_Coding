from scipy import signal
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cross_decomposition import CCA


def pre_data(input_dataset, channel_number):  # 数据预处理
    output_data = []
    for i in range(len(channel_number)):
        input_data = input_dataset[:,channel_number[i]]
        input_data = input_data - np.mean(input_data)

        b, a = signal.butter(8, [0.04, 0.32], "bandpass")
        filted_data = signal.filtfilt(b, a, input_data)
        b, a = signal.butter(8, [0.36, 0.44], "bandstop")
        filted_data = signal.filtfilt(b, a, filted_data)

        output_data.append(filted_data)
    return np.array(output_data).T


def gen_template(fre_list, t_linspace):
    output_list = []
    for i in range(len(fre_list)):
        temp = [np.sin(2 * np.pi * fre_list[i] * t_linspace), np.sin(2 * np.pi * 2 * fre_list[i] * t_linspace),
                np.cos(2 * np.pi * fre_list[i] * t_linspace), np.cos(2 * np.pi * 2 * fre_list[i] * t_linspace)]
        temp = np.array(temp).T
        output_list.append(temp)
    return output_list


def cca_classification(X, Y_list):
    corr = []
    for i in range(len(Y_list)):
        Y = Y_list[i]
        cca = CCA(n_components=1)  # 建立模型，计算第一主成分
        cca.fit(X, Y)  # 训练
        X_train_r, Y_train_r = cca.transform(X, Y)  # 得到X和Y降维后的数据
        corr.append(np.corrcoef(X_train_r[:, 0], Y_train_r[:, 0])[0, 1])  # 输出相关系数，[:, 0]中0代表第一主成分
    return corr


fs = 250  # 采样频率
offset = 20 * fs  # 起始时间
gap = 2  # 时间间隔
channel_num = [0, 1, 2]  # 通道编号
t = np.linspace(0, gap, gap * fs)  # 时轴

dataset = pd.read_excel("./data121_output.xlsx")
dataset = dataset.values
dataset = dataset[offset:offset + len(t), :]
data = pre_data(dataset, channel_num)  # 生成数据

ft = np.linspace(10, 20, 50)
template = gen_template(ft, t)  # 生成模板列表

corr_list = cca_classification(data,template)
print(max(corr_list))
index = corr_list.index(max(corr_list))
print(ft[index])

