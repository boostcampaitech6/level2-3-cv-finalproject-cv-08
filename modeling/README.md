# Voice2Face-Modeling
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white">  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">  <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white">  <img src="https://img.shields.io/badge/NCP-03C75A?style=for-the-badge&logo=Naver&logoColor=white"> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=white">

## Project Structure

```  
modeling
┣ pytorch_template
┃ ┣ config
┃ ┣ models
┃ ┣ modules
┃ ┣ predict.py
┃ ┗ train.py
┣ sf2f
┃ ┣ datasets
┃ ┣ models
┃ ┣ options
┃ ┣ scripts
┃ ┣ utils
┃ ┣ infer.py
┃ ┣ inference_fuser.py
┃ ┣ test.py
┃ ┗ train.py
┣ SimSwap
┃ ┣ inference_swap.py
┃ ┗ test_*_swap*.py
┣ wcgan-gp
┃ ┣ dataset.py
┃ ┣ inference_options.py
┃ ┣ inference.py
┃ ┣ model.py
┃ ┣ train_options.py
┃ ┣ train.py
┃ ┗ utils.py
┣ README.md
┗ requirements.txt
```

## Usage

#### pytorch_template

 - `config`: 모델을 동작시킬 arguments를 모두 포함하는 config 파일들을 모아 놓은 폴더입니다.
 - `models`: model을 정의하고 build하는 코드들을 저장하는 폴더입니다.
 - `modules`: 모델을 학습시키는데 필요한 부가적인 파일들을 저장해 둔 폴더입니다. (dataloader, loss function, scaler, optimizer, metrics 등)
 - `predict.py` : 학습한 모델을 통해 inference를 실행시키는 코드입니다.
 - `train.py` : config 파일을 통해 build한 후 모델을 학습시키는 코드입니다.

#### sf2f

 - `datasets` : dataset을 build하는 코드들을 모아둔 폴더입니다.
 - `models` : voice encoder, embedding fuser, decoder, discriminator 등의 모델 전반적인 구조를 선언하고 build하는 파일들을 모아둔 폴더입니다.
 - `options` : 사용할 모델의 구조와 데이터 셋, 하이퍼파라미터 등의 arguments를 정리해 둔 config 파일들을 모아 놓은 폴더입니다.
 - `scripts` : mel spectrogram 변환, fid score 계산, inception score 계산 등의 기능들을 모아둔 폴더입니다.
 - `utils` : loss, evalutation, metrics, training utils 등의 모델 학습과 평가지표를 구성한 파일들을 모아둔 폴더입니다.
 - `infer.py`: voice를 spectrogram으로 변환시켜 입력하였을 때 encoder_decoder 구조만으로 결과를 생성하도록 하는 코드입니다.
 - `inference_fuser.py`: voice를 spectrogram으로 변환시켜 입력하였을 때 encoder_decoder 구조와 embedding fuser를 통해 향상된 결과를 생성하도록 하는 코드입니다.
 - `test.py`: 모델의 성능을 평가하기 위해 새로운 데이터셋으로 test를 진행하는 코드입니다.
 - `train.py`: 모델을 학습시키기 위해 사용되는 코드로, stage-1과 stage-2로 변경해서 사용할 수 있도록 구성되어 있습니다.

#### SimSwap

 - `inference_swap.py` : face image와 target video를 입력받고, frames 별로 얼굴을 합성한 후 최종 video의 frames과 fps를 출력하는 코드입니다.
 - ` test_*_swap*.py ` : 다양한 얼굴 합성을 수행합니다. 이미지/영상의 얼굴 하나에만, 이미지/영상의 모든 얼굴, 이미지/영상의 특정 얼굴 등 파일에 따라 target을 바꿀 수 있습니다.

