from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(title="AIOps Anomaly Detection API")

model = joblib.load('models/anomaly_model.pkl')

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
    input_data = np.array([[
        metrics.cpu_usage,
        metrics.memory_usage,
        metrics.disk_usage
    ]])

    prediction = model.predict(input_data)
    score = model.decision_function(input_data)
    is_anomaly = bool(prediction[0] == -1)

    cpu_gauge.set(metrics.cpu_usage)
    memory_gauge.set(metrics.memory_usage)
    disk_gauge.set(metrics.disk_usage)

    if is_anomaly:
        anomaly_counter.inc()

    return {
        "is_anomaly": is_anomaly,
        "anomaly_score": float(score[0]),
        "cpu_usage": metrics.cpu_usage,
        "memory_usage": metrics.memory_usage,
        "disk_usage": metrics.disk_usage,
        "status": "ANOMALY DETECTED! 🚨" if is_anomaly else "Normal ✅"
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "healthy"}
