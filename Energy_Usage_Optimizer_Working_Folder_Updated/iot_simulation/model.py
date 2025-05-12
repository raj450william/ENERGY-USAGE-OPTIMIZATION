import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Realistic example data: [[hour, day, temperature, appliance usage]]
X = np.array([
    [6, 1, 22.5, 300],
    [9, 2, 25.0, 1000],
    [14, 3, 30.0, 1500],
    [18, 4, 28.0, 1200],
    [21, 5, 26.0, 1300],
    [23, 6, 24.0, 800],
    [3, 7, 22.0, 400],
    [10, 1, 26.0, 1100],
    [16, 2, 29.0, 1700],
    [20, 3, 27.5, 1600]
])

# Corresponding target energy values in kWh
y = np.array([0.5, 1.2, 2.5, 2.0, 2.2, 1.0, 0.3, 1.3, 2.7, 2.4])

# Create and train model pipeline
model = make_pipeline(StandardScaler(), LinearRegression())
model.fit(X, y)

# Save model
joblib.dump(model, 'model/energy_model.pkl')
print("✅ Model trained and saved successfully.")
