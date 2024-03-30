FROM python:latest

RUN mkdir /backend
WORKDIR /backend

COPY . /backend/

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables for ffmpeg and ffprobe
ENV FFMPEG_PATH /usr/bin/ffmpeg
ENV FFPROBE_PATH /usr/bin/ffprobe

# for error message
ENV PYTHONUNBUFFERED 1

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]