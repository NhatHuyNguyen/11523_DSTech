"""Rain-prediction API: takes 4 weather numbers, returns will_rain."""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

FEATURES = ["humidity", "temperature", "pressure", "wind_speed"]

model = joblib.load("model/rf.joblib")
app = FastAPI(title="Rain Prediction API v2")


class Weather(BaseModel):
    humidity: float      # %
    temperature: float   # degrees C
    pressure: float      # hPa
    wind_speed: float    # km/h


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(w: Weather):
    row = pd.DataFrame(
        [[w.humidity, w.temperature, w.pressure, w.wind_speed]], columns=FEATURES
    )
    prob_rain = float(model.predict_proba(row)[0][1])
    return {"will_rain": bool(prob_rain >= 0.5), "prob_rain": round(prob_rain, 3)}