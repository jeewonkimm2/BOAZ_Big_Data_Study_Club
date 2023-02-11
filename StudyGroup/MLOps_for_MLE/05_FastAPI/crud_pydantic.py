from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class CreateIn(BaseModel):
    name:str
    nickname:str

class CreateOut(BaseModel):
    status:str
    id:int

app = FastAPI()

USER_DB = {}
NAME_NOT_FOUND = HTTPException(status_code=400, detail = "Name not found.")

@app.post("/users", response_model = CreateOut)
# Response Body에 필요한 변수는 CreateOut모델의 변수인 status와 id
def create_user(user:CreateIn):
    # parameter로 user를 입력받고, type은 CreateIn 임을 알 수 있음
    USER_DB[user.name] = user.nickname
    user_dict = user.dict()
    user_dict["status"]="success"
    user_dict["id"]=len(USER_DB)
    return user_dict
# create_user 함수의 입력으로는 CreateIn모델을 받고, CreateOut모델을 반환함으로써 request와 response를 할때 다른 변수를 사용할 수 있음

@app.get("/users")
def read_user(name:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname":USER_DB[name]}

@app.put("/users")
def update_user(name:str, nickname:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status":"success"}

@app.delete("/users")
def delete_user(name:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status":"success"}