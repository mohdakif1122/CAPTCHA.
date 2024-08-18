import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

def process_chunk(chunk):
    """
    Process a chunk of data.

    Parameters:
    - chunk: A DataFrame representing a chunk of the CSV file.

    Returns:
    - Processed DataFrame.
    """
    # Drop rows with missing values in critical columns
    chunk = chunk.dropna(subset=['Login Timestamp', 'User ID', 'Round-Trip Time [ms]', 'IP Address', 'Country'])

    # Convert 'Login Timestamp' to datetime format using .loc[] to avoid SettingWithCopyWarning
    chunk.loc[:, 'Login Timestamp'] = pd.to_datetime(chunk['Login Timestamp'], errors='coerce')

    # Drop rows where 'Login Timestamp' couldn't be converted
    chunk = chunk.dropna(subset=['Login Timestamp'])

    # Convert 'Round-Trip Time [ms]' to numeric type
    chunk.loc[:, 'Round-Trip Time [ms]'] = pd.to_numeric(chunk['Round-Trip Time [ms]'], errors='coerce')

    # Normalize 'Round-Trip Time [ms]' using StandardScaler
    scaler = StandardScaler()
    chunk['Round-Trip Time [ms]'] = scaler.fit_transform(chunk[['Round-Trip Time [ms]']])

    # Convert categorical columns to category dtype for better performance
    chunk['Country'] = chunk['Country'].astype('category')
    chunk['Browser Name and Version'] = chunk['Browser Name and Version'].astype('category')

    # Encode categorical columns
    chunk['Country'] = chunk['Country'].cat.codes
    chunk['Browser Name and Version'] = chunk['Browser Name and Version'].cat.codes

    # Convert 'Login Successful', 'Is Attack IP', 'Is Account Takeover' to boolean
    chunk['Login Successful'] = chunk['Login Successful'].astype(bool)
    chunk['Is Attack IP'] = chunk['Is Attack IP'].astype(bool)
    chunk['Is Account Takeover'] = chunk['Is Account Takeover'].astype(bool)

    # Drop unnecessary columns (modify as needed)
    chunk = chunk.drop(columns=['IP Address', 'User Agent String'])

    return chunk

def main():
    """
    Main function to load, process, and save the data.
    """
    # Define file paths
    file_path = '/Users/kaushalkento/Desktop/GroupProject./CAPTCHARefinement./project-root/data/rba-dataset.csv'
    processed_file_path = '/Users/kaushalkento/Desktop/GroupProject./CAPTCHARefinement./project-root/data/processed1_rba-dataset.csv'

    # Ensure the 'data' directory exists
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)

    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return  # Exit the script if the file is not found

    # Define chunk size
    chunk_size = 1000000  # Adjust based on your memory constraints

    # Initialize an empty DataFrame to hold processed data
    processed_data = pd.DataFrame()

    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            print(f"Processing chunk of size {len(chunk)}")

            # Process the chunk
            processed_chunk = process_chunk(chunk)

            # Append the processed chunk to the final DataFrame
            processed_data = pd.concat([processed_data, processed_chunk], ignore_index=True)

    except Exception as e:
        print(f"An error occurred while processing the chunks: {e}")
        return

    # Check if processed_data is empty
    if processed_data.empty:
        print("Processed data is empty. No data to save or describe.")
        return

    # Save the processed data to a new CSV file
    try:
        processed_data.to_csv(processed_file_path, index=False)
        print(f"Processed data saved to {processed_file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return

    # Explore the processed dataset
    print("Processed Data Head:")
    print(processed_data.head())
    print("Processed Data Description:")
    print(processed_data.describe())

if __name__ == "__main__":
    main()
