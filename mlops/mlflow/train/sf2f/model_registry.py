from options.opts import  options
import models
import torch
import os, glob
import mlflow
from utils.wav2mel import wav_to_mel
from datasets import imagenet_deprocess_batch, set_mel_transform, \
    deprocess_and_save, window_segment
    
os.environ["MLFLOW_S3_ENDPOINT_URL"] = ""
os.environ["MLFLOW_TRACKING_URI"] = ""
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
mlflow.set_experiment("new-exp")
model, _ = models.build_model(
            options["generator"],
            image_size=[128,128],
            checkpoint_start_from="/home/hojun/Documents/project/boostcamp/final_project/mlops/temp/voice2face-mlops/best_IS_with_model.pt")
model.cuda().eval()
    
voice_path = os.path.join("/home/hojun/Documents/project/boostcamp/final_project/mlops/mlflow/train/mlflow/sf2f/data/", '*.wav')
voice_list = glob.glob(voice_path)
filename = voice_list[0]
print(filename)



#데이터 전처리
mel_transform = set_mel_transform("vox_mel")
image_normalize_method = 'imagenet'
log_mel = wav_to_mel(filename)
float_dtype = torch.cuda.FloatTensor
log_mel = mel_transform(log_mel).type(float_dtype)

log_mel_segs = window_segment(
log_mel, window_length=125, stride_length=63)
log_mel = log_mel.unsqueeze(0)

with torch.no_grad():
    imgs_fused, others = model(log_mel_segs.unsqueeze(0))
    print("dksldklwkdlw : ",type(imgs_fused))
if isinstance(imgs_fused, tuple):
    imgs_fused = imgs_fused[-1]
imgs_fused = imgs_fused.cpu().detach()
imgs_fused = imagenet_deprocess_batch(
    imgs_fused, normalize_method=image_normalize_method)
for j in range(imgs_fused.shape[0]):
    img_np = imgs_fused[j].numpy().transpose(1, 2, 0) # 64x64x3
# img_np = torch.from_numpy(img_np)
# log_mel_segs = log_mel_segs.unsqueeze(0).cpu().numpy()
print(type(img_np))
print(type(log_mel_segs))
signature = mlflow.models.signature.infer_signature(model_input=log_mel_segs.unsqueeze(0).cpu().numpy(), model_output=img_np)
input_sample = log_mel_segs.unsqueeze(0).cpu().numpy()



with mlflow.start_run():
    mlflow.pytorch.log_model(
        pytorch_model=model,
        artifact_path = "sf2f_pytorch",
        signature= signature,
        input_example = input_sample,
        # pip_requirements = "rec.txt"
    )