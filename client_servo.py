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

host = "192.168.2.13" #お使いのサーバーのホスト名を入れます
port = 5000 #適当なPORTを指定してあげます

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします

client.connect((host, port)) #これでサーバーに接続します

client.send("from nadechin") #適当なデータを送信します（届く側にわかるように）

response = client.recv(4096) #レシーブは適当な2進数にします（大きすぎるとダメ）

print response

if response == '起きて':
    servo.ChangeDutyCycle(2.5)
    time.sleep(1)

servo.ChangeDutyCycle(7.25)
time.sleep(1)
servo.stop
GPIO.cleanup()
