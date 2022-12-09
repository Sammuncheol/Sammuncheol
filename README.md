# Sammuncheol
## 들어가기 전
과실 분쟁의 해결 절차는 일반적으로 시간과 비용이 매우 크게 들고, 보험사의 결정에 불만이 있을 때 사용할 수 있는 온라인상의 전문가에게(한문철TV 등) 제보, 상담받는 경우 역시 시간이 오래 걸리며 답변이 확실히 온다는 보장 역시 없습니다. 이에 본 프로젝트에서는 비 전문가들이 믿고 사용할 수 있는 차량 사고 과실 비율을 분석하는 인공지능 서비스를 만드는 것을 목표로 합니다. 하지만 차량 간의 교통사고는 아주 다양한 도로 상황에서 다양한 양상으로 나타나기 때문에 우선은 사고 유형을 사고가 일어난 도로의 종류에 따라 나누고 그 중 직선도로, 신호등 없는 사거리 교차로, T자형 교차로의 경우로 교통사고 유형을 축소하여 서비스를 우선 만들어보고자 합니다.

## 프로젝트 아키텍쳐(변경 가능)
전체 프로젝트는 파이썬을 기반으로 합니다. 웹페이지는 ```django```를 이용해 구축 및 배포를 할 예정입니다. 회원 정보 및 회원이 올린 영상의 이름과 서비스를 통해 산정된 과실 비율 등을 저장할 데이터베이스는 ```mysql```로 구축할 예정이며, 사용자가 올린 영상은 ```tencent cloud의 COS 혹은 Amazon web service의 S3 ```같은 오브젝트 스토리지에 저장할 예정입니다. 
즉, 사용자가 영상을 제출하면 우선 오브젝트 스토리지에 저장한 후, 파일 네임을 데이터베이스에 저장하고, ```keras```를 통해 학습된 R-CNN 모델이 해당 영상을 어떤 케이스라고 생각되는지 분류하게 됩니다. 

## 실행 환경
crash_normal_classification.ipynb : google colab<br>
prototype : aws ec2 ubuntu server

![ezgif-4-15afba9afc](https://user-images.githubusercontent.com/108507011/206701992-1e5e2279-a842-4e98-a1a7-9b7e9979048f.gif)


## 구현 참고 자료
R-CNN video classification: https://github.com/ddioni/keras-io/blob/master/examples/vision/video_classification.py


## 1차 프로토타입
프로토타입 링크 : https://cloud.protopie.io/p/2f1ca30d6a

프로토타입 사용을 위한 로그인 정보 
```
id : test
passwd : test
```

웹 사이트 프로토타입으로 영상 업로드 탭에는 crash가 없는 블랙박스 영상이 예시로 들어가 있습니다. 

![crash 없는 경우](https://user-images.githubusercontent.com/71022583/206725036-b1cc66b8-1f39-4832-ac9e-a0282633c74b.gif)
crash가 없는 경우

![crash 있는 경우](https://user-images.githubusercontent.com/71022583/206725073-c5ab7f3e-ca7b-4471-a567-0d0efde13584.gif)
crash가 있는 경우

(* 해당 이미지는 프로토타입이기 때문에 임의의 예시 영상을 이용한 것이기 때문에 실제와 다를 수 있다)
