import joblib
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# 1. Get data
X, y = load_iris(return_X_y = True, as_frame = True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size = 0.8, random_state = 2022)

# 2. Preprocessing and train
scaler = StandardScaler()
classifier = SVC()

scaled_X_train = scaler.fit_transform(X_train)
scaled_X_valid = scaler.fit_transform(X_valid)
classifier.fit(scaled_X_train, y_train)

train_pred = classifier.predict(scaled_X_train)
valid_pred = classifier.predict(scaled_X_valid)

train_acc = accuracy_score(y_train, train_pred)
valid_acc = accuracy_score(y_valid, valid_pred)

print(train_acc)
print(valid_acc)

# 3. Save model
joblib.dump(scaler, "scaler.joblib")
joblib.dump(classifier, "classifier.joblib")