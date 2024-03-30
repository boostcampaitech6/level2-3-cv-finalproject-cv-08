import os
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from pydub import AudioSegment
import cv2
from facenet_pytorch import MTCNN
import subprocess

# Initialize MTCNN for face detection
mtcnn = MTCNN()

from moviepy.editor import VideoFileClip

# 1. 비디오에서 음성 추출
def extract_audio_from_video(video_file, audio_file):
    # ffmpeg를 사용하여 비디오에서 오디오 추출
    command = f"ffmpeg -i {video_file} -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_file}"
    subprocess.call(command, shell=True)

# 2. 사람 음성부분 추출 
def detect_human_voice(audio_file): 
    # 오디오 파일에서 사람 음성부분을 감지하여 해당 인덱스 반환
    y, sr = librosa.load(audio_file, sr=None)
    voice_segments = librosa.effects.split(y, top_db=18)
    voice_indices = []
    for start, end in voice_segments:
        if end - start >= sr * 1:  # 1초 이상인 경우에만 추가
            voice_indices.extend(range(start, end))
    return voice_indices 

# 3. 음성부분만 모아 다시 저장. + 비디오도 이 간격 맞춰 다시 저장 
def save_detected_voice(audio_file, video_file, save_audio_file, save_video_file):
    # 감지된 사람 음성부분을 추출하여 저장
    y, sr = librosa.load(audio_file, sr=None)
    voice_indices = detect_human_voice(audio_file)
    combined_audio = y[voice_indices]
    sf.write(save_audio_file, combined_audio, sr)

    # 비디오도 해당 음성에 맞게 잘라서 저장
    audio_clip = AudioSegment.from_wav(save_audio_file)
    video_clip = VideoFileClip(video_file)
    video_duration = int(video_clip.duration * 1000)  # 비디오의 길이를 정수로 변환
    if len(audio_clip) > video_duration:
        audio_clip = audio_clip[:video_duration]
    else:
        audio_clip += audio_clip[-1] * (video_duration - len(audio_clip))

    audio_clip.export(save_audio_file, format="wav")
    video_clip.write_videofile(save_video_file, codec='libx264', audio_codec='aac')

# 4. 새로운 비디오에서 얼굴인식되는 부분중에 frame 추출 + frame에서도 256x256으로 얼굴 부분 bbox 맞춰 잘라 이미지 저장. 
def extract_frames_with_faces(video_file, output_folder):
    # 비디오 파일에서 프레임 추출하여 얼굴을 인식하고 이미지 저장
    cap = cv2.VideoCapture(video_file)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    success, frame = cap.read()
    while success:
        frame_count += 1
        if frame_count % (10 * frame_rate) == 0:  # 10초마다 프레임 추출
            try:
                boxes, _ = mtcnn.detect(frame)
                if boxes is not None:
                    for i, box in enumerate(boxes):
                        x, y, w, h = [int(coord) for coord in box]
                        face_image = frame[y:y+h, x:x+w]
                        cv2.imwrite(os.path.join(output_folder, f"frame_{frame_count}_{i}.jpg"), face_image)
            except Exception as e:
                print(f"Failed to detect face in frame {frame_count}: {e}")
        success, frame = cap.read()
    cap.release()


# Define paths
video_file_path = "/Users/imseohyeon/Documents/voice2face-data/code/file/testvideo.mp4"
audio_file_path = "/Users/imseohyeon/Documents/voice2face-data/code/file/testaudio.mp3"
detected_voice_file_path = "/Users/imseohyeon/Documents/voice2face-data/code/file/combined_voice.wav"
output_frame_folder = "/Users/imseohyeon/Documents/voice2face-data/code/file/images"
trimmed_video_file_path = "/Users/imseohyeon/Documents/voice2face-data/code/file/trimmed_video.mp4"

# Convert audio file to WAV format
converted_audio_file_path = os.path.splitext(audio_file_path)[0] + ".wav"
AudioSegment.from_file(audio_file_path).export(converted_audio_file_path, format="wav")

# Extract audio from video
extract_audio_from_video(video_file_path, converted_audio_file_path)

# Create necessary folders
for folder in [output_frame_folder, os.path.dirname(detected_voice_file_path)]:
    os.makedirs(folder, exist_ok=True)

# Step 2: Save the detected human voice segment and corresponding video
save_detected_voice(converted_audio_file_path, video_file_path, detected_voice_file_path, trimmed_video_file_path)

# If no human voice segments are detected, delete the corresponding video file
if not os.path.exists(detected_voice_file_path):
    os.remove(trimmed_video_file_path)
else:
    # Step 3: Extract frames with detected faces every 10 seconds
    extract_frames_with_faces(trimmed_video_file_path, output_frame_folder)
