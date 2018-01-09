# -*- coding: utf-8 -*-
from __future__ import division
import socket
from io import StringIO
import re
import subprocess
import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

pwm = Adafruit_PCA9685.PCA9685()

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    pulse_length //= 4096     # 12 bits of resolution
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(60)

try:
    unicode # python2
    def u(str): return str.decode('utf-8')
    pass
except: #python3
    def u(str): return str
    pass

host = '127.0.0.1'
port = 10500
bufsize = 1024

buff = StringIO(u(''))
pattern = r'WHYPO WORD=\"(.*)\" CLASSID'
j = 1
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    while j == 1:
        data = sock.recv(bufsize)
        buff.write(data.decode('utf-8'))
        data = buff.getvalue().replace('> ', '>\n ')
        if '\n' in data:
            lines = data.splitlines()
            for i in range(len(lines)-1):
                if lines[i] != '.':
                    m = re.search(pattern, lines[i])
                    if m:
                        word = m.group(1)
                        while True:
                            pwm.set_pwm(5, 0, 300)
                            time.sleep(1)
                            pwm.set_pwm(5, 0, 450)
                            time.sleep(1)
                            word = m.group(1)
                            if u('ありがとう') in word:
                                j = 0
                                break

            buff.close()
            buff = StringIO(u(''))
            if lines[len(lines)-1] != '.':
                buff.write(lines[len(lines)-1])

except socket.error:
    print('socket error')
except KeyboardInterrupt:
    pass

sock.close()

pwm.set_pwm(5,0,200)
time.sleep(1)
