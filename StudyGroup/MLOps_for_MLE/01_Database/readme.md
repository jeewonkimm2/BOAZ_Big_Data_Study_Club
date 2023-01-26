# <목표>
1. Docker를 이용하여 PostgreSQL DB 서버 생성
2. 생성된 의 role name과 attributes 확인
3. ```psycopg2``` 패키지를 이용하여 테이블 생성 및 데이터 삽입
4. Dockerfile, Docker Compose 파일을 통해 Docker 컨테이너 안에서 계속해서 데이터를 생성하는 서비스 구축

```
PostgreSQL 이란?

PostgreSQL(포스트-그레스-큐엘 [Post-Gres-Q-L]로 발음)은 객체-관계형 데이터베이스 시스템(ORDBMS)으로, 엔터프라이즈급 DBMS의 기능과 차세대 DBMS에서나 볼 수 있을 법한 많은 기능을 제공하는 오픈소스 DBMS다.
실제 기능적인 면에서는 Oracle과 유사한 것이 많아, Oracle 사용자들이 가장 쉽게 적응할 수 있는 오픈소스 DBMS가 PostgreSQL이라는 세간의 평 또한 많다.

```


# <1> DB Server Creation

1. Docker를 통한 DB서버 생성


```
docker run -d --name postgres-server -p 5432:5432 -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase postgres:14.0
```

- 결과

  <img width="700" alt="Screenshot 2023-01-25 at 4 59 58 PM" src="https://user-images.githubusercontent.com/108987773/214509840-4a16158d-e724-43f5-a467-d36f07286398.png">
  
  <터미널>
  
  <img width="700" alt="Screenshot 2023-01-25 at 5 01 45 PM" src="https://user-images.githubusercontent.com/108987773/214510173-56b195c0-5b0a-4e5e-a9c6-32cd95082cf1.png">
  
  <도커 컨테이너 화면>

- postgres:14.0 이미지가 다운 되었으며, postgres-server 이름의 컨테이너가 생성됨

---
  
```
docker ps
```
- 위의 명령어를 통하여 DB서버가 생성되었는지 확인

- 결과
  
  <img width="700" alt="Screenshot 2023-01-25 at 5 10 07 PM" src="https://user-images.githubusercontent.com/108987773/214511386-5f2681c5-f8db-4020-a129-84a1587ec925.png">

---
  
```
/Library/PostgreSQL/15/scripts/runpsql.sh;
```

- 위의 명령어를 통하여 psql(PostgreSQL DB서버 확인할 때 사용)에 접근함

- 결과

  <img width="700" alt="Screenshot 2023-01-25 at 5 16 20 PM" src="https://user-images.githubusercontent.com/108987773/214512525-3dc0f186-114d-43dc-9d30-0b2a3a1e5d6a.png">
  
  - password => mypassword
---
```
\du
```

- 위의 명령어를 통하여 DB의 role name과 attribute를 확인

- 결과

  <img width="700" alt="Screenshot 2023-01-25 at 5 18 26 PM" src="https://user-images.githubusercontent.com/108987773/214512875-3a87a781-8c7f-4f9b-968a-bc1655d53a3c.png">
---
# <2> Table Creation

```
pip install pandas psycopg2-binary scikit-learn

```
- 위의 명령어를 통하여 필요한 패키지 설치

- psycopg2-binary 란? ([Ref][link1])
  - Psycopg 는 파이썬을 위한 PostgreSQL 어뎁터
  - 파이썬을 사용하여 PostgreSQL DB서버에 접근하는 코드를 구현하는 가장 간단한 방법은 psycopg2 패키지를 이용하는 것
  - 가장 빠르게 설치하는 방법이 ```$ pip install psycopg2-binary```
---
```
import psycopg2

db_connect = psycopg2.connect(
    user="myuser", 
    password="mypassword",
    host="localhost",
    port=5432,
    database="mydatabase",
)
```
- 위의 명령어를 통하여 DB에 접근. psycopg2의 connect 함수를 사용
- DB 연결시 기본적으로 5개의 정보가 필요
---
```
import pandas as pd
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y = True, as_frame = True)
df = pd.concat([X, y], axis = "columns")
```
- 위의 명령어를 사용하여 데이터 불러오기
---
```
def create_table(db_connect):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS iris_data (
        id SERIAL PRIMARY KEY,
        timestamp timestamp,
        sepal_length float8,
        sepal_width float8,
        petal_length float8,
        petal_width float8,
        target int
    );"""
    print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()
```
- 위의 명령어를 사용하여 테이블 생성
- ```db_connect.cursor() as cur```를 통해 connector에서 cursor 열기
- ```cur.execute(create_table_query)```를 통해 cursor에 query 전달
- ```db_connect.commit()```를 통해 query 실행하기 위해 connector에 commit
- ```cur.close()``` : cursor의 사용이 끝나면 종료
---
최종 코드 [table_creator.py][link2]

