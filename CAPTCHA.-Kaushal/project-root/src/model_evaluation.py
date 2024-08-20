from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Load the model
model = load_model('../models/trained_model.h5')

# Print model summary to get input shape
print("Model summary:")
model.summary()

# Load the test data
data = pd.read_csv('../data/processed1_rba-dataset.csv')

# Convert timestamps to numeric features (adjust based on your specific needs)
data['Login Timestamp'] = pd.to_datetime(data['Login Timestamp'])
data['Login Timestamp'] = data['Login Timestamp'].map(lambda x: (x - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s'))

# Drop non-numeric columns and check for missing values
X_test = data.drop(columns=['Is Attack IP', 'Is Account Takeover'])
X_test = X_test.apply(pd.to_numeric, errors='coerce').fillna(0)

# Print the shape of X_test to match the model's input
print("Shape of X_test:", X_test.shape)

# Example target
y_test = data['Is Account Takeover']

# Scale features if needed
scaler = StandardScaler()
X_test_scaled = scaler.fit_transform(X_test)

# Print the shape of scaled data to ensure it matches model input
print("Shape of X_test_scaled:", X_test_scaled.shape)

# Make predictions
try:
    predictions = model.predict(X_test_scaled)
    predictions = (predictions > 0.5).astype(int)

    # Evaluate the model
    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)

    # Save the evaluation results
    with open('../reports/model_evaluation_report.txt', 'w') as f:
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(str(matrix))

except Exception as e:
    print("An error occurred during prediction:", e)
