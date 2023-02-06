# <목표>

1. 모델을 MLflow 서버를 구축을 한 후 구축된 MLflow 서버에 저장, 관리 하는 방법을 학습
    
    ![image](https://user-images.githubusercontent.com/108987773/216822691-c64a0704-873c-4a3e-bea6-cf250ad7092f.png)

---
# <1> MLflow Setup

### Overview

<img width="500" alt="Screenshot 2023-02-06 at 1 50 00 PM" src="https://user-images.githubusercontent.com/108987773/216886197-618f8c66-14e4-45cc-a5fd-1029b3d0cc73.png">

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
---
# <2> Save Model to Registry

1. 패키지 설치

```
pip install boto3==1.26.8 mlflow==1.30.0 scikit-learn
```
---
2. 모델 저장 및 확인

- [기존 코드][link4]에 환경 변수 설정을 추가하자 => MLflow와 통신하기 위해

- 환경변수
    
    ```
    import os

    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
    os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5001"
    os.environ["AWS_ACCESS_KEY_ID"] = "minio"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "miniostorage"
    ```
    
    - MLFLOW_S3_ENDPOINT_URL : 모델을 저장할 Storage 주소
    - MLFLOW_TRACKING_URI : 정보를 저장하기 위해 연결할 MLflow 서버의 주소
    - AWS_ACCESS_KEY_ID : MinIO 접근 아이디
    - AWS_SECRET_ACCESS_KEY : MinIO 접근 비밀번호

- 모델 저장하기 : ```experiment```와 ```run```사용
    - experiment : MLflow에서 정보를 관리하기 위한 일종의 directory. 따로 지정하지 않으면 Default의 이름의 experiment에 저장됨
    - run : experiment에 저장되는 모델의 실험 결과

- 파일 실행 : [save_model_to_registry.py][link2]
    ```
    python save_model_to_registry.py --model-name "sk_model"
    ```
    
    - 결과
        
        <img width="1200" alt="Screenshot 2023-02-06 at 2 04 20 PM" src="https://user-images.githubusercontent.com/108987773/216887994-12d5db05-920e-40d2-882d-aa585d05d0a3.png">

        <img width="1200" alt="Screenshot 2023-02-06 at 2 05 22 PM" src="https://user-images.githubusercontent.com/108987773/216888108-2da3898c-34be-4324-95ae-4f0916916a87.png">
        
        - Localhost:5001 (MLflow 서버)
        - [data.csv][link3] 생성
        
    - 파일 실행시 주의사항
    
        <img width="1430" alt="Screenshot 2023-02-06 at 2 13 44 PM" src="https://user-images.githubusercontent.com/108987773/216888980-e3a9aa29-11fc-4907-bdbd-6807762acf7d.png">
        
        - 이전에 data-generator를 실행하여 저장한 데이터를 꺼내와서 실행해야함
---
# <3> Load Model from Registry

- 목표 : ```Save Model to Registry```에서 작성된 코드로 학습된 모델을 서버로부터 불러오는 코드 작성

    <img width="592" alt="Screenshot 2023-02-06 at 2 32 10 PM" src="https://user-images.githubusercontent.com/108987773/216891300-db537dc7-1e81-4caf-92aa-e67d5f3af227.png">


1. 파일 실행 : [load_model_from_registry.py][link5]

    ```
    python load_model_from_registry.py --model-name "sk_model" --run-id "877bc98dc7894f35a571b3bb45ac14b4"
    ```
    
    - 877bc98dc7894f35a571b3bb45ac14b4 : RUN ID로 MLflow experiment ID를 확인 후 추가함
    
        <img width="1671" alt="Screenshot 2023-02-06 at 2 26 14 PM" src="https://user-images.githubusercontent.com/108987773/216890665-1be8dcd2-a7df-4fbe-9052-3bd9bbbcb541.png">
        
    - 결과
    
        <img width="1324" alt="Screenshot 2023-02-06 at 2 29 22 PM" src="https://user-images.githubusercontent.com/108987773/216890956-db9f21dc-29dc-402c-bfa5-8004010cdb0b.png">

        - MLflow 서버의 metrics 를 확인하여 학습했던 결과와 같은지 확인
        
            <img width="338" alt="Screenshot 2023-02-06 at 2 30 02 PM" src="https://user-images.githubusercontent.com/108987773/216891118-7dfd42a5-f692-49f9-8f26-6acf6ef09c80.png">



        
        


        



[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/Dockerfile
[link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/docker-compose.yaml
[link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/save_model_to_registry.py
[link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/data.csv
[link4]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/db_train.py
[link5]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/03_Model_Registry/load_model_from_registry.py
