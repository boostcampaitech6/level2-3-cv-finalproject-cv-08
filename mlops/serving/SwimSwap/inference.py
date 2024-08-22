'''
Author: Naiyuan liu
Github: https://github.com/NNNNAI
Date: 2021-11-23 17:03:58
LastEditors: Naiyuan liu
LastEditTime: 2021-11-24 19:00:38
Description: 
'''

import cv2
import torch
import fractions
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import transforms
from insightface_func.face_detect_crop_single import Face_detect_crop
from util.mp4swap import mp4_swap
from util.upload_minio import upload_object
import os
import mlflow
from minio import Minio
import tempfile

from config import MLFLOW_S3_ENDPOINT_URL, MLFLOW_TRACKING_URI, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, MINIO_BUCKET, MINIO_ENDPOINT

torch.cuda.empty_cache()

os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["MINIO_BUCKET"] = MINIO_BUCKET
os.environ["MINIO_ENDPOINT"] = MINIO_ENDPOINT

print(MINIO_ENDPOINT, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY,MINIO_BUCKET)
client = Minio(MINIO_ENDPOINT, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, secure=True)

model = mlflow.pytorch.load_model("runs:/c7430d77a51a454cad5f315f38af9104/swimswap_pytorch").eval()

def face_synthesis_gif(face_image_url,base_video_url,request_id,result_id):
    def lcm(a, b): return abs(a * b) / fractions.gcd(a, b) if a and b else 0


    transformer_Arcface = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    crop_size = 224
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            object_path = "/".join(face_image_url.split("/")[4:])
            VOICE_MINIO_BUCKET = face_image_url.split("/")[3]
            
            print(VOICE_MINIO_BUCKET)
            client.fget_object(VOICE_MINIO_BUCKET, object_path, tmpfile.name)
            save_url = f"web_artifact/output/{request_id}_{result_id}_video.mp4"
            
            app = Face_detect_crop(name='antelope', root='./insightface_func/models')
            app.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640),mode="{}")
            with torch.no_grad():
                pic_a = tmpfile.name
                # img_a = Image.open(pic_a).convert('RGB')
                img_a_whole = cv2.imread(pic_a)

        try:
            img_a_align_crop, _ = app.get(img = img_a_whole,crop_size=crop_size)
        except TypeError:
            return 400, "low quality image"
            
        img_a_align_crop_pil = Image.fromarray(cv2.cvtColor(img_a_align_crop[0],cv2.COLOR_BGR2RGB)) 
        img_a = transformer_Arcface(img_a_align_crop_pil)
        img_id = img_a.view(-1, img_a.shape[0], img_a.shape[1], img_a.shape[2])
        # convert numpy to tensor
        img_id = img_id.cuda()


        #create latent id
        img_id_downsample = F.interpolate(img_id, size=(112,112))
        latend_id = model.netArc(img_id_downsample)
        latend_id = F.normalize(latend_id, p=2, dim=1)
        content_type = 'video/mp4'
        os.makedirs(os.path.dirname(save_url),exist_ok=True)
        make_flag = mp4_swap(base_video_url, latend_id, model, app, save_url,\
                        no_simswaplogo=True, use_mask=True, crop_size=crop_size)
        if make_flag:
            with open(save_url, 'rb') as file_data:
                file_stat = os.stat(save_url)
                upload_object(client, save_url, file_data,file_stat.st_size,VOICE_MINIO_BUCKET,content_type)
                os.remove(save_url)
        else:
            return 400, "make_flag error"
        return 200, f"https://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{save_url}"
    except Exception as ex:
        return 400, str(ex)



