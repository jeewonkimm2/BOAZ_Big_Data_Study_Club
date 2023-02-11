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
- **Query Parameter** : function parameter로는 사용되지만 Path Operation(이 경우에는 GET)에 포함되지 않아 Path Parameter라고 할 수 없는 Parameter
- [query_param.py][link2]
- 결과
  ```
  uvicorn query_param:app --reload
  ```
  - 위 명령어 실행
  
  - ```http://localhost:8000``` 에 접속
  
    <img width="660" alt="Screenshot 2023-02-09 at 8 10 29 PM" src="https://user-images.githubusercontent.com/108987773/217796752-2fc87f2d-4bec-48c5-b7d2-5a1f1be1b503.png">
    
    <img width="758" alt="Screenshot 2023-02-09 at 8 10 40 PM" src="https://user-images.githubusercontent.com/108987773/217796795-c92ce5b2-9309-442b-9bb4-a5134e8cd373.png">

  - ```http://localhost:8000/items/?skip=0&limit=10``` 에 접속
  
    <img width="757" alt="Screenshot 2023-02-09 at 8 11 57 PM" src="https://user-images.githubusercontent.com/108987773/217797102-7d56bdc1-9dde-4542-968a-bbc62b2c49b0.png">

    - Query는 URL에서 ```?``` 뒤에 key-value 쌍의 형태로 나타나고, ```&```으로 구분되어 사용됨
    - Query Parameter는 path의 고정부분이 아니기 때문에 optional으로 사용될 수 있고, 따라서 기본값을 가질 수 있음
    
  - ```http://localhost:8000/items/?skip=0&limit=2``` 에 접속 : 리스트[0:2]가 출력됨을 확인
  
    <img width="757" alt="Screenshot 2023-02-09 at 8 18 46 PM" src="https://user-images.githubusercontent.com/108987773/217798498-454faf77-5d14-49b0-aa5c-ca9700d8d7b6.png">
---
# <4> Multiple Path and Query Parameters 사용해보기
- Path Parameter와 Query Parameter를 모두 사용하여 Path Operation Function을 작성해보자
- [multi_param.py][link3]
  - Path Parameter : ```user_id```, ```item_id```
  - Query Parameter : ```q```, ```short```
- 결과
  ```
  uvicorn multi_param:app --reload
  ```
  - 위 명령어 실행
  
  - ```http://localhost:8000``` 에 접속
  
    <img width="662" alt="Screenshot 2023-02-09 at 8 33 40 PM" src="https://user-images.githubusercontent.com/108987773/217801652-5f001519-8b59-4895-b38a-7686a2c99081.png">
    
    <img width="755" alt="Screenshot 2023-02-09 at 8 33 52 PM" src="https://user-images.githubusercontent.com/108987773/217801702-1cce5e92-8955-4ac1-be7a-04a740445bec.png">

  - ```http://localhost:8000/users/3/items/foo-item``` 에 접속

    <img width="756" alt="Screenshot 2023-02-09 at 8 36 20 PM" src="https://user-images.githubusercontent.com/108987773/217802225-00a45298-26ab-4d13-95e2-27424012ff6d.png">
    
  - ```http://localhost:8000/users/3/items/foo-item?q=hello``` 에 접속

    <img width="757" alt="Screenshot 2023-02-09 at 8 37 54 PM" src="https://user-images.githubusercontent.com/108987773/217802508-b789ea5c-8cc7-4755-92e0-018baa7f76b6.png">

  - ```http://localhost:8000/users/3/items/foo-item?short=True``` 에 접속

    <img width="758" alt="Screenshot 2023-02-09 at 8 43 45 PM" src="https://user-images.githubusercontent.com/108987773/217803699-b173c51d-ea79-4988-8655-bae0f5319f9a.png">

  - ```http://localhost:8000/users/3/items/foo-item?q=hello&short=True``` 에 접속

    <img width="757" alt="Screenshot 2023-02-09 at 8 44 18 PM" src="https://user-images.githubusercontent.com/108987773/217803816-73d3164f-1a31-4787-bc9d-31dd6cb6f382.png">
---
# <5> API 명세서 작성 및 구현
- Path Parameter 사용시 : 각 API 에서 사용되는 파라미터를 Request Header 에 넣어 전달

  <img width="589" alt="Screenshot 2023-02-09 at 9 14 20 PM" src="https://user-images.githubusercontent.com/108987773/217810073-bcff03c6-7546-4829-85cc-8717e34fb7e0.png">
  
- Query Parameter 사용시 : 각 API 에서 사용되는 파라미터를 Request Body 에 넣어 전달

  <img width="476" alt="Screenshot 2023-02-09 at 9 15 05 PM" src="https://user-images.githubusercontent.com/108987773/217810227-a8dd5919-2167-4d7a-a506-52190ce58f05.png">

- Path Parameter를 활용하여 API 구현
  - [crud_path.py][link4]
  - 결과
    - ```uvicorn crud_path:app --reload``` 명령어 실행
      
      <img width="1330" alt="Screenshot 2023-02-09 at 9 17 24 PM" src="https://user-images.githubusercontent.com/108987773/217810749-affab050-f295-48e3-a325-bc365160f713.png">

- Query Parameter를 활용하여 API 구현
  - [crud_query.py][link5]
  - 결과
    - ```uvicorn crud_query:app --reload``` 명령어 실행
    
      <img width="755" alt="Screenshot 2023-02-09 at 9 21 38 PM" src="https://user-images.githubusercontent.com/108987773/217811612-89e9e3a0-df94-4e91-84a0-eaabc6647f0e.png">
---
# <6> Pydantic Model
- Pydantic Model
  - Client와 API 사이에 데이터를 주고 받을 때 데이터의 형식을 지정해줄 수 있는데 이를 위해 Pydantic Model을 사용할 수 있음
  - Request Body - Client에서 API로 전송하는 데이터, Response Body - API가 Client로 전송하는 데이터
- [crud_pydantic.py][link6]
  ```
  class CreateIn(BaseModel):
    name: str
    nickname: str
    
  class CreateOut(BaseModel):
    status: str
    id: int
  ```
  - Input(Request Body의 구성 요소가 될 변수), Output Schema(Response Body의 구성 요소가 될 변수)를 지정해줌

- 실행
  ```
  uvicorn crud_pydantic:app --reload
  ```
  - 결과
    
    <img width="569" alt="Screenshot 2023-02-11 at 11 02 59 PM" src="https://user-images.githubusercontent.com/108987773/218262161-cf4e18ba-2239-4efb-8ff3-7997b95ab6d7.png">
    
    - ```http://localhost:8000/docs``` 접속 : Swagger UI 화면 확인 가능
    
      <img width="758" alt="Screenshot 2023-02-11 at 11 04 09 PM" src="https://user-images.githubusercontent.com/108987773/218262213-fc26dc47-f045-4e3a-8342-2b805379d2e7.png">
    
- Pydantic Model의 장점
  - 비밀번호처럼 사용자가 필수적으로 입력해야 하지만 반환 값에는 나타나면 안되는 파라미터를 지정할 때 유용하게 






[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/main.py
[link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/path_param.py
[link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/query_param.py
[link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/multi_param.py
[link4]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/crud_path.py
[link5]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/crud_query.py
[link6]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/05_FastAPI/crud_pydantic.py
