import time
import numpy as np
import serial
from threading import Thread
from scipy import signal
from sklearn.cross_decomposition import CCA


def get_val(buf):  # 处理接收数据
    scale_fac_uVolts_per_count = 0.022351744455307063  # uV
    val = []
    for i in range(8):
        temp = buf[1 + i * 3:1 + (i + 1) * 3]
        if temp[0] > 127:
            temp = int.from_bytes(temp, byteorder='big')
            val.append((temp - 16777216) * scale_fac_uVolts_per_count)
        else:
            temp = int.from_bytes(temp, byteorder='big')
            val.append(temp * scale_fac_uVolts_per_count)
    return val


def recv_data(buf, port):  # 串口接收数据
    bps = 115200
    timex = 5
    ser = serial.Serial(port, bps, timeout=timex)
    ser.write('b\n'.encode('UTF-8'))

    while True:
        char = ser.read()
        if char == b'\xa0':
            temp = ser.read(32)
            buf.append(get_val(temp))
            if len(buf) > 15000:  # 设置buffer容量
                buf.pop(0)


def pre_data(input_dataset, channel_number):  # 数据预处理
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


def gen_template(fre_list, t_linspace):  # 生成模板信号
    output_list = []
    for i in range(len(fre_list)):
        temp = [np.sin(2 * np.pi * fre_list[i] * t_linspace), np.sin(2 * np.pi * 2 * fre_list[i] * t_linspace),
                np.cos(2 * np.pi * fre_list[i] * t_linspace), np.cos(2 * np.pi * 2 * fre_list[i] * t_linspace)]
        temp = np.array(temp).T
        output_list.append(temp)
    return output_list


def cca_classification(X, Y_list):  # CCA判断
    corr = []
    for i in range(len(Y_list)):
        Y = Y_list[i]
        cca = CCA(n_components=1)  # 建立模型，计算第一主成分
        cca.fit(X, Y)  # 训练
        X_train_r, Y_train_r = cca.transform(X, Y)  # 得到X和Y降维后的数据
        corr.append(np.corrcoef(X_train_r[:, 0], Y_train_r[:, 0])[0, 1])  # 输出相关系数，[:, 0]中0代表第一主成分
    return corr


buffer = []
portx = "COM5"
recv = Thread(target=recv_data, args=(buffer, portx,))  # 启动接收数据线程
recv.start()

fs = 250
window_size = 2
channel_num = [0, 1, 2]  # 通道编号
t = np.linspace(0, window_size, window_size * fs)  # 时轴
ft = np.linspace(10, 20, 50)  # 模板频率成分
template = gen_template(ft, t)  # 生成模板列表

time.sleep(5)
while True:
    time.sleep(window_size)
    dataset = np.array(buffer[-window_size * fs - 1:-1])  # 选取最后一段数据
    data = pre_data(dataset, channel_num)  # 生成数据
    corr_list = cca_classification(data, template)
    index = corr_list.index(max(corr_list))
    print("识别频率：", ft[index])
    print("相关系数：", max(corr_list))
