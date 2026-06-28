import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Generate synthetic training data (normal server behavior)
np.random.seed(42)
n_samples = 1000

# Normal metrics
cpu_normal = np.random.normal(30, 10, n_samples)      # avg 30% CPU
memory_normal = np.random.normal(50, 15, n_samples)   # avg 50% memory
disk_normal = np.random.normal(40, 10, n_samples)     # avg 40% disk

# Combine into dataframe
data = pd.DataFrame({
    'cpu_usage': np.clip(cpu_normal, 0, 100),
    'memory_usage': np.clip(memory_normal, 0, 100),
    'disk_usage': np.clip(disk_normal, 0, 100)
})

# Train Isolation Forest model
model = IsolationForest(
    contamination=0.1,
    random_state=42,
    n_estimators=100
)

model.fit(data)

# Save the model
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/anomaly_model.pkl')

print("Model trained and saved successfully!")
print(f"Training data shape: {data.shape}")
print(f"Sample data:\n{data.head()}")