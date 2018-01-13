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
import random

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

num = 0

def janken(num):
    time.sleep(0.7)
    if num == 1:
        time.sleep(0.7)
    elif num == 2:
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_min)
        pwm.set_pwm(4,0,servo_min)
        time.sleep(0.7)
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_max)
        pwm.set_pwm(4,0,servo_max)
    elif num == 3:
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_min)
        pwm.set_pwm(2,0,servo_min)
        pwm.set_pwm(3,0,servo_min)
        pwm.set_pwm(4,0,servo_min)
        time.sleep(0.7)
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_max)
        pwm.set_pwm(2,0,servo_max)
        pwm.set_pwm(3,0,servo_max)
        pwm.set_pwm(4,0,servo_max)
    else:
        print('not found')
    print(num)
    time.sleep(1)

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
                            pwm.set_pwm(5,0,200)
                            time.sleep(1)
                        elif u('じゃんけん') in word:
                            print(word)
                            janken(random.randint(1,3))
                        elif u('つまらない') in word:
                            print(word)
                            cmd = 'mplayer -ao alsa:device=plughw=2.0 2.mp3'
                            subprocess.call(cmd.strip().split(" ") )
                        elif u('ありがとう') in word:
                            print(word)
                            pwm.set_pwm(0,0,servo_max)
                            pwm.set_pwm(1,0,servo_max)
                            pwm.set_pwm(2,0,servo_max)
                            pwm.set_pwm(3,0,servo_max)
                            pwm.set_pwm(4,0,servo_max)
                            pwm.set_pwm(5,0,200)
                            time.sleep(1)
            buff.close()
            buff = StringIO(u(''))
            if lines[len(lines)-1] != '.':
            	buff.write(lines[len(lines)-1])

except socket.error:
    print('socket error')
except KeyboardInterrupt:
    pass

sock.close()
