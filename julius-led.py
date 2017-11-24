# -*- coding: utf-8 -*-
import socket
from io import StringIO
import re
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

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
                            GPIO.output(25, GPIO.HIGH)
                        elif u('起きて') in word:
                            print(word)
                            GPIO.output(25, GPIO.LOW)
            buff.close()
            buff = StringIO(u(''))
            if lines[len(lines)-1] != '.':
            	buff.write(lines[len(lines)-1])

except socket.error:
    print('socket error')
except KeyboardInterrupt:
    pass

sock.close()
