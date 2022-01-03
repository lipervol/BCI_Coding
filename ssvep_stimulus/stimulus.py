#!coding:UTF-8

import cv2
import numpy as np
import threading
import time
import math


# locations = [[(100, 200), (750, 850)], [(400, 500), (1120, 1220)], [(700, 800), (750, 850)], [(400, 500), (400, 500)]]  # 色块位置
# frequency = [7, 9, 11, 13]  # 闪烁频率

# 方波驱动
# def twinkle(region, image, period):
#     while True:
#         time.sleep(period / 2)
#         for i in range(region[0][0], region[0][1]):
#             for j in range(region[1][0], region[1][1]):
#                 image[i][j] = 0
#         time.sleep(period / 2)
#         for i in range(region[0][0], region[0][1]):
#             for j in range(region[1][0], region[1][1]):
#                 image[i][j][0] = 255

# 以正弦信号闪烁，python上效果不太好
# def twinkle_pro(region, image, period):
#     x = 0
#     while True:
#         for i in range(region[0][0], region[0][1]):
#             for j in range(region[1][0], region[1][1]):
#                 image[i][j][0] = 255 * ((math.sin(2 * math.pi * x / 10) + 1) / 2)
#         x += 1
#         if x == 10:
#             x = 0
#         time.sleep(period / 10)

def gen_pads(regions, color):
    pads = []
    for region in regions:
        x1, x2, y1, y2 = region[0][0], region[0][1], region[1][0], region[1][1]
        pad = np.zeros((x2 - x1, y2 - y1, 3))
        for i in range(x2 - x1):
            for j in range(y2 - y1):
                pad[i][j] = color
        pads.append(pad)
    return pads


def twinkle(region, image, pad, period):
    x1, x2, y1, y2 = region[0][0], region[0][1], region[1][0], region[1][1]
    while True:
        time.sleep(period / 2)
        image[x1:x2, y1:y2] = pad
        time.sleep(period / 2)
        image[x1:x2, y1:y2] = 0


size = (1080, 1920, 3)  # 画面大小
locations = [[(300, 700), (750, 1150)]]  # 色块位置
frequency = [50/3]  # 闪烁频率
img = np.zeros(size, np.uint8)
pads = gen_pads(locations, [255, 0, 0])
out_win = "stimulus"
cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(out_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# 多线程单独渲染
threads = []
for i in range(len(locations)):
    threads.append(threading.Thread(target=twinkle, args=(locations[i], img, pads[i], 1 / frequency[i],)))
for i in range(len(threads)):
    threads[i].start()

while True:
    cv2.waitKey(1)
    cv2.imshow(out_win, img)

# region = locations[0]
# x1, x2, y1, y2 = region[0][0], region[0][1], region[1][0], region[1][1]
# pic = np.zeros(size, np.uint8)
# pic[x1:x2, y1:y2] = pads[0]
# while True:
#     cv2.waitKey(30)
#     cv2.imshow(out_win, img)
#     cv2.waitKey(30)
#     cv2.imshow(out_win, pic)


