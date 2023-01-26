# <목표>
1. Basic Workflow 구성하기 : Load Data -> Train Data -> Save Model
---
# <1> Base Model Development

1. ```pandas```, ```scikit-learn```, ```joblib``` 패키지 설치

```
pip install pandas scikit-learn joblib
```

  - ```joblib``` 이란? : scikit-learn에서 공식적으로 권장하는 모델 저장 방법
---
2. 코드
  - 학습된 모델 저장 [base_train.py][link]
  - 저장된 모델 검증 [base_validate_save_model.py][link1]
---
# <2> Model Pipeline

1. 파이프라인을 활용한 Preprocessing & Train
- 학습된 모델 저장 [pipeline_train.py][link2]
- 학습된 모델 저장 [pipeline_validate_save_model.py][link3]

  
  
  
  
  [link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/base_train.py
  [link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/base_validate_save_model.py
  [link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/pipeline_train.py
  [link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/02_Model_Development/pipeline_validate_save_model.py
