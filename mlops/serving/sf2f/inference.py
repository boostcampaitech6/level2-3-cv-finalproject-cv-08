import models
import torch
import os, glob
import mlflow
from utils.wav2mel import wav_to_mel
from utils.upload_minio import upload_object
from datasets import imagenet_deprocess_batch, set_mel_transform, \
    deprocess_and_save, window_segment
import mlflow
from PIL import Image
import io
from minio import Minio
from minio.error import S3Error
from flask import jsonify
from config import MLFLOW_S3_ENDPOINT_URL, MLFLOW_TRACKING_URI, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, MINIO_BUCKET, MINIO_ENDPOINT
import subprocess
import tempfile

torch.cuda.empty_cache()
model_url = "runs:/54d4991723104ba9b048df217bd32ce6/sf2f_pytorch"

#docker compose에서 지정해줘야함 Fastapi 
os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["MINIO_BUCKET"] = MINIO_BUCKET
os.environ["MINIO_ENDPOINT"] = MINIO_ENDPOINT

print(MINIO_ENDPOINT, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY,MINIO_BUCKET)
client = Minio(MINIO_ENDPOINT, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, secure=True)

model = mlflow.pytorch.load_model(model_url).cuda().eval()

def load_voice_to_face(model_url):
    global model
    model =  mlflow.pytorch.load_model(model_url).cuda().eval()
    
def generate_voice_to_face(voice_url,request_id,result_id):
    #file 정보를 받아오는 
    temp_folder_path = "./temp/"
    os.makedirs(temp_folder_path,exist_ok=True)
    save_path = os.path.join(temp_folder_path, os.path.basename(voice_url))
    object_path = "/".join(voice_url.split("/")[4:])
    GET_BUCKET_NAME = voice_url.split("/")[3]
    
    file_path = f"web_artifact/output/{request_id}_{result_id}_image.png"
    save_url = f"https://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{file_path}"
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with tempfile.NamedTemporaryFile(delete=False) as save_temp_file:
                save_temp_path = save_temp_file.name
            # MinIO 객체를 임시 파일로 다운로드
                client.fget_object(GET_BUCKET_NAME, object_path, temp_file.name)
                # wav 파일로 변환 => ffmpeg 명령어 실행 
                subprocess.run(['ffmpeg', '-i', temp_file.name,'-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '1', save_path])
                print(save_path)
                mel_transform = set_mel_transform("vox_mel")
                image_normalize_method = 'imagenet'
                log_mel = wav_to_mel(save_path)
        log_mel = mel_transform(log_mel).type(torch.cuda.FloatTensor)

        log_mel_segs = window_segment(log_mel, window_length=125, stride_length=63)
        log_mel = log_mel.unsqueeze(0)

        with torch.no_grad():
            imgs_fused, others = model(log_mel_segs.unsqueeze(0))
        if isinstance(imgs_fused, tuple):
            imgs_fused = imgs_fused[-1]
        imgs_fused = imgs_fused.cpu().detach()
        imgs_fused = imagenet_deprocess_batch(imgs_fused, normalize_method=image_normalize_method)
        for j in range(imgs_fused.shape[0]):
            img_np = imgs_fused[j].numpy().transpose(1, 2, 0) # 64x64x3

        pil_image = Image.fromarray(img_np)
        a = Image.open("ss_korean.png")
        # Save the image to an in-memory file
        in_mem_file = io.BytesIO()
        pil_image.save(in_mem_file, format="PNG")
        in_mem_file.seek(0)
        img_byte_arr = in_mem_file.getvalue()
        
        upload_object(client, file_path, in_mem_file, len(img_byte_arr), MINIO_BUCKET)
        os.remove(save_path)
        print(save_url)
        return 200, save_url
    except Exception as ex:
        print(ex)
        os.remove(save_path)
        return 400, str(ex)
# generate_voice_to_face("/home/hojun/Documents/project/boostcamp/final_project/mlops/pipeline/serving/sf2f/녹음_남자목소리_여잘노래.wav")
# generate_voice_to_face("http://223.130.133.236:9000/voice2face-public/mzRequest/00107_00109_voice_2024-03-22.wav",0,0)