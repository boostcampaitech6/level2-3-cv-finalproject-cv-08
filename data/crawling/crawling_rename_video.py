import os
import pandas as pd

'''
Match the video names in the 'download' folder with the index in the CSV.
This facilitates the subsequent video relabeling task.
'''

# Read links from the CSV file
csv_file_path = "/Users/imseohyeon/Documents/crawling/data/Youtube_search_df.csv"
df = pd.read_csv(csv_file_path)

# Path to the folder where downloaded videos are stored
DOWNLOAD_FOLDER = "/Users/imseohyeon/Documents/crawling/download/"

# Iterate over all files in the folder and rename them
for filename in os.listdir(DOWNLOAD_FOLDER):
    # Full path of the file
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    # Check if the file is a .mp4 file
    if filename.endswith(".mp4"):
        # Extract the index value from the file name (assuming the video title is stored as the index)
        idx = filename.split("_")[0]  # Example: "0_video.mp4" -> "0"
        # Create a new file name
        new_filename = f"{idx}_video.mp4"
        # Create the new file path
        new_file_path = os.path.join(DOWNLOAD_FOLDER, new_filename)
        # Rename the file
        os.rename(file_path, new_file_path)
        print(f"File renamed: {filename} -> {new_filename}")
