import os  # 需要安装pillow库
from PIL import Image

img = Image.open('./break.gif')
os.mkdir('break')  # 生成的图片的文件夹名称
try:
    i = 0
    while True:
        img.seek(i)
        img.save('break/' + str(i) + '.png')  # 生成的图片名称
        i = i + 1
except:
    pass
print('共拆解图像帧数' + str(i))  # 控制台输出拆分的帧数
