import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import json
import requests
import json
import urllib.parse
import urllib.request
import ssl
context = ssl._create_unverified_context()
url = 'https://13.124.126.131'
port = 443


# getserver의 경우 방울 홈의 경우 home 방울 켄넬 같은경우 kennel 로 진행한다.
def getserver(user, cmds) :  
    uri = url + '/home/' + user +'?' # 스타트 좀 그런데
    data = urllib.parse.urlencode(cmds)

    req=urllib.request
    d=req.urlopen(uri + data, context=context)
    result= json.loads(d.read().decode())


    keylist = list(result.keys())
    for key in keylist :
        num = result.get(keylist)
        result.update({key : float(num)})

    return result

    #json 형태로 명령을 받고, 현재 상태도 받는다.
    # 구성요소는 모터, 온도, 또뭐있지??




def camera_motor_control(na, ra) :
    pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 50)
    p.start(0)

    #만약에 180도를 넘어가는 명령은 안들어오는게 좋을 것 같긴함.
    degree = (na + ra) 
    if degree > 180 :
        degree = 180
    if degree < 0 :
        degree = 0
    
    duty = 3.2 +  degree * (12.95 - 3.2) / 180
    p.ChangeDutyCycle(duty)
    GPIO.cleanup()

    return degree
    #현재의 카메라 각도를 반환한다

def food_motor_control(feed) :
    pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 50)
    p.start(0)

    if feed == 1 :
        degree = 180

    else : 
        degree = 0

    duty = 3.2 +  degree * (12.95 - 3.2) / 180
    p.ChangeDutyCycle(duty)
    GPIO.cleanup()

    return


def dht_control() :
    #현재 온습도를 반환한다.
    sensor = Adafruit_DHT.DHT11
    pin = 4
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    return h,t



def camera_find() :
    #while : 개를 찾을때 까지 계속해야함. 다만 타임 인터벌이 일정 수준 이상일때는 없다고 반환해야할것
    #30도 각도 차이로 돌고, request 계속 보내서 개 찾았는지 물어보기
    # 카메라를 돌리고, 서버에 리퀘스트를 보내서 개를 찾았는지 계속 확인해야함    
    # 찾자마자 각도 갱신시키고 나갈 것.
    pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 50)
    p.start(0)

    degree = 0
    dog_flag = 0
    while dog_flag == 0 : 
        #일단은 강아지를 찾을 때 까지 계속함
        duty = 3.2 +  degree * (12.95 - 3.2) / 180
        p.ChangeDutyCycle(duty)

        
        start_time = time.time()
        end_time = start_time + 2
        ret = {'FEED' : 0 , 'NOW_ANGLE' : degree , 'ROTATE_ANGLE' : 0, 'DHT_H' : 0, 'DHT_T' : 0 , 'DOG_FLAG' : 0}
        while end_time > start_time + 1.5 :
            ret = getserver('home', ret)
            dog_flag = ret['DOG_FLAG']
            if dog_flag != 0 :
                break
            end_time = time.time()

        if dog_flag != 0 :
            break
        #돌리기 전에 약간의 인터벌 필요
        degree = (degree+30)%180


    GPIO.cleanup()
    return
    

def server_control() :

    cmds = {'FEED' : 0 , 'NOW_ANGLE' : 90 , 'ROTATE_ANGLE' : 0, 'DHT_H' : 0, 'DHT_T' : 0 , 'DOG_FLAG' : 0}
    #소켓을 통해서 현재 받아오고 있을때만 실행하면 될거같음.

    while True :
        ret = getserver('device', cmds)

        now_angle= ret['NOW_ANGLE'] 
        rotate_angle= ret['ROTATE_ANGLE']
        dht_h= ret['DHT_H']
        dht_t= ret['DHT_T']
        feed= ret['FEED']
        dog_flag= ret['DOG_FLAG']
        

        #개가 현재 없으면 찾아야함.
        if dog_flag == 0 :
            camera_find()
            ret = getserver('home', cmds)
            now_angle= ret['NOW_ANGLE'] 
            rotate_angle= ret['ROTATE_ANGLE']
            dht_h= ret['DHT_H']
            dht_t= ret['DHT_T']
            feed= ret['FEED']
            dog_flag= ret['DOG_FLAG']
    
        #  개가 없으면 찾고 나서 마지막에 리퀘스트 한번 더 해올 것        
        now_angle = camera_motor_control(now_angle, rotate_angle)
        rotate_angle = 0
        food_motor_control(feed)
        dht_h, dht_t = dht_control()

        #현재값을 갱신한다
        cmds['NOW_ANGLE'] = now_angle
        cmds['ROTATE_ANGLE'] = rotate_angle
        cmds['DHT_H'] = dht_h
        cmds['DHT_T'] = dht_t
        cmds['FEED'] = feed
        cmds['DOG_FLAG'] = dog_flag


server_control()