# 569

import joblib
import pandas as pd
import psycopg2
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

# 1. Get Data

db_connect = psycopg2.connect(host='localhost', database = 'jeewondatabase',user = 'jeewonuser',password='jeewonpassword')
df = pd.read_sql("SELECT * FROM breast_cancer ORDER BY id ASC LIMIT 569", db_connect)
X = df.drop(["id", "timestamp", "target"], axis="columns")
y = df["target"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, random_state=2022)

# 2. Preprocessing and train
model_pipeline = Pipeline([("scaler", StandardScaler()), ("dc", DecisionTreeClassifier())])
model_pipeline.fit(X_train, y_train)

train_pred = model_pipeline.predict(X_train)
valid_pred = model_pipeline.predict(X_valid)

train_acc = accuracy_score(y_train, train_pred)
valid_acc = accuracy_score(y_valid, valid_pred)

print("Train Accuracy :", train_acc)
print("Valid Accuracy :", valid_acc)

# 3. Save model
joblib.dump(model_pipeline, "jw_dc_pipeline.joblib")

# 4. Save data
df.to_csv("jw_dc.csv", index=False)