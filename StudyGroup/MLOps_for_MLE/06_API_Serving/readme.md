# <목표>

<img width="972" alt="Screenshot 2023-02-17 at 3 10 04 PM" src="https://user-images.githubusercontent.com/108987773/219563341-f7c8bc6f-0753-4fa3-a308-413a41be5bc9.png">

- FastAPI를 이용하여 데이터를 입력받아 모델의 예측값을 반환하는 REST API 구현
---
# <Prerequisite>

<img width="700" alt="Screenshot 2023-02-20 at 9 44 42 AM" src="https://user-images.githubusercontent.com/108987773/219985984-61d3782e-d4f2-46ce-adbf-7a695060dda7.png">

- [Chapter 1][link]와 [Chapter 3][link1] 컨테이너를 띄운 상태에서 진행
---
# <1> Model API

1. 환경 설정

```
pip install boto3==1.26.8 mlflow==1.30.0 "fastapi[all]" pandas scikit-learn
```
- 사용할 패키지 설치

2. 모델 다운로드
- [download_model.py][link2] 스크립트 실행
  ```
  python download_model.py --model-name sk_model --run-id <run-id>
  ```
  
  - model name과 run-id 확인하는 방법
    - localhost:5001 접속
      
      <img width="496" alt="219986409-8dd999b4-c185-40c7-8478-d9d895bd3b3a" src="https://user-images.githubusercontent.com/108987773/219986553-37e7c08c-6b52-4a82-ae46-961c86064074.png">


  
- 결과
  - ```sk_model```이라는 [디렉토리][link5] 생성
  
    <img width="615" alt="Screenshot 2023-02-20 at 9 54 38 AM" src="https://user-images.githubusercontent.com/108987773/219986653-e6f12850-65fb-43ce-a5e1-6247a6a5877d.png">


3. Model API 명세서 작성

<img width="521" alt="Screenshot 2023-02-20 at 9 55 45 AM" src="https://user-images.githubusercontent.com/108987773/219986719-a29eaa39-bbcd-44d3-bdab-51f401b144f7.png">

```POST/predict```를 수행했을 때 Request Body로 iris 데이터를 전달해주면 Response Body 를 통해 예측된 값을 전달받음

4. Pydantic Model로 스키마의 클래스 작성

- [schemas.py][link3] : Input과 Output 스키마 작성

5. Predict API 구현

- [app.py][link4]

6. API 작동 확인

- API 실행
```
uvicorn app:app --reload
```
- 결과

  <img width="663" alt="Screenshot 2023-02-20 at 10 07 47 AM" src="https://user-images.githubusercontent.com/108987773/219987497-f2bec004-1b67-4730-a2f4-7036fc0e08f8.png">

  <img width="1198" alt="Screenshot 2023-02-20 at 10 06 39 AM" src="https://user-images.githubusercontent.com/108987773/219987438-34eda39f-e502-4d8a-ad4c-30a21e032a08.png">
  
  - http://localhost:8000/docs 접속
---
# <2> Model API on Docker Compose

- 앞서 작성한 API를 실행할 수 있는 Dockefile 작성

1. Dockerfile 작성
- [Dockerfile][link6] : 앞서 작성한 Model API를 작동시킬 수 있는 API 서버의 Docker 이미지 만들기

2. Docker Compose
- [dockeer-compose.yaml][link7] : Model API 서비스를 띄우는 Docker Compose 파일

3. 실행
```
docker compose up -d
```

- 결과

  <img width="1018" alt="Screenshot 2023-02-20 at 10 21 10 AM" src="https://user-images.githubusercontent.com/108987773/219988561-97d56b8f-cc09-4cf1-ab7d-0435d1944607.png">
  
  - http://localhost:8000/docs 접속 : Request Body의 형태에 알맞게 데이터를 전달해주면 Response Body 로 Inference 결과가 잘 반환됨
  - ```curl``` 사용하여 결과 확인
    ```
    curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"sepal_length": 6.7, "sepal_width": 3.3, "petal_length": 5.7, "petal_width": 2.1}'
    ```
    - 결과
    
      <img width="871" alt="Screenshot 2023-02-20 at 10 23 35 AM" src="https://user-images.githubusercontent.com/108987773/219988751-79c72803-b740-40c1-8089-8abb72d6c199.png">
      
      ```
      curl이란?
      
      오픈 소스로 개발되어 윈도우와 리눅스에 기본 설치되어 사용자 상호 작용 없이 작동하도록 설계된 서버로부터 데이터를 받거나 서버로 데이터를 전송하기 위한 명령 줄 유틸리티
      ```





[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/tree/main/StudyGroup/MLOps_for_MLE/01_Database
[link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/tree/main/StudyGroup/MLOps_for_MLE/03_Model_Registry
[link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/06_API_Serving/download_model.py
[link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/06_API_Serving/schemas.py
[link4]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/06_API_Serving/app.py
[link5]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/tree/main/StudyGroup/MLOps_for_MLE/06_API_Serving/sk_model
[link6]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/06_API_Serving/Dockerfile
[link7]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/06_API_Serving/docker-compose.yaml
