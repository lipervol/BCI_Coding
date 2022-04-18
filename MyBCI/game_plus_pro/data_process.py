import numpy as np
from sklearn.cross_decomposition import CCA
from scipy import signal
import scipy.stats as stats


# 数据预处理
def pre_data(input_dataset, channel_number):
    output_data = []
    for i in range(len(channel_number)):
        input_data = input_dataset[:, channel_number[i]]
        input_data = input_data - np.mean(input_data)

        b, a = signal.butter(8, [0.04, 0.32], "bandpass")  # 滤波
        filted_data = signal.filtfilt(b, a, input_data)
        b, a = signal.butter(8, [0.36, 0.44], "bandstop")
        filted_data = signal.filtfilt(b, a, filted_data)

        output_data.append(filted_data)
    return np.array(output_data).T


# 生成模板信号
def gen_template(fre_list, t_linspace):
    output_list = []
    for i in range(len(fre_list)):
        temp = [np.sin(2 * np.pi * fre_list[i] * t_linspace), np.sin(2 * np.pi * 2 * fre_list[i] * t_linspace),
                np.cos(2 * np.pi * fre_list[i] * t_linspace), np.cos(2 * np.pi * 2 * fre_list[i] * t_linspace)]
        temp = np.array(temp).T
        output_list.append(temp)
    return output_list


# CCA判断
def cca_classification(X, Y_list):
    idx = []
    value = []
    for channel in range(X.shape[1]):
        corr = []
        for i in range(len(Y_list)):
            Y = Y_list[i]
            cca = CCA(n_components=1)  # 建立模型，计算第一主成分
            cca.fit(X[:, channel], Y)  # 训练
            X_train_r, Y_train_r = cca.transform(X, Y)  # 得到X和Y降维后的数据
            corr.append(np.corrcoef(X_train_r[:, 0], Y_train_r[:, 0])[0, 1])  # 输出相关系数，[:, 0]中0代表第一主成分
        idx.append(np.argmax(corr))
        value.append(np.max(corr))
    return idx, value


# 核概率密度估计频率
def calc_freq(src):
    kde = stats.gaussian_kde(src)
    src_bottom = np.min(src)
    src_top = np.max(src)
    xs = np.linspace(src_bottom, src_top, len(src))
    src_range = src_top - src_bottom
    kde.set_bandwidth(bw_method=kde.factor / 5.0)
    src_kde = kde(xs) * src_range
    freq_index = (np.argmax(src_kde) / len(xs))
    freq_index = 0.01 if freq_index < 0.01 else freq_index
    freq = freq_index * (np.max(src) - np.min(src)) + np.min(src)
    return freq