#### wcgan-gp

 - `dataset.py` : argument로 지정된 dataset을 불러오도록 선언해둔 코드입니다.
 - `inference_options.py` : 학습된 모델에 inference를 위해 필요한 arguments를 parameter로 받는 코드입니다.
 - `inference.py` : arguments를 통해 성별과 나이를 condition으로 주어 모델을 통해 64x64 face image를 생성하는 코드입니다.
 - `model.py` : 모델을 (conditional GAN, Discriminator, convolutional block 등) 선언하여 build할 수 있도록 하는 코드입니다.
 - `train_options.py` : 모델을 학습시킬 때 사용되는 arguments를 parameter로 받는 코드로, pre-train 혹은 finetuning을 진행할 수 있도록 제어할 수 있는 argument도 있습니다.
 - `train.py` : arguments를 통해 모델을 선언하고 학습시키는 코드입니다.
 - `utils.py` : Gradient Penalty Loss와 그 이외의 추가적인 optinal한 함수들을 모아둔 코드입니다.

## Getting Started

  
### Setting up Vitual Enviornment

  
1. Initialize and update the server

```

su -

source .bashrc

```

  

2. Create and Activate a virtual environment in the project directory

  

```

conda create -n env python=3.8

conda activate env

```

  

4. To deactivate and exit the virtual environment, simply run:

  

```

deactivate

```

  

### Install Requirements

  

To Install the necessary packages liksted in `requirements.txt`, run the following command while your virtual environment is activated:

```

pip install -r requirements.txt

```
### SF2F
[Prepare](https://github.com/boostcampaitech6/level2-3-cv-finalproject-cv-08/blob/feat/modeling/modeling/sf2f/GETTING_STARTED.md#download-vggface2-resnet-checkpoint) \
[Training](https://github.com/boostcampaitech6/level2-3-cv-finalproject-cv-08/blob/feat/modeling/modeling/sf2f/GETTING_STARTED.md#launch-training) \
Inference for a service that generates faces from voices :
```
python sf2f/inference_swap.py --checkpoint_start_from CHEKPOINT_DIR/CHECKPOINT.pt --input_wav_file WAV_DIR/VOICE.wav
```


### WCGAN-GP
Training script for pre-train and finetuning model that generates faces from condition(gender, age) :
```
# train shell
python wcgan-gp/main.py --gpu_ids 0 --use_gpu True --mode {train/finetune/inference} --train_continue {on/off} --checkpoint_path {./checkpoint} --checkpoint_name {epoch1.pth} --checkpoint_fine_tune_name {fine_tune/epoch1.pth} --dataset_path /workspace/data --dataset_name celeba --dataset_fine_tune_name VoxCeleb --output_path ./results --num_epoch 100 --num_freq_save 5 --batch_size 128 --lr_G 2e-4 --lr_D 2e-4 --lr_policy {linear/step/plateau/cosine} --lr_G_weight_decay 1e-5 --lr_D_weight_decay 1e-5 --nch_ker 64 --fine_tune True --fine_tune_nume_epoch 100 --fine_tune_num_freq_save 5
```

Inference for a service that generates faces from condition(gender, age) :
```
# inference shell
python wcgan/main.py --mode {inference} --fine_tune {True, HQ-VoxCeleb dataset에 fine tune 진행여부} --output_path {inference 결과 저장 위치} --checkpoint_name {경로/checkpoint를 불러올 주소와 이름} --input_gendere {m/man/male/f/female/woman} --input_age {0 - 100}
```


### SimSwap
[Prepare](https://github.com/boostcampaitech6/level2-3-cv-finalproject-cv-08/blob/feat/modeling/modeling/SimSwap/docs/guidance/preparation.md) \
[Training](https://github.com/boostcampaitech6/level2-3-cv-finalproject-cv-08/tree/feat/modeling/modeling/SimSwap#training) \
[Inference for image or video face swapping](https://github.com/boostcampaitech6/level2-3-cv-finalproject-cv-08/blob/feat/modeling/modeling/SimSwap/docs/guidance/usage.md) \
Inference for a service that swaps only one face within the video :
```
python SimSwap/inference_swap.py --Arc_path SimSwap/arcface_model/arcface_checkpoint.tar --pic_a_path ./demo_file/hj.png --video_path ./demo_file/tae_24fps.mp4
```

## References
[Speech Fusion to Face](https://arxiv.org/pdf/2006.05888.pdf) 

[Conditional GAN](https://arxiv.org/pdf/1411.1784.pdf)

[Sim Swap](https://arxiv.org/pdf/2106.06340v1.pdf)

[Pytorch Template](https://github.com/victoresque/pytorch-template)



- [Origin github](https://github.com/Make-Zenerator/voice2face-modeling.git)
