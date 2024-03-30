import os
import pandas as pd
from argparse import ArgumentParser

def parse_args():
    """
    Command-line arguments parser.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = ArgumentParser()

    parser.add_argument('--csv_file', type=str, default='output_test.csv',
                        help="Path to the CSV file containing data.")
    parser.add_argument('--data_path', type=str, default='origin/video',
                        help="Path to the directory containing files and folders.")
    parser.add_argument('--save_csv', type=str, default='new_output.csv',
                        help="Path to save the new CSV file.")

    args = parser.parse_args()
    return args

def list_files_and_folders(data_path):
    """
    List files and folders in the given directory path.

    Args:
        data_path (str): Path to the directory.

    Returns:
        list or None: List of files and folders if directory exists, otherwise None.
    """
    if os.path.isdir(data_path):
        items = os.listdir(data_path)
        return items
    else:
        return None

def main(csv_file, data_path, save_csv):
    """
    Main function to process data.

    Args:
        csv_file (str): Path to the CSV file.
        data_path (str): Path to the directory containing files and folders.
        save_csv (str): Path to save the new CSV file.
    """
    # Read CSV file
    csv_data = pd.read_csv(csv_file, header=None)

    # Get list of files and folders in the data path
    youtube_ids = list_files_and_folders(data_path)

    # Process each YouTube ID
    for youtube_id in youtube_ids:
        # Filter rows corresponding to the YouTube ID
        filtered_df = csv_data[csv_data[0].astype(str).str.contains(youtube_id)]
        first_row = filtered_df.iloc[0:1]

        # Extract information from file name
        file_name = list_files_and_folders(os.path.join(data_path, youtube_id))[0]
        file_name_list = file_name.split("_")
        
        # Add extracted information as new columns
        first_row[4] = file_name_list[0]
        first_row[5] = file_name_list[1]
        
        # Save to new CSV file
        first_row.to_csv(save_csv, mode="a", index=False, header=False)

if __name__ == '__main__':
    args = parse_args()
    main(**args.__dict__)
