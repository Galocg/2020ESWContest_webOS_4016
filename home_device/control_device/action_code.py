import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import json
import threading
import requests
from flask import Flask, request
import socket
url = 'https//172.31.38.232'
port = 443
isUserUsing = 0
app = Flask(__name__)
#라즈베라 파이도 서버로 열어서  /userAlive 가 들어왔을때만 실행 할 수 있도록 한다.
@app.route("/userAlive") 
def userAlive():
    global isUserUsing
    isUserUsing = 1
    return {"status":1}

@app.route("/userDead") 
def userDead():
    global isUserUsing
    isUserUsing = 0
    return {"status":1}

@app.route("/")
def hello():
   return "I'm alive"


def camera_find() :
    #while : 개를 찾을때 까지 계속해야함. 다만 타임 인터벌이 일정 수준 이상일때는 없다고 반환해야할것
    #30도 각도 차이로 돌고, request 계속 보내서 개 찾았는지 물어보기
    # 카메라를 돌리고, 서버에 리퀘스트를 보내서 개를 찾았는지 계속 확인해야함    
    # 찾자마자 각도 갱신시키고 나갈 것.


def camera_motor_control(camera_motor) :
    pin = 18 #핀번호 중요함
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 50)
    p.start(0)
    cnt = 0
    #이쪽은 모터 값이 더하고 빼고로 올듯.
    try:
            while True:
                    p.ChangeDutyCycle(1)
                    print "angle : 1"
                    time.sleep(1)
                    p.ChangeDutyCycle(5)
                    print "angle : 5"
                    time.sleep(1)
    except KeyboardInterrupt:
            p.stop()

    GPIO.cleanup()
    #현재의 카메라 각도를 반환한다

def food_motor_control(food_motor_request) :
    pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 50)
    p.start(0)
    cnt = 0

    degree = food_motor_request
    duty = 3.2 +  degree * (12.95 - 3.2) / 180
    p.ChangeDutyCycle(duty)
    GPIO.cleanup()

    #현재 feed통의 각도를 반환해라. 180은 열림 0은 닫힘.


def dht_control() :
    #현재 온습도를 반환한다.
    sensor = Adafruit_DHT.DHT11
    pin = 4
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    return h,t

# getserver의 경우 방울 홈의 경우 home 방울 켄넬 같은경우 kennel 로 진행한다.
def getserver(user, cmds) :  
    uri = url + '/start/' + user
    return requests.post(uri,json = cmds).json()
    #json 형태로 명령을 받고, 현재 상태도 받는다.
    # 구성요소는 모터, 온도, 또뭐있지??

def server_control() :
    global isUserUsing
    cmds = {'cmotor' : 0 , 'fmotor' : 90 , 'dht_h' : 0, 'dht_t' : 0 , 'dogs' : 0}
    #소켓을 통해서 현재 받아오고 있을때만 실행하면 될거같음.

    while isUserUsing == 1 : #isUserUsing이 1인 경우만 실행중이란 뜻이다.
        ret = getserver('home', cmds)
        camera_motor = ret['cmotor'] #추적용 카메라 모터의 움직임 명령을 받아온다
        food_motor_request = ret['fmotor'] #먹이 제공용 모터의 상태를 받아온다. (열림 닫힘)
        dog_count = ret['dogs']
        #개가 현재 없으면 찾아야함.
        #  개가 없으면 찾고 나서 마지막에 리퀘스트 한번 더 해올 것        



        camera = camera_motor_control(camera_motor)
        food = food_motor_control(food_motor_request)
        dht_h, dht_t = dht_contorl()

        #현재값을 갱신한다
        cmds['cmotor'] = camera
        cmds['fmotor'] = food
        cmds['dht_h'] = dht_h
        cmds['dht_t'] = dht_t


#쓰레드를 통해서 app을 지속적으로 실행시킨다. 이부분은 계속 받아오는 중이기 때문에 큰 문제가 되지 않는다
threading.Thread(target=server_control, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000')