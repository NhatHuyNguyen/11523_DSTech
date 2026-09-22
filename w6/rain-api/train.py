"""Train a small rain-prediction model and save it to model/rf.joblib."""
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

FEATURES = ["humidity", "temperature", "pressure", "wind_speed"]

# 1) make a small synthetic weather dataset (no download needed)
rng = np.random.default_rng(42)
n = 2000

X = pd.DataFrame(
    {
        "humidity": rng.uniform(20, 100, n),      # %
        "temperature": rng.uniform(0, 40, n),     # degrees C
        "pressure": rng.uniform(980, 1040, n),    # hPa
        "wind_speed": rng.uniform(0, 60, n),      # km/h
    },
    columns=FEATURES,
)

# 2) rain is more likely when humidity is high and pressure is low
score = (
    0.06 * X["humidity"]
    - 0.05 * (X["pressure"] - 1010)
    + 0.02 * X["wind_speed"]
    - 0.03 * X["temperature"]
)
prob_rain = 1 / (1 + np.exp(-2.0 * (score - 3.6)))
y = (rng.uniform(0, 1, n) < prob_rain).astype(int)

# 3) train and score
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model = RandomForestClassifier(n_estimators=200, random_state=42).fit(Xtr, ytr)

# 4) save the trained model for the API to load
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/rf.joblib")
print(f"saved model/rf.joblib | features: {FEATURES} | test accuracy: {model.score(Xte, yte):.4f}")