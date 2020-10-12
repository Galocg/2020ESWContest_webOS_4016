# YOLO + Bangul

- 라이센스와 코드는 darknet yolo 코드를 그대로 가져옴(darknet license는 공개와 변경이 자유로움)
- 오픈라이센스 yolo를 이용할 예정
- server.py와 모델 weight가 주로 변경 되었음



## 실행 방법

1. 서버에 python3.6 환경 설치
   - 아래는 aws AMI 기준

```bash
sudo yum install python36 
python36 -m pip install --user --upgrade pip
```

2. git clone https://github.com/AntonMu/TrainYourOwnYOLO.git
3. requirements.txt 설치
4. https://blog.insightdatascience.com/how-to-train-your-own-yolov3-detector-from-scratch-224d10e55de2
   - 이후부터는 위 블로그대로 이미지 셋 생성후 동일하게 코드 실행
   - 아래는 트레이닝 중인 화면 캡처
   - ![image-20200808195219136](https://dogvomit.s3.ap-northeast-2.amazonaws.com/github_related/process_1.PNG)

## 앞으로 해야될 것

- 이미지 라벨링 잘하는 법 찾기
- 안좋은 샘플 사진과 좋은 샘플 사진 구별하는 방법 알아보기

  

## 주의사항

- 메모리부족할 경우 메모리킬이나며 실행이 안될 수 있음
- gpu를 사용하지 않을 시 연산 속도가 느릴 수 있음
- KeyError: 'val_loss'
  - 사진 개수가 부족할때 생김. 권장은 최소50장~100장이상으로 되어있음.



## 코드설명

- server.py
  - 메인서버와 통신하는 flask 
- requirements.txt
  - 라이브러리 참고

- output.txt

  - 메인서버의 이미지 결과값을 임시 텍스트파일로 결과물을 저장

  
