# <목표>

1. 모델을 MLflow 서버를 구축을 한 후 구축된 MLflow 서버에 저장, 관리 하는 방법을 학습
    
    ![image](https://user-images.githubusercontent.com/108987773/216822691-c64a0704-873c-4a3e-bea6-cf250ad7092f.png)

---
# <1> MLflow Setup

### Overview

![image](https://user-images.githubusercontent.com/108987773/216858765-55c7fee4-1e80-4a08-9b55-be0ac138cfaa.png)

- ```PostgresSQL DB Server``` : MLflow의 운영 정보, 모델 결과를 저장하는 물리적인 공간
- ```MinIO Server``` : 학습된 모델을 저장하는 물리적인 공간
- ```MLflow Server``` : 모델과 모델의 결과들을 관리하는 서버, Backend Store와 Artifact Store에 접근이 가능함

1. MLflow Backend Store (```PostgreSQL DB```)
- Backend Store : 수치 데이터(학습 결과 - accuray, f1-score 등)와 MLflow 서버의 정보(MLflow의 메타 데이터)들을 체계적으로 관리하기 위한 DB 서버

    - 실습 환경
        - image: postgres:14.0
        - environment:
        
            POSTGRES_USER: mlflowuser
            
            POSTGRES_PASSWORD: mlflowpassword
            
            POSTGRES_DB: mlflowdatabase
---
2. MLflow Artifact Store (```MinIO Server```)
- Artifact Store : MLflow에서 학습된 모델을 저장하는 Model Registry로써 이용하기 위한 스토리지(storage)서버. 체계적 관리가 가능하며 외부에 있는 스토리지 서버도 사용할 수 있다는 장점이 있음.

    ```
    MinIO Server란?
    
    - AWS의 S3를 대체할 수 있는 오픈 소스 고성능 개체 스토리지
    - AWS S3와도 호환이 가능하며 SDK도 동일하게 사용 가능
    - MLflow에서 S3를 모델 저장을 위한 스토리지로 권장하기 때문에 MinIO를 사용할 예정
    - AWS credential을 통해 MinIO 대신 S3를 사용해도 같은 결과를 얻을 수 있음
    ```
    
    - 실습 환경
        - image: minio/minio
        - environment:
        
            MINIO_ROOT_USER: minio
            
            MINIO_ROOT_PASSWORD: miniostorage
---
3. MLflow Server
- MLflow 서버에 필요한 패키지가 설치된 이미지 생성([Dockerfile][link])

    - 실습 환경
        - environment:
        
            AWS_ACCESS_KEY_ID: minio
            
            AWS_SECRET_ACCESS_KEY: miniostorage
            
            MLFLOW_S3_ENDPOINT_URL: http://mlflow-artifact-store:9000
            
           ```
           AWS_ACCESS_KEY_ID : AWS S3 의 credential 정보. MinIO 의 MINIO_ROOT_USER 와 동일
           
           AWS_SECRET_ACCESS_KEY : AWS S3 의 credential 정보. MinIO 의 MINIO_ROOT_PASSWORD 와 동일
           
           MLFLOW_S3_ENDPOINT_URL : AWS S3 의 주소를 설정. 여기서는 MinIO 의 주소와 동일
           ```
           
       - command:
         - /bin/sh
         - -c
         - |
         
           mc config host add mlflowminio http://mlflow-artifact-store:9000 minio miniostorage &&
           mc mb --ignore-existing mlflowminio/mlflow
           mlflow server \
           --backend-store-uri postgresql://mlflowuser:mlflowpassword@mlflow-backend-store/mlflow \
           --default-artifact-root s3://mlflow/ \
           --host 0.0.0.0
           
           ```
           MinIO 초기 버켓을 생성 하고, MLflow 서버를 실행
           
           mc config ~ : MinIO Client 를 활용해 MinIO 서버에 호스트를 등록
           mc mb ~ : 등록된 호스트를 통해 초기 버켓을 생성
           mlflow server : MLflow 서버를 동작
           --backend-store-uri : 명시된 정보를 통해 PostgreSQL DB 와 연결
           --default-artifact-root : 명시된 버켓을 통해 MinIO 의 초기 버켓과 연결
           ```
---
4. [Dockerfile][link]과 [Docker Compose][link1]를 이용하여 서비스 띄우기
- [Dockerfile][link]
    - FROM : Base 이미지는 Python 3.9가 포함되게 설정
    - RUN
        - ```git```(MLflow 서버 내부 동작),```wget```(MinIO Client 설치하기 위해) 설치
        - PostgreSQL DB, AWS S3 에 관련된 Python 패키지를 설치
        - ```wget```을 활용하여 MinIO Client 설치

- 실행
    ```
    docker compose up -d
    ```
    
    - 결과
    
        <img width="700" alt="Screenshot 2023-02-06 at 10 44 07 AM" src="https://user-images.githubusercontent.com/108987773/216863001-8e2e2a0b-0082-4874-820e-d8f8bf461cee.png">
        
        <img width="700" alt="Screenshot 2023-02-06 at 10 44 35 AM" src="https://user-images.githubusercontent.com/108987773/216863044-70cad882-b1a3-4d6e-bbbd-5f82b585d3fd.png">
        
            - ID : minio, PW : miniostorage으로 로그인 




[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/Dockerfile
[link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/docker-compose.yaml
