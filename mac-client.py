#coding: utf-8

import socket
from io import StringIO
import re
import subprocess

host = '127.0.0.1'
port = 10500
bufsize = 1024

try:
    unicode # python2
    def u(str): return str.decode('utf-8')
    pass
except: # python3
    def u(str): return str
    pass

buff = StringIO(u(''))
pattern = r'WHYPO WORD=\"(.*)" CLASSID'
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    while True:
        data  = sock.recv(bufsize)
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

                        if u('起きて') in word:
                            print(word)
                            sock.close()
                        
                            host = "192.168.2.11" #お使いのサーバーのホスト名を入れます
                            port = 5000 #クライアントと同じPORTをしてあげます
                            
                            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                            client.connect((host, port))

                            client.send("from mac")

                            response = client.recv(4096)

                            print response

            buff.close()
            buff = StringIO(u(''))
            if lines[len(lines)-1] != '.':
                buff.write(lines[len(lines)-1])

except socket.error:
    print('socket error')
except KeyboardInterrupt:
    pass
