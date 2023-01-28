# <목표>

1. Basic Workflow 구성하기 : Load Data -> Train Model -> Save Model

    ![image](https://user-images.githubusercontent.com/108987773/214774081-fdd47443-12cd-4269-b0e9-0ccc11901d09.png)

2. Database Workflow 구성하기 : Data Generator -> Postgres Server -> Query Data -> Train Model -> Save model
  
    ![image](https://user-images.githubusercontent.com/108987773/214774168-fec096f7-a703-48e1-b368-e119dbe75af7.png)

---
# <1> Base Model Development

1. ```pandas```, ```scikit-learn```, ```joblib``` 패키지 설치

```
pip install pandas scikit-learn joblib
```

  - ```joblib``` 이란? : scikit-learn에서 공식적으로 권장하는 모델 저장 방법
---
2. Basic Workflow 코드
      - 학습된 모델 저장 [base_train.py][link]
        - 결과 : [scaler.joblib][link6], [classifier.joblib][link7] 파일이 생성되어 저장됨
      - 저장된 모델 검증 [base_validate_save_model.py][link1]
---
# <2> Model Pipeline

1. 파이프라인을 활용한 Preprocessing & Train
    - 학습된 모델 저장 [pipeline_train.py][link2]
        - 결과 : [model_pipeline.joblib][link8] 파일이 생성되어 저장됨
    - 저장된 모델 검증 [pipeline_validate_save_model.py][link3]
---
# <3> Load Data from Database

1. Database Workflow 코드
    - 학습된 모델 저장 [db_train.py][link4]
        - ```pd.read_sql``` 는 입력 argument로 query와 DB connector를 받음
        - 결과1 : [data.csv][link5] - 내림차순(가장 큰 숫자 id부터)으로 총 100 개의 데이터가 저장됨
        - 결과2 : [db_pipeline.joblib][link9]
    - 저장된 모델 검증 [db_validate_save_model.py][link10]
---
# <4> Practice

1. 목표
    - [Breast cancer wisconsin dataset][link11] 을 활용하여 Database Workflow 설계하기
---    
2. [wisconsin_generator.py][link12]
    - DB 서버에 breast cancer 데이터를 추가하도록 파이썬 코드 작성
---    
3. [Dockerfile][link13]
    - Dockerfile을 이용하여 [wisconsin_generator.py][link12] 파일을 실행할 수 있는 이미지를 생성
    
    ```
    Dockerfile 이란?
    
    Dockerfile이란 docker에서 이용하는 이미지를 기반으로 하여 새로운 이미지를 스크립트 파일을 통해 내가 설정한 나만의 이미지를 생성할 수 있는 일종의 이미지 설정파일
    ```
---     
4. [docker-compose.yaml][link14]
    - postgres-server 환경 변경
        - 유저 : jeewonuser
        - 비밀번호 : jeewonpassword
        - DB : jeewondatabase
    - postgres-server와 data-generator는 ```jw-network```를 생성하여 연결
---     
5. [db_train.py][link15]
    - DB로부터 데이터를 추출하여 분석 후 모델 저장
    - *주의사항* : 모든 컨테이너 (DB서버, Data Generator)가 띄워진 상태에서 진행
    
        <img width="700" alt="Screenshot 2023-01-28 at 10 35 22 PM" src="https://user-images.githubusercontent.com/108987773/215269241-c62fc1c0-bbc9-48ed-8c5b-831185e93f61.png">
    - 학습시때와 다르게 DecisionTreeClassifier 사용
    - 결과
        - [jw_dc_pipeline.joblib][link16] 모델 생성
        - [jw_dc.csv][link17] 데이터 저장 csv 파일 생성
--- 
6. [db_validate_save_model.py][link18]
    - 저장된 모델 검증
    - 결과
        
        <img width="700" alt="Screenshot 2023-01-28 at 10 40 56 PM" src="https://user-images.githubusercontent.com/108987773/215269565-05f44508-2fb0-4721-bc42-87bfe9566192.png">



  
  [link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/base_train.py
  [link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/base_validate_save_model.py
  [link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/pipeline_train.py
  [link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/pipeline_validate_save_model.py
  [link4]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/db_train.py
  [link5]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/data.csv
  [link6]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/scaler.joblib
  [link7]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/classifier.joblib
  [link8]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/model_pipeline.joblib
  [link9]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/db_pipeline.joblib
  [link10]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/db_validate_save_model.py
  [link11]: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html
  [link12]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/wisconsin_generator.py
  [link13]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/Dockerfile
  [link14]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/docker-compose.yaml
  [link15]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/db_train.py
  [link16]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/jw_dc_pipeline.joblib
  [link17]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/jw_dc.csv
  [link18]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/wisconsin_practice/db_validate_save_model.py
