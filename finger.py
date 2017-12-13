#!/usr/bin/python
# coding: utf-8

import RPi.GPIO as GPIO
import time
import signal
import sys

def exit_handler(signal, frame):
    print("\nExit")
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)
    servo.stop()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

GPIO.setmode(GPIO.BCM)

gp_out = 21

GPIO.setup(gp_out, 50)

servo.star(0.0)

servo.ChangeDutyCycle(7.25)
time.sleep(0.5)

servo.ChangeDutyCycle(2.5)
time.sleep(0.5)
servo.stop()
GPIO.cleanup()
sys.exit(0)
