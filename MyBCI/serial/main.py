import time
import numpy as np
import serial
from threading import Thread


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
            if len(buf) > 15000:
                buf.pop(0)


buffer = []
portx = "COM5"
recv = Thread(target=recv_data, args=(buffer,portx,))
recv.start()

fs = 250
window_size = 2
time.sleep(window_size + 3)

while True:
    data = np.array(buffer[-window_size * fs:-1])
