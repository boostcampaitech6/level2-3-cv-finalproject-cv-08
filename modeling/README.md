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
┣ cgan-gp
┃ ┣ inference.py
┃ ┗ train.py
┣ README.md
┗ requirements.txt
```

## Usage

#### pytorch_template

 - `config`: 모델을 동작시킬 argumentation을 모두 포함하는 config 파일들을 모아 놓은 폴더입니다.
 - `models`: model을 정의하고 build하는 코드들을 저장하는 폴더입니다.
 - `modules`: 모델을 학습시키는데 필요한 부가적인 파일들을 저장해 둔 폴더입니다. (dataloader, loss function, scaler, optimizer, metrics 등)
 - `predict.py` : 학습한 모델을 통해 inference를 실행시키는 코드입니다.
 - `train.py` : config 파일을 통해 build한 후 모델을 학습시키는 코드입니다.

#### sf2f

 - `datasets` : dataset을 build하는 코드들을 모아둔 폴더입니다.
 - `models` : voice encoder, embedding fuser, decoder, discriminator 등의 모델 전반적인 구조를 선언하고 build하는 파일들을 모아둔 폴더입니다.
 - `options` : 사용할 모델의 구조와 데이터 셋, 하이퍼파라미터 등의 argumentation들을 정리해 둔 config 파일들을 모아 놓은 폴더입니다.
 - `scripts` : mel spectrogram 변환, fid score 계산, inception score 계산 등의 기능들을 모아둔 폴더입니다.
 - `utils` : loss, evalutation, metrics, training utils 등의 모델 학습과 평가지표를 구성한 파일들을 모아둔 폴더입니다.
 - `infer.py`: voice를 spectrogram으로 변환시켜 입력하였을 때 encoder_decoder 구조만으로 결과를 생성하도록 하는 코드입니다.
 - `inference_fuser.py`: voice를 spectrogram으로 변환시켜 입력하였을 때 encoder_decoder 구조와 embedding fuser를 통해 향상된 결과를 생성하도록 하는 코드입니다.
 - `test.py`: 모델의 성능을 평가하기 위해 새로운 데이터셋으로 test를 진행하는 코드입니다.
 - `train.py`: 모델을 학습시키기 위해 사용되는 코드로, stage-1과 stage-2로 변경해서 사용할 수 있도록 구성되어 있습니다.

#### SimSwap

 - `inference_swap.py` : face image와 target video를 입력받고, frames 별로 얼굴을 합성한 후 최종 video의 frames과 fps를 출력하는 코드입니다.
 - ` test_*_swap*.py ` : 다양한 얼굴 합성을 수행합니다. 이미지/영상의 얼굴 하나에만, 이미지/영상의 모든 얼굴, 이미지/영상의 특정 얼굴 등 파일에 따라 target을 바꿀 수 있습니다.

#### cgan-gp

 - `inference.py`: 주어진 비디오에서 얼굴을 감지하고, 감지된 얼굴에 대해 성별과 연령을 추정하여 화면에 표시하고, 일정한 간격으로 프레임을 캡처하여 이미지 파일로 저장하는 기능을 수행합니다.
 - `train.py`: 이미지 폴더에서 이미지들을 읽어와 각 이미지의 나이를 예측하고, 가장 흔한 나이 그룹을 세서 출력하고, 그 결과를 CSV 파일에 저장하는 작업을 수행합니다.


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

  
## References
[Speech Fusion to Face](https://arxiv.org/pdf/2006.05888.pdf) 

[Conditional GAN](https://arxiv.org/pdf/1411.1784.pdf)

[Sim Swap](https://github.com/neuralchen/SimSwap)

[Pytorch Template](https://github.com/victoresque/pytorch-template)
  

