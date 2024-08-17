import pandas as pd
import os

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

    # Convert 'Login Timestamp' to datetime format using .loc
    chunk.loc[:, 'Login Timestamp'] = pd.to_datetime(chunk['Login Timestamp'], errors='coerce')

    # Convert 'Round-Trip Time [ms]' to numeric type using .loc
    chunk.loc[:, 'Round-Trip Time [ms]'] = pd.to_numeric(chunk['Round-Trip Time [ms]'], errors='coerce')

    # Convert 'Login Successful', 'Is Attack IP', 'Is Account Takeover' to boolean using .loc
    chunk.loc[:, 'Login Successful'] = chunk['Login Successful'].astype(bool)
    chunk.loc[:, 'Is Attack IP'] = chunk['Is Attack IP'].astype(bool)
    chunk.loc[:, 'Is Account Takeover'] = chunk['Is Account Takeover'].astype(bool)

    return chunk

def main():
    """
    Main function to load, process, and save the data.
    """
    # Define file paths
    file_path = ''
    processed_file_path = ''

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

    # Process the CSV file in chunks
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
