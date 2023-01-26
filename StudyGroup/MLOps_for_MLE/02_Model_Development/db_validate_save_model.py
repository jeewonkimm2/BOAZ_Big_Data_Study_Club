import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# 1. Reproduce data
df = pd.read_csv("data.csv")
X = df.drop(["id", "timestamp", "target"], axis="columns")
y = df["target"]
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, random_state=2022)

# 2. Load model
pipeline_load = joblib.load("db_pipeline.joblib")

# 3. Validate
load_train_pred = pipeline_load.predict(X_train)
load_valid_pred = pipeline_load.predict(X_valid)

load_train_acc = accuracy_score(y_train, load_train_pred)
load_valid_acc = accuracy_score(y_valid, load_valid_pred)

print(load_train_acc)
print(load_valid_acc)