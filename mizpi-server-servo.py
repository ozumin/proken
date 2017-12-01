#coding: utf-8

import socket
import RPi.GPIO as GPIO
import time
import sys

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, 50)
servo.start(0.0)

try:
    unicode
    def u(str): return str.decode('utf-8')
    pass
except:
    def u(str): return str
    pass

host = "192.168.2.11" #お使いのサーバーのホスト名を入れます
port = 5000 #クライアントと同じPORTをしてあげます

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）

print 'Waiting for connections...'
clientsock, client_address = serversock.accept() #接続されればデータを格納

while True:
    rcvmsg = clientsock.recv(1024)
    print 'Received -> %s' % (rcvmsg)
    if rcvmsg == '':
        break
    
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    servo.ChangeDutyCycle(8.4375)
    time.sleep(0.5)
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)

    print 'Wait...'

servo.ChangeDutyCycle(7.25)
time.sleep(1.5)
servo.stop
GPIO.cleanup()

clientsock.close()
