import pygame
from pygame import Surface, Rect
import threading
import time
import numpy as np
import serial
from threading import Thread
from scipy import signal
from sklearn.cross_decomposition import CCA


# 创建刺激源图像
def create(flag, a=5, b=5, w=250, h=250):
    k = w / a
    l = h / b
    surf = Surface((w, h))
    c = (0, 0, 0) if flag else (255, 255, 255)
    surf.fill(c)
    for i in range(0, a):
        for j in range(0, b):
            c = (255, 255, 255) if c == (0, 0, 0) else (0, 0, 0)
            r = Rect(k * i, l * j, k, l)
            surf.fill(c, r)
    return surf


IMAGES = [
    create(0),
    create(1)
]  # 定义图像
A = IMAGES[0].get_width()


# 控制图像闪烁
class FlickyManager:
    def __init__(self, scr):
        self.flickies = []
        self.screen = scr

    def addFlicky(self, f):
        self.flickies.append(f)

    def add(self, location, frames):
        w, h = self.screen.get_size()
        if location == 'left':
            x = A / 2
            y = h / 2 - A / 2
        elif location == 'right':
            x = w - A - A / 2
            y = h / 2 - A / 2
        elif location == 'top':
            y = 0
            x = w / 2 - A / 2
        elif location == 'bottom':
            y = h - A
            x = w / 2 - A / 2
        elif location == 'center':
            y = h / 2 - A / 2
            x = w / 2 - A / 2
        else:
            raise ValueError("location %s unknown" % location)
        f = Flicky(x, y, frames)
        self.flickies.append(f)

    def process(self):
        for f in self.flickies:
            f.process()

    def draw(self):
        for f in self.flickies:
            f.draw(self.screen)


# 每一个闪烁的定义
class Flicky(object):
    def __init__(self, x, y, frames=10, w=A, h=A):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.frames = frames
        self.clock = 0
        self.img_index = 0

    def process(self):
        self.clock = self.clock + 1
        if self.clock >= self.frames:
            self.clock = 0
            self.img_index = 0 if self.img_index == 1 else 1

    def draw(self, scr):
        scr.blit(IMAGES[self.img_index], (self.x, self.y))


# 显示刺激
def disp_start(location_list, gap_list, fps=120):
    pygame.init()
    W, H = 1920, 1080
    screen = pygame.display.set_mode((W, H))  # 设置背景大小
    pygame.display.set_caption("SSVEP")

    clock = pygame.time.Clock()
    flickymanager = FlickyManager(screen)

    player_img = pygame.image.load("./player.png")
    player_img = pygame.transform.scale(player_img, (120, 95))
    player = pygame.sprite.Sprite()
    player.image = player_img
    player.rect = player.image.get_rect()
    player.rect.x, player.rect.y = W / 2 - player_img.get_size()[0] / 2, H / 2 - player_img.get_size()[1] / 2
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # 设置位置和刷新半周期
    for i in range(len(location_list)):
        flickymanager.add(location_list[i], gap_list[i])

    global disp_sign
    disp_sign = 0
    done_sign = False
    dir_sign = 1
    while not done_sign:
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    done_sign = True
            if event.type == pygame.QUIT:
                done_sign = True
        if disp_sign == 1:
            player.rect.x -= 50
            if dir_sign == 2:
                player.image = pygame.transform.flip(player.image, True, False)
                dir_sign = 1
        if disp_sign == 2:
            player.rect.x += 50
            if dir_sign == 1:
                player.image = pygame.transform.flip(player.image, True, False)
                dir_sign = 2
        disp_sign = 0
        screen.fill((0, 0, 0))  # 设置背景颜色
        clock.tick_busy_loop(fps)  # 设置背景刷新率
        flickymanager.process()
        flickymanager.draw()
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()


# 处理接收数据
def get_val(buf):
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


# 串口接收数据
def recv_data(buf, port):
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
    corr = []
    for i in range(len(Y_list)):
        Y = Y_list[i]
        cca = CCA(n_components=1)  # 建立模型，计算第一主成分
        cca.fit(X, Y)  # 训练
        X_train_r, Y_train_r = cca.transform(X, Y)  # 得到X和Y降维后的数据
        corr.append(np.corrcoef(X_train_r[:, 0], Y_train_r[:, 0])[0, 1])  # 输出相关系数，[:, 0]中0代表第一主成分
    return corr


# 显示进程
locations = ["left","right"]  # 刺激显示位置
gaps = [5,4]  # 刺激半周期
disp_th = threading.Thread(target=disp_start, args=(locations, gaps,))
disp_th.start()

# 接收和处理数据主线程
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
f_set = [12,15]  # 设置的频率

time.sleep(5)
while True:
    time.sleep(window_size)
    # np.save("./buffer", buffer)  # 保存数据
    dataset = np.array(buffer[-window_size * fs - 1:-1])  # 选取最后一段数据
    data = pre_data(dataset, channel_num)  # 生成数据
    corr_list = cca_classification(data, template)
    index = corr_list.index(max(corr_list))
    re_f = ft[index]
    re_corr = max(corr_list)
    print("识别频率：", re_f)
    print("相关系数：", re_corr)
    if abs(re_f - f_set[0]) < 1.0:
        disp_sign = 1
    elif abs(re_f - f_set[1]) < 1.0:
        disp_sign = 2
    else:
        disp_sign = 0
