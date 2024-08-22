import os
import pandas as pd
from pytube import YouTube
import time

'''
Download videos from URLs obtained through 'crawling_urlave.py'.
Videos are saved in the 'download' folder.
'''

# Read links from the CSV file
csv_file_path = "/Users/imseohyeon/Documents/crawling/data/Youtube_search_df.csv"
df = pd.read_csv(csv_file_path)

# Define the download folder path
DOWNLOAD_FOLDER = "/Users/imseohyeon/Documents/crawling/download/"

# Create the download folder if it doesn't exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Iterate over each video and download
for idx, row in df.iterrows():
    video_url = row['url_link']
    try:
        # Get video information using Pytube
        yt = YouTube(video_url)
        length_seconds = yt.length

        # Set the filename
        filename = f"{idx}_video.mp4"

        # If the video length exceeds 5 minutes, download only the first 5 minutes
        if length_seconds > 5 * 60:
            print(f"{yt.title} video exceeds 5 minutes. Downloading only the first 5 minutes.")
            stream = yt.streams.filter(adaptive=True, file_extension='mp4').first()
            if stream:
                print(f"Downloading: {yt.title}")
                stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
                print(f"{yt.title} download complete")
            else:
                print(f"No highest quality stream available for {yt.title}.")
        else:
            # Download the entire video for videos less than 5 minutes long
            stream = yt.streams.get_highest_resolution()
            if stream:
                print(f"Downloading: {yt.title}")
                stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
                print(f"{yt.title} download complete")
            else:
                print(f"No highest quality stream available for {yt.title}.")
    except Exception as e:
        print(f"Failed to download {yt.title}: {e}")