```
python table_creator.py
```
- 위 명령어를 사용하여 파이썬 스크립트 실행
- 결과

  <img width="700" alt="Screenshot 2023-01-25 at 10 49 30 PM" src="https://user-images.githubusercontent.com/108987773/214580521-87fbc61f-0e58-4b0d-9a3a-b9e05385932a.png">
---
```
\d
```
- psql을 통해 DB에 접속 후 테이블 확인
- 결과

  <img width="700" alt="Screenshot 2023-01-25 at 10 51 37 PM" src="https://user-images.githubusercontent.com/108987773/214580994-ed6669e4-6592-42f9-8914-c05539b6464f.png">
  
```
select * from iris_data;
```
- 위 명령어를 사용하여 iris_data 테이블에 있는 전체 데이터 확인
- 결과
  
  <img width="700" alt="Screenshot 2023-01-25 at 10 53 02 PM" src="https://user-images.githubusercontent.com/108987773/214581339-cf9b6ae3-3a0a-4a02-b6ef-ed4630bbeeba.png">
---
# <3> Data Insertion

1. 데이터 불러오고 함수 형태로 저장
```
import pandas as pd
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True, as_frame=True)
df = pd.concat([X, y], axis="columns")
rename_rule = {
    "sepal length (cm)": "sepal_length",
    "sepal width (cm)": "sepal_width",
    "petal length (cm)": "petal_length",
    "petal width (cm)": "petal_width",
}
df = df.rename(columns=rename_rule)
```
---
2. 데이터 row 1개 추출 후 DB 서버에 추가
- 최종 코드 [data_insertion.py][link3]

```
python data_insertion.py
```
- 위 명령어를 사용하여 파이썬 스크립트 실행
- 결과

  <img width="700" alt="Screenshot 2023-01-25 at 11 07 55 PM" src="https://user-images.githubusercontent.com/108987773/214584895-d1e04874-6be7-40ba-98f0-1f5f8d06bc4e.png">

```
select * from iris_data;
```
- 위 명령어를 사용하여 iris_data 테이블에 있는 전체 데이터 확인
- 결과
  
  <img width="700" alt="Screenshot 2023-01-25 at 11 09 12 PM" src="https://user-images.githubusercontent.com/108987773/214585175-36393640-28dc-4ab5-aa00-04bc61cd7180.png">
---
# <4> Data Insertion Loop

1. [data_insertion.py][link3] 를 바탕으로 ```while```문을 사용하여 코드 작성

- 최종 코드 [data_insertion_loop.py][link4]
- 결과

  <img width="700" alt="Screenshot 2023-01-26 at 1 26 51 PM" src="https://user-images.githubusercontent.com/108987773/214758476-bc1d0552-4339-49d0-95b1-2644ac19a38e.png">

  - ```command+C``` 를 하지 않는 이상 계속 추가됨
---
# <5> Data Generator on Docker

- 앞서 작성했던 코드를 Docker 컨테이너 안에서 실행하기 위해 Dockerfile 작성

1. 데이터를 생성하는 [data_generator.py][link5] 작성
  - 이전과의 차이점은 호스트를 받는 부분을 ```ArgumentParser```로 변경함
  
  ```
  ArgumentParser 란?
  프로그램 실행시 커맨드 라인에 인수를 받아 처리를 간단히 할 수 있도록 하는 표준 라이브러리
  
  ```
---
2. Dockerfile을 이용한 컨테이너 생성
  - 이미지 빌드
    ```
    docker build -t data-generator .
    ```
  - 결과
  
    <img width="700" alt="Screenshot 2023-01-26 at 1 37 27 PM" src="https://user-images.githubusercontent.com/108987773/214759465-f78cf215-0148-42b8-9790-40c67dd0fb47.png">
