from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import requests

app = FastAPI(title="AIOps Anomaly Detection API")

# Load the trained model
model = joblib.load('/app/models/anomaly_model.pkl')

# Prometheus metrics
anomaly_counter = Counter('aiops_anomalies_total', 'Total number of anomalies detected')
cpu_gauge = Gauge('aiops_cpu_usage', 'Current CPU usage')
memory_gauge = Gauge('aiops_memory_usage', 'Current memory usage')
disk_gauge = Gauge('aiops_disk_usage', 'Current disk usage')

class MetricsInput(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float

@app.get("/")
def root():
    return {"message": "AIOps Anomaly Detection API is running!"}

@app.post("/predict")
def predict_anomaly(metrics: MetricsInput):
    # Prepare input
    input_data = np.array([[
        metrics.cpu_usage,
        metrics.memory_usage,
        metrics.disk_usage
    ]])

    # Predict
    prediction = model.predict(input_data)
    score = model.decision_function(input_data)

    is_anomaly = prediction[0] == -1

    # Update Prometheus metrics
    cpu_gauge.set(metrics.cpu_usage)