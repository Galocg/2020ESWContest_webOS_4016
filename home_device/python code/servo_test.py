import RPi.GPIO as GPIO
import time

pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
cnt = 0

degree = 90
duty = 3.2 +  degree * (12.95 - 3.2) / 180

while True:
        p.ChangeDutyCycle(3.2)
        print"angle : ", 0
        time.sleep(1)
        p.ChangeDutyCycle(duty)
        print "angle : ", 90
        time.sleep(1)
        p.ChangeDutyCycle(12.95)
        print "angle : ", 180
        time.sleep(1)

GPIO.cleanup()
