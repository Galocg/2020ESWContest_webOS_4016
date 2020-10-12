# Bangul_device-github-
"차량용 스마트 펫케어 서비스 : 방울이가타고있어요의 DEVICE CODE 입니다.


# 스트리밍 서비스 제작

1. gstreamer : gstreamer의 경우 자체 앱을 사용하여 스트리밍 하기 때문에 사용 할 수 없음

2. mjpeg Streamer : 기본적으로 영상을 사진 단위로 잘라서 보내기 때문에 활용하기 매우 편하다는 장점이 있음.
  사진으로 불러오기 때문에 머신러닝 등의 코드 적용에도 편리하고 프론트 엔드로 쉽게 가져 올 수 있는 장점이 존재함.
   
   ++ mjpeg Streamer 은 음성을 지원 하지 않기 때문에 음성을
   python 혹은 node.js를 통해 따로 스트리밍 해줄 방법이 필요.

3. WebRTC : html5의 사양으로 플러그인 없이 브라우저간 실시간 통신이 가능하게 하는기능
  오디오 스트리밍의 경우 node.js 를 활용하여 WebRTC통신 하는 것이 좋을 것으로 보임.
  그런데 어짜피 WebRTC 사용 할거면 영상도 WebRTC로?? 
  
 문제점
  => 라즈베리파이에서 WebRTC를 사용하기 위해 uv4l을 사용하였으나 일반적으로 사용되는 jessie, Strech와 다르게 현재 방울 홈 서비스의 버전은 booster여서 접근 키가 똑바로 안되어있는것 같음.
  https://ocaeb.altervista.org/en/uv4l-setup-for-raspbian-buster-lite/ 로 부스터 접근을 시도해보았지만 실패함.
  
 선종이네 집에 있는 라즈베리파이 3b모델을 사용해서 uv4l스트리밍을 시도해보고 성공하면 그것을 사용해보자.
 그게 안되면 다시 한번 부스터에서 다른 방법으로 접근 시도한다.


# 온습도 센서(DHT22)

1. DHT22센서 GPIO 연결
센서 맨 왼쪽 부터 1, 2, 3, 4
- 1번 : VCC - 3.3V
- 2번 : DATA - GPIO XX
- 4번 : GND - Ground

2. Adafruit DHT 설치
- git clone https://github.com/adafruit/Adafruit_Python_DHT.git
- cd Adafruit_Python_DHT
- sudo python setup.py install

3. 코드 작성
- 코드 작성시 pin은 2번 핀이랑 연결된 GPIO 값을 입력
- h, t = Adafruit_DHT.read_retry(sensor, pin) : 온도랑 습도 읽어오는 코드

4. 실행
- sudo python dht22.py

# 서보모터 작동(MGR 945)
1. 서보모터(MGR945) GPIO 연결
- 빨강 : VCC - 5v
- 갈색 : GND - Ground
- 주황 : DATA - GPIO XX

2. GPIO.RPi 라이브러리 install
- sudo apt-get update
- sudo apt-get install python-pri.gpio

3. 코드 작성
- duty 값 -> 보간법 이용 x = 3.2 + deg * ( 12.95 - 3.2 ) / 180 (0도 : 3.2, 180도 : 12.95)
- p.ChangeDutyCycle(duty) : 각도 변경 코드

# TensorFlow Lite 를 통한 object detection

1. 오픈 소스 다음 링크에 나온 과정을 따라한다. 
https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Raspberry_Pi_Guide.md#part-1---how-to-set-up-and-run-tensorflow-lite-object-detection-models-on-the-raspberry-pi
현재는 구글에서 제공된 detection 파일을 사용하고 있으며, 강아지 데이터는 새로 만들 예정에 있다. (혹은 수정)

2. 가상환경에서 작동되기 때문에 코드에서 서버로 값이 보내지는지 확인이 필요하다.
서버로 보내질 경우 각도를 통해 카메라의 회전 각을 보내주는 코드를 작성한다.

3.  Coral USB Accelerator 를 통해 연산속도를 현재 4fps 에서 24 fps 가량으로 늘릴 수 있다.
혁명이야!
