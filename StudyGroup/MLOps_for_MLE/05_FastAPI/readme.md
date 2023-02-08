# <목표>

<img width="628" alt="Screenshot 2023-02-08 at 9 46 50 PM" src="https://user-images.githubusercontent.com/108987773/217533625-d1854edd-8081-43e7-8a6d-1a9d3ede7b0c.png">

- API 학습 : Python을 이용하여 API를 만들 수 있는 웹 프레임워크인 FastAPI 사용
- Docker를 이용하여 FastAPI로 만든 API를 실행하여 client가 서버에 request를 보냄. Request를 받은 API서버는 다시 client에게 response 를 줌
---
# <1> FastAPI Tutorial

1. FastAPI를 이용해 간단한 API 만들어보기

- 필요한 패키지 설치
  ```
  pip install "fastapi[all]"
  ```
- [main.py][link] 작성

  ```
  from fastapi import Fast API
  ```
    - API를 만들 수 있도록 하는 Python 클래스 FastAPI import하기
  
  ```
  app = FastAPI()
  ```
    - 인스턴스 생성
    - 인스턴스의 이름에 따라 ```uvicorn main:app --reload``` 에서 'app' 부분이 이름이 바뀜
    
  ```
  @app.get("/)
  def read_root():
    return {"Hello":"World"}
  ```
    - FastAPI로 하여금 path ```/```로 가서 ```GET``` operation을 수행하라는 의미

- 결과
  ```
  uvicorn main:app --reload
  ```
  - 위 명령어 실행
  
    <img width="570" alt="Screenshot 2023-02-08 at 10 10 14 PM" src="https://user-images.githubusercontent.com/108987773/217539223-3f31cfa7-8917-4f9e-8d56-f3bb2df2427b.png">
    
  - ```http://localhost:8000``` 에 접속
  
    <img width="760" alt="Screenshot 2023-02-08 at 10 11 14 PM" src="https://user-images.githubusercontent.com/108987773/217539427-7887b01a-0776-4a94-a3b3-29b9ffd0b6cd.png">

  - ```http://localhost:8000/docs```에 접속
  
    <img width="759" alt="Screenshot 2023-02-08 at 10 12 02 PM" src="https://user-images.githubusercontent.com/108987773/217539603-1af24497-81ec-45db-b98a-1868c40cd686.png">
    - Swagger UI에 의해 제공되는 interactive API documentation
---
# <2> Path Parameter 이해하기
- **Path Parameter** : Path Operation(이 경우에는 GET)에 포함된 변수로 사용자에게 입력받아 function의 argument로 사용되는 parameter
- [path_param.py][link1]
- 결과
  ```
  uvicorn path_param:app --reload
  ```
  - 위 명령어 실행
  
  - ```http://localhost:8000``` 에 접속
  
    <img width="414" alt="Screenshot 2023-02-08 at 10 27 25 PM" src="https://user-images.githubusercontent.com/108987773/217543139-a748474e-4ee2-4ef4-96a4-35208f187c23.png">
    
    <img width="759" alt="Screenshot 2023-02-08 at 10 26 38 PM" src="https://user-images.githubusercontent.com/108987773/217542962-497f8b53-95fe-41ea-871b-48e038e78b51.png">
    
  - ```http://localhost:8000/items/100``` 에 접속 (/items/숫자)
  
    <img width="431" alt="Screenshot 2023-02-08 at 10 28 38 PM" src="https://user-images.githubusercontent.com/108987773/217543436-87804b41-8129-4895-8fd7-a2e4c8ce78dc.png">
    
    <img width="755" alt="Screenshot 2023-02-08 at 10 28 55 PM" src="https://user-images.githubusercontent.com/108987773/217543491-1fb0aab0-890b-4ed9-beea-b42507a9ad22.png">
---
# <3> Query Parameter 이해하기

  
    








[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/main.py
[link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/path_param.py
