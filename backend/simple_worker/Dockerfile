FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt /
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

#COPY app.py /app.py
ADD . /simple_worker
WORKDIR /simple_worker

CMD ["celery", "-A", "tasks", "worker", "-l", "info", "--pool=gevent", "--concurrency=4"]
#-Q celery_worker
#ENTRYPOINT ['celery','-A','test_celery', 'worker', '--loglevel=info']