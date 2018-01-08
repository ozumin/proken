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

pwm = Adafruit_PCA9685.PCA9685()

servo_min = 150
servo_max = 600

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000
    pulse_length //=60
    pulse_length //=4096
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(60)

try:
    unicode # python2
    def u(str): return str.decode('utf-8')
    pass
except: # python3
    def u(str): return str
    pass

host = '127.0.0.1'
port = 10500
bufsize = 1024

buff = StringIO(u(''))
pattern = r'WHYPO WORD=\"(.*)\" CLASSID'
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        data = sock.recv(bufsize)
        buff.write(data.decode('utf-8'))
        data = buff.getvalue().replace('> ', '>\n ')
        if '\n' in data:
            lines = data.splitlines()
            for i in range(len(lines)-1):
                if lines[i] != '.':
                    #print(lines[i])
                    m = re.search(pattern, lines[i])
                    if m:
                        word = m.group(1)
                        # 認識された単語wordの中に、u('...') という文字列が含まれるかどうかを
                        # チェックし、文字列に応じたアクションを記述します。
                        # u('...')でくくるのは、python2とpython3の互換性を保つためです。
                        # 「対象となる文字が含まれているか」を調べていますので、
                        # 先に「『１』が含まれるか」をチェックすると
                        # １０～１２がすべて「１」と判定されてしまいます。
                        # そのため、１０～１２のチェックを先に行っています。

                        if u('寂しい') in word:
                            print(word)
                            pwm.set_pwm(5,0,400)
                            time.sleep(1)
                            for i in range(3):
                                pwm.set_pwm(0,0,servo_min)
                                pwm.set_pwm(1,0,servo_min)
                                pwm.set_pwm(2,0,servo_min)
                                pwm.set_pwm(3,0,servo_min)
                                pwm.set_pwm(4,0,servo_min)
                                time.sleep(0.75)
                                pwm.set_pwm(0,0,servo_max)
                                pwm.set_pwm(1,0,servo_max)
                                pwm.set_pwm(2,0,servo_max)
                                pwm.set_pwm(3,0,servo_max)
                                pwm.set_pwm(4,0,servo_max)
                                time.sleep(0.75)
                            pwm.set_pwm(0,0,servo_max)
                            pwm.set_pwm(1,0,servo_max)
                            pwm.set_pwm(2,0,servo_max)
                            pwm.set_pwm(3,0,servo_max)
                            pwm.set_pwm(4,0,servo_max)
                            pwm.set_pwm(5,0,300)
                            time.sleep(1)
                        elif u('ありがとう') in word:
                            print(word)
#                            sock.close()
            buff.close()
            buff = StringIO(u(''))
            if lines[len(lines)-1] != '.':
            	buff.write(lines[len(lines)-1])

except socket.error:
    print('socket error')
except KeyboardInterrupt:
    pass

sock.close()
