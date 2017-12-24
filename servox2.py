#!/usr/bin/python
from __future__ import division
import time

# Import the PCA9685 module
import Adafruit_PCA9685

#Initialize the PCA9685 using the default address (0x40)
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lenghts
servo_min = 150 # Min pulse length out of 4096
servo_max = 600 # Max pulse length out og 4096

# Helper function to make setting a servo pulse width simpler
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000 # 1,000,000 us per second
#    pulse_length //= 60 # 60 Hz
    pulse length //= 50 # 50 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //=4096 # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
#    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

#pwm.set_pwm_freq(60)
pwm.set_pwm_freq(50)

print('Moving servo on channel 0 and 1, press Ctrl-C to quit...')
while True:
    # Move servo on channel 0 and 1 between extremes
    pwm.set_pwm(0,0,servo_min)
    time.sleep(1)
    pwm.set_pwm(0,0,servo_max)
    time.sleep(1)
    pwm.set_pwm(1,0,servo_min)
    time.sleep(1)
    pwm.set_pwm(1,0,servo_max)
    time.sleep(1)
