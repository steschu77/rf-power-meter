# -*- coding: utf-8 -*-
import serial
import time
import csv
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

level = []

freq = np.arange(100, 5001, 50)

with serial.Serial('COM3', 9600) as ser:

  for f in freq:
    s = '${:04d}+00.0#'.format(f)
    ser.write(s.encode('utf-8'))
    time.sleep(0.5)

    ser.reset_input_buffer()
    print(f)
    
    # reads '$-x.xx  dBm  xxx uVpp$' strings from the RF Meter
    res = []
    for i in range(10):
      ser.read() # read '$'
      x = float(ser.read_until(b'$').decode("utf-8").split()[0])
      res.append(x)

    level.append(mean(res))

ser.close()

#print("{}, {}, {}".format(min(res), mean(res), max(res)))
print(freq)
print(level)

with open('levels.csv', 'w', newline='') as writecsv:
  writer = csv.writer(writecsv)

  for l in zip(freq, level):
    writer.writerow(l)

fig, ax = plt.subplots()
ax.plot(freq, level)

ax.set(xlabel='frequency (MHz)', ylabel='level (dBm)')
ax.grid()

fig.savefig("test.png", dpi=300)
