# <목표>

<img width="972" alt="Screenshot 2023-02-17 at 3 10 04 PM" src="https://user-images.githubusercontent.com/108987773/219563341-f7c8bc6f-0753-4fa3-a308-413a41be5bc9.png">

- FastAPI를 이용하여 데이터를 입력받아 모델의 예측값을 반환하는 REST API 구현
---
# <1> Model API

1. 환경 설정

```
pip install boto3==1.26.8 mlflow==1.30.0 "fastapi[all]" pandas scikit-learn
```
- 사용할 패키지 설치

```
docker rm --force api-server
```
- 포트가 겹치는 문제를 막기 위해 [05. FastAPI][link] 에서 띄운 Docker 컨테이너 종료

2-1. 사전 준비
- ch3에서 작성한 도커 파일 실행 : [Dockerfile][link2], [docker-compose.yaml][link3]
- [download_model.py][link1]







[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/tree/main/StudyGroup/MLOps_for_MLE/05_FastAPI
[link1]: 
[link2]: 
[link3]: 
