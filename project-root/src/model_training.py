import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def load_data(file_path):
    """
    Load the processed data from a CSV file.

    Parameters:
    - file_path: Path to the processed CSV file.

    Returns:
    - DataFrame with the loaded data.
    """
    return pd.read_csv(file_path)

def preprocess_data(df):
    """
    Prepare data for training by separating features and target labels.

    Parameters:
    - df: DataFrame containing the processed data.

    Returns:
    - X: Features DataFrame.
    - y: Target labels.
    """
    # Define features and target label
    X = df.drop(columns=['Is Attack IP'])  # Modify target column as needed
    y = df['Is Attack IP']

    return X, y

def train_model(X_train, y_train):
    """
    Train a machine learning model on the provided training data.

    Parameters:
    - X_train: Features for training.
    - y_train: Labels for training.

    Returns:
    - Trained model.
    """
    # Initialize the model (RandomForestClassifier is used as an example)
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model on the test data.

    Parameters:
    - model: The trained model.
    - X_test: Features for testing.
    - y_test: Labels for testing.
    """
    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    # Print classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Print confusion matrix
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

def save_model(model, file_path):
    """
    Save the trained model to a file.

    Parameters:
    - model: The trained model.
    - file_path: Path to save the model.
    """
    joblib.dump(model, file_path)
    print(f"Model saved to {file_path}")

def main():
    # Define file paths
    processed_file_path = '/Users/kaushalkento/Desktop/GroupProject./CAPTCHARefinement./project-root/data/processed_rba-dataset.csv'
    model_file_path = '/Users/kaushalkento/Desktop/GroupProject./CAPTCHARefinement./project-root/models/rba_model.pkl'

    # Load and preprocess data
    df = load_data(processed_file_path)
    X, y = preprocess_data(df)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Save the trained model
    save_model(model, model_file_path)

if __name__ == "__main__":
    main()
