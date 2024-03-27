import os
import pandas as pd
from moviepy.editor import VideoFileClip
import numpy as np
import face_recognition
import shutil

'''
Detects faces and audio in video clips and refines them.

Extracts faces from the video clips and selects segments with audio to rebuild new videos.
New videos are organized in the "processed_videos" folder.

'''

# Function to extract audio from video clips with detected faces
def extract_audio_with_face(video_clip, start_time, end_time):
    '''
    Extracts audio from a video clip with detected faces within a specified time range.

    Args:
        video_clip (VideoFileClip): Input video clip.
        start_time (float): Start time of the segment containing the detected faces.
        end_time (float): End time of the segment containing the detected faces.

    Returns:
        audio (AudioClip): Extracted audio clip.
    '''
    audio = video_clip.audio.subclip(start_time, end_time)
    return audio

# Function to extract audio from video clips with detected faces in multiple segments
def extract_audio_with_faces(video_clip, face_detections):
    '''
    Extracts audio from a video clip with detected faces in multiple segments.

    Args:
        video_clip (VideoFileClip): Input video clip.
        face_detections (list): List of tuples containing start and end times of segments with detected faces.

    Returns:
        final_audio (ndarray): Concatenated audio array from all detected face segments.
    '''
    audio_clips = []

    for start_time, end_time in face_detections:
        audio_clip = extract_audio_with_face(video_clip, start_time, end_time)
        audio_clips.append(audio_clip)

    final_audio = np.concatenate([clip.to_soundarray() for clip in audio_clips])
    return final_audio

# Function to detect faces in video clips
def detect_faces(video_clip):
    '''
    Detects faces in a video clip.

    Args:
        video_clip (VideoFileClip): Input video clip.

    Returns:
        face_detections (list): List of tuples containing start and end times of segments with detected faces.
    '''
    frames = [frame for frame in video_clip.iter_frames()]
    frame_rate = video_clip.fps
    frame_times = np.arange(len(frames)) / frame_rate
    face_detections = []

    for i, frame in enumerate(frames):
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            start_time = frame_times[max(0, i - 1)]
            end_time = frame_times[min(len(frames) - 1, i + 1)]
            face_detections.append((start_time, end_time))

    return face_detections

# Function to create a new video from detected face segments
def create_new_video(video_clip, face_detections, output_path):
    '''
    Creates a new video from detected face segments.

    Args:
        video_clip (VideoFileClip): Input video clip.
        face_detections (list): List of tuples containing start and end times of segments with detected faces.
        output_path (str): Path to save the new video.
    '''
    new_video_clip = None

    for start_time, end_time in face_detections:
        subclip = video_clip.subclip(start_time, end_time)
        if new_video_clip is None:
            new_video_clip = subclip
        else:
            new_video_clip = new_video_clip.append(subclip)

    new_video_clip.write_videofile(output_path)

# Read data from a CSV file
csv_file_path = "/Users/imseohyeon/Documents/crawling/data/Youtube_search_df.csv"
df = pd.read_csv(csv_file_path)

# Paths for input and output folders
DOWNLOAD_FOLDER = "/Users/imseohyeon/Documents/crawling/download/"
NEW_FOLDER = "/Users/imseohyeon/Documents/crawling/processed_videos/"

# Create a new folder if it doesn't exist
if not os.path.exists(NEW_FOLDER):
    os.makedirs(NEW_FOLDER)

# Process each video to extract audio from segments with detected faces and create new videos
for idx, row in df.iterrows():
    video_filename = f"{idx}_video.mp4"
    video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

    if os.path.exists(video_path):
        try:
            video_clip = VideoFileClip(video_path)
            face_detections = detect_faces(video_clip)

            if face_detections:
                final_audio = extract_audio_with_faces(video_clip, face_detections)
                output_path = os.path.join(NEW_FOLDER, f"{idx}_new_video.mp4")
                create_new_video(video_clip, face_detections, output_path)

                print(f"Processing complete for {video_filename}")
            else:
                print(f"No faces detected in {video_filename}")
        except Exception as e:
            print(f"Error processing {video_filename}: {e}")
    else:
        print(f"File {video_filename} does not exist.")

# Move processed videos to another folder
processed_files = os.listdir(NEW_FOLDER)
for file in processed_files:
    shutil.move(os.path.join(NEW_FOLDER, file), DOWNLOAD_FOLDER)

print("All videos processed")
