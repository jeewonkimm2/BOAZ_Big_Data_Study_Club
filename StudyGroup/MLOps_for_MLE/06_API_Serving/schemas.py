# Pydantic Model로 스키마 클래스 작성

from pydantic import BaseModel

# Input schema
class PredictIn(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Output schema : 0,1,2 중에 하나가 될 것
class PredictOut(BaseModel):
    iris_class: int