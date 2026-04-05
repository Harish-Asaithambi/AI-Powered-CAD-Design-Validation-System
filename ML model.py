import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


MODEL_PATH = "models/compliance_model.pkl"
DATA_PATH = "data/training_data.csv"


def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[["thickness", "hole_diameter", "hole_distance", "edge_distance", "fillet_present"]]
    y = df["label"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def load_model():
    if not os.path.exists(MODEL_PATH):
        return train_model()
    return joblib.load(MODEL_PATH)


def predict_design(model, thickness, hole_diameter, hole_distance, edge_distance, fillet_present):
    sample = [[thickness, hole_diameter, hole_distance, edge_distance, fillet_present]]
    prediction = model.predict(sample)[0]
    return prediction
