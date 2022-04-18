import time
from ctypes import windll
import numpy as np
from threading import Thread
import game_form
import data_recv
import data_process


def get_action(player):
    time.sleep(5)
    while True:
        time.sleep(window_size)
        # np.save("./buffer", buffer)  # 保存数据
        dataset = np.array(buffer[-window_size * fs - 1:-1])  # 选取数据
        data = data_process.pre_data(dataset, channel_num)  # 预处理
        ft = np.linspace(bottom_freq, top_freq, 50)  # 频率列表
        template = data_process.gen_template(ft, np.linspace(0, window_size, window_size * fs))  # 信号模板
        idx, corr_list = data_process.cca_classification(data, template)
        freq_list = ft[idx]
        re_f = data_process.calc_freq(freq_list)
        re_corr = max(corr_list)
        print("识别频率：", re_f)
        print("相关系数：", re_corr)
        if abs(re_f - f_set[0]) < 1.4:
            player.move(1)
        elif abs(re_f - f_set[1]) < 1.8:
            player.move(2)
        else:
            player.move(0)


# 修改windows系统时钟分辨率
timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

# 参数设置
fs = 250  # 采样频率
window_size = 3  # 窗口宽度
channel_num = [0, 1, 2, 3, 4, 5]  # 通道编号
top_freq = 18  # 模板频率上限
bottom_freq = 11  # 模板频率下限
f_set = [12.5, 15.5]  # 设置的频率

# 接收和处理数据线程
buffer = []
portx = "COM5"
recv_th = Thread(target=data_recv.recv_data, args=(buffer, portx,))
recv_th.start()
# 角色动作线程
game = game_form.Game()
hero = game.hero
action_th = Thread(target=get_action, args=(hero,))
action_th.start()
# 游戏主进程
game.start_game()
