import pandas as pd
from sklearn.ensemble import IsolationForest

# Load Zeek conn.log
try:
    df = pd.read_csv("/data/conn.log", delim_whitespace=True, comment='#', engine='python')
except Exception as e:
    print("Could not load log:", e)
    exit()

# Extract features
features = ['duration', 'orig_bytes', 'resp_bytes']
df = df[features].dropna()

# Train isolation forest
model = IsolationForest(contamination=0.01)
model.fit(df)

# Predict anomalies
df['anomaly'] = model.predict(df)

# Print suspicious entries
print(df[df['anomaly'] == -1])

