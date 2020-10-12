from flask import Flask, request
from flask_cors import CORS
import subprocess
from PIL import Image
import os
import base64
import time
from threading import Thread

result = {"dog":"0", "shit":"0"}

app = Flask(__name__) 
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CORS(app)

@app.route("/")
def hello():                           
    return "Hello World!"


@app.route('/ml/image', methods=['POST'])
def receive_image():

    """ 클라이언트로 부터 이미지를 받아서 출력한다. """
    global result
    # jpg_string = request.json["data"]
    # jpg_string = jpg_string + '=' * (4 - len(jpg_string) % 4)
    # jpg_string = jpg_string.split(',')[-1]
    # imgdata = base64.b64decode(jpg_string)
    # with open('image.jpg', 'wb') as f:
    #     f.write(imgdata)
    # command = "./darknet detect cfg/yolov3.cfg yolov3.weights image.jpg"
    # with open("output.txt", "w+") as f:
    #     subprocess.call(command, shell=True, stdout=f)
    # with open("output.txt", "r") as f:
    #     lines = f.read().split("\n")
    # result = {"dog":"0", "shit":"0"}
    # for line in lines:
    #     if line.find('dog') > -1:
    #         percent = line.split(" ")[-1].split("%")[0]
    #         result["dog"] = percent
    
    # fake
    return result



@app.route('/vomit', methods=['POST'])
def change_answer():
    global result
    if request.json["data"] in ['y', 'Y']:
        result = {"dog":"100", "shit":"100"}
    else:
        result = {"dog":"0", "shit":"0"}
    return "Changed"


@app.route('/ml/learn', methods=['POST'])
def receive_image_for_learning():

    """ 캠서버로부터 학습할 이미지 샘플들을 받는다. 
        Production Mode가 아닐때만 사용하는 것이 좋다. """

    jpg_string = request.json["data"]
    jpg_string = jpg_string + '=' * (4 - len(jpg_string) % 4)
    jpg_string = jpg_string.split(',')[-1]
    imgdata = base64.b64decode(jpg_string)
    with open(f"{DIR_PATH}/images/images_cnt.txt", 'r') as f:
        cnt = int(f.readline())
    filename = f"{DIR_PATH}/images/images{str(cnt)}.jpg"
    with open(filename, 'wb') as f:
        f.write(imgdata)
    cnt += 1
    with open(f"{DIR_PATH}/images/images_cnt.txt", 'w+') as f:
        f.write(str(cnt))

    return "Image Received"






if __name__=='__main__':
    app.run(host='0.0.0.0', debug=Tr    ue)