---
3. Docker Network
  <img width="300" alt="Screenshot 2023-01-26 at 1 39 46 PM" src="https://user-images.githubusercontent.com/108987773/214759730-2abf751e-62bc-404b-9c5a-c31091cf0888.png">
  
  - 포트 포워딩을 통하여 로컬에서 컨테이너 내부의 5432 포트인 DB에 접근할 수 있었음
  
  <img width="500" alt="Screenshot 2023-01-26 at 1 40 42 PM" src="https://user-images.githubusercontent.com/108987773/214759831-658aee1f-8d15-4f7f-8cca-0ac8cda108b0.png">
  
  - Data Generator 컨테이너를 실행시켰을 때, 위의 그림처럼 DB container와 연결해주어야함(두 개의 컨테이너가 통신할 수 있어야 함)
---
4. 해결책 - 네트워크 연결

```
docker network create my-network
```
  - 컨테이너 간 통신을 위한 네트워크 생성

```
docker network connect my-network postgres-server
```

  - DB 컨테이너를 생성된 네트워크에 연결
  
```
docker run -d \
  --name data-generator \
  --network "my-network" \
  data-generator "postgres-server"
```

  - data-generator 이미지를 이용하여 data-generator 이름의 컨테이너 생성
  - ```--network "my-network"```를 통하여 네트워크 이름 입력
  - 결과
  
    <img width="700" alt="Screenshot 2023-01-26 at 1 51 05 PM" src="https://user-images.githubusercontent.com/108987773/214760955-9167627e-ce75-457f-a05d-d4241bb21305.png">

    ```
    select * from iris_data;
    ```

    - 데이터가 계속 추가됨을 확인 
---
# <6> Data Generator on Docker Compose

- DB 컨테이너와 Data Generator 컨테이너를 함께 띄우기 위한 Docker Compose 파일 작성하기

1. Compose 파일 작성 [docker-compose.yaml][link6]

```
yaml 이란?

json과 xml처럼 데이터를 표현하는 방식
한눈에 구조를 알아보기 쉬운 장점이 있음
기본적으로 key-value형태로 표현
```

  - Docker Compose Healthcheck : postgres server가 사용 가능한 상태가 되어 있는지 체크를 한 뒤에 Data Generator를 띄워야 함
  
```
docker compose up -d
```

  - 위 명령어를 사용하여 yaml 파일 실행
  - 결과
  
    <img width="700" alt="Screenshot 2023-01-26 at 2 10 41 PM" src="https://user-images.githubusercontent.com/108987773/214762923-d871b40d-47e2-4c75-97ec-e6d845ac1a93.png">
    
```
docker network ls
```
  
  - 결과
    
    <img width="700" alt="Screenshot 2023-01-26 at 2 11 46 PM" src="https://user-images.githubusercontent.com/108987773/214763029-0f8de91e-a1c6-4328-a542-cdeb86521bc0.png">
    
    - ```mlops-network``` 가 생성됨 (터미널 현재 디렉토리가 mlops이기 때문)
---
2. 데이터 확인

  - 방법1 : 로컬 ```psql```을 이용하여 데이터가 계속 삽입됨을 확인

    <img width="700" alt="Screenshot 2023-01-26 at 2 15 16 PM" src="https://user-images.githubusercontent.com/108987773/214763385-6b95eeb4-8e07-4cc5-b8d0-97c61abbee3b.png">
    
  - 방법2 : Data Generator 컨테이너 안 ```psql```을 이용하여 DB접속
  
    - Data Generator 컨테이너 안으로 접속

      ```
      docker exec -it data-generator /bin/bash
      ```
    
        <img width="700" alt="Screenshot 2023-01-26 at 2 17 41 PM" src="https://user-images.githubusercontent.com/108987773/214763632-10d417c6-42ec-4403-9430-bccbd9f518d0.png">
  
  
      
    - psql 접속
    
      ```
      PGPASSWORD=mypassword psql -h postgres-server -p 5432 -U myuser -d mydatabase
      ```
---
```
docker compose down -v
```

  - 실행한 서비스들 종료
  
  
  
  
  
  
[link1]: https://www.psycopg.org/docs/install.html
[link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/01_Database/table_creator.py
[link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/01_Database/data_insertion.py
[link4]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/01_Database/data_insertion_loop.py
[link5]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/01_Database/data_generator.py
[link6]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/01_Database/docker-compose.yaml
