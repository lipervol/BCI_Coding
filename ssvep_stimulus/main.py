#!coding:UTF-8

import cv2
import numpy as np
import threading
import time
import math

size = (1080, 1920, 3)  # 画面大小
# locations = [[(100, 200), (750, 850)], [(400, 500), (1120, 1220)], [(700, 800), (750, 850)], [(400, 500), (400, 500)]]  # 色块位置
# frequency = [7, 9, 11, 13]  # 闪烁频率
locations = [[(400, 600), (800, 1000)]]  # 色块位置
frequency = [20]  # 闪烁频率

# 方波驱动
def twinkle(region, image, period):
    while True:
        time.sleep(period / 2)
        for i in range(region[0][0], region[0][1]):
            for j in range(region[1][0], region[1][1]):
                image[i][j] = 0
        time.sleep(period / 2)
        for i in range(region[0][0], region[0][1]):
            for j in range(region[1][0], region[1][1]):
                image[i][j][1] = 255


# 以正弦信号闪烁，python上效果不太好
def twinkle_pro(region, image, period):
    x = 0
    while True:
        for i in range(region[0][0], region[0][1]):
            for j in range(region[1][0], region[1][1]):
                image[i][j][1] = 255 * ((math.sin(2 * math.pi * x / 10) + 1) / 2)
        x += 1
        if x == 10:
            x = 0
        time.sleep(period / 10)


img = np.zeros(size, np.uint8)
# 多线程单独渲染
threads = []
for i in range(len(locations)):
    threads.append(threading.Thread(target=twinkle, args=(locations[i], img, 1 / frequency[i],)))
for i in range(len(threads)):
    threads[i].start()

while True:
    cv2.waitKey(1)
    cv2.imshow("stimulus", img)
