#! coding:UTF-8
import pandas as pd

file_path = "./data.txt"  # 文件路径
channel_number = [item + 1 for item in list(range(8))]  # 通道号
with open(file_path) as f:
    data = f.readlines()
print(data[2][1:])

data = data[6:-1]  # 去掉最后一行
output = [[] for i in range(len(data))]
for i in range(len(data)):
    data[i] = data[i].split(',')
    for j in range(len(channel_number)):
        output[i].append(float(data[i][channel_number[j]]))

df = pd.DataFrame(output, columns=["ch"+str(item) for item in channel_number])
df.to_excel(file_path[0:-4] + "_output.xlsx", index=False)
