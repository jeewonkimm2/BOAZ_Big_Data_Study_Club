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




  
  
[link1]: https://www.psycopg.org/docs/install.html
[link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/01_Database/table_creator.py
