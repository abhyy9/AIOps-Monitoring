import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

np.random.seed(42)
n_samples = 1000

# Updated normal ranges to match real server behavior
cpu_normal = np.random.normal(10, 5, n_samples)      # avg 10% CPU
memory_normal = np.random.normal(25, 8, n_samples)   # avg 25% memory
disk_normal = np.random.normal(32, 5, n_samples)     # avg 32% disk

data = pd.DataFrame({
    'cpu_usage': np.clip(cpu_normal, 0, 100),
    'memory_usage': np.clip(memory_normal, 0, 100),
    'disk_usage': np.clip(disk_normal, 0, 100)
})

model = IsolationForest(
    contamination=0.05,
    random_state=42,
    n_estimators=100
)

model.fit(data)

os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/anomaly_model.pkl')

print("Model retrained successfully!")
print(f"Normal ranges → CPU: ~10%, Memory: ~25%, Disk: ~32%")
