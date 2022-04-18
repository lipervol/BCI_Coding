import serial

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
