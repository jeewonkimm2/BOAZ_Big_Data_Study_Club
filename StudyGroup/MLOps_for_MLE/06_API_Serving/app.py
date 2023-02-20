# app.py
import mlflow
import pandas as pd
from fastapi import FastAPI
from schemas import PredictIn, PredictOut

# 로컬에 다운로드 받은 모델을 불러옴 (Load Model)
def get_model():
    model = mlflow.sklearn.load_model(model_uri="./sk_model")
    return model

MODEL = get_model()

# Create a FastAPI instance
app = FastAPI()

# API에 POST/predict을 수행했을때 모델 결과를 반환할 수 있도록 하는 함수 작성
@app.post("/predict", response_model=PredictOut)
def predict(data: PredictIn) -> PredictOut:
    df = pd.DataFrame([data.dict()])
    pred = MODEL.predict(df).item()
    return PredictOut(iris_class=pred)