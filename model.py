import os
import pickle
import numpy as np
import pandas as pd
from kagglehub import dataset_download
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
# Load Dataset
def load_dataset():
    dataset_path = dataset_download("atharvaingle/crop-recommendation-dataset")
    file_path = os.path.join(dataset_path, "Crop_recommendation.csv")
    return pd.read_csv(file_path)

df = load_dataset()

# Data Preprocessing
def preprocess_data(df):
    X = df.drop(columns=["label"])
    y = df["label"]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    return train_test_split(X, y_encoded, test_size=0.2, random_state=42), le

(X_train, X_test, y_train, y_test), le = preprocess_data(df)

# Train XGBoost with Hyperparameter Tuning
def train_xgboost(X_train, y_train):
    xgb = XGBClassifier(eval_metric="mlogloss", random_state=42)
    param_grid_xgb = {
        'n_estimators': [100, 200],
        'max_depth': [3, 6],
        'learning_rate': [0.01, 0.1],
    }
    grid_xgb = RandomizedSearchCV(xgb, param_distributions=param_grid_xgb, cv=5, scoring='accuracy', n_jobs=-1, n_iter=5)
    grid_xgb.fit(X_train, y_train)
    return grid_xgb.best_estimator_

best_xgb = train_xgboost(X_train, y_train)

# Save Model
def save_model(model, filename):
    with open(filename, "wb") as model_file:
        pickle.dump(model, model_file)

save_model(best_xgb, "xgb_crop_model.pkl")
# Load Model
def load_model(filename):
    with open(filename, "rb") as model_file:
        return pickle.load(model_file)

# Predict Crop
def predict_crop(input_features):
    model = load_model("xgb_crop_model.pkl")
    input_array = np.array([input_features]).reshape(1, -1)
    predicted_label = model.predict(input_array)[0]
    predicted_crop = le.inverse_transform([predicted_label])[0]
    return predicted_crop

# ✅ Data Preprocessing
X = df.drop(columns=["label"])  # Features
y = df["label"]  # Target variable

# Label Encoding
le = LabelEncoder()
y_encoded = le.fit_transform(y)


# Save the LabelEncoder
with open("label_encoder.pkl", "wb") as le_file:
    pickle.dump(le, le_file)
