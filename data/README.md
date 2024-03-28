
# 🔊 Voice2Face-Data

<img  src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img  src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"> <img  src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img  src="https://img.shields.io/badge/NCP-03C75A?style=for-the-badge&logo=Naver&logoColor=white"> <img  src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=white"> <img  src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white"> <img  src="https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=Numpy&logoColor=white"> <img  src="https://img.shields.io/badge/Pytorch-EE4C2C?style=for-the-badge&logo=Pytorch&logoColor=white"> <img  src="https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=FFmpeg&logoColor=white">

## Project Structure
```
data
┣ audio
┃ ┣ audio_check_dB.py
┃ ┣ audio_crop.py
┃ ┗ audio_wav_cropping.py
┣ crawling
┃ ┣ crawling_detect.py
┃ ┣ crawling_rename_video.py
┃ ┣ crawling_select_csv.py
┃ ┣ crawling_urlsave.py
┃ ┗ crawling_videosave.py
┣ image
┃ ┣ image_clipseg2.py
┃ ┗ image_face_frame.py
┣ relabel
┃ ┣ relabel_detect_getframe.py
┃ ┣ relabel_select_csv.py
┃ ┗ relabel_Vox_age.py
┣ total
┃ ┣ total_audio_video_image.py
┃ ┗ total_origin_remove.py
┣ video
┃ ┣ video_clipimage.py
┃ ┗ video_download.py
┗ README.md
┗ requirements.txt
```

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

To Insall the necessary packages liksted in `requirements.txt`, run the following command while your virtual environment is activated:
```
pip install -r requirements.txt
```

## Usage

#### Training

To train the model with your custom dataset, set the appropriate directories for the training images and model saving, then run the training script.

```
python train.py --data_dir /path/to/images --model_dir /path/to/model
```

#### Inference

For generating predictions with a trained model, provide directories for evaluation data, the trained model, and output, then run the inference script.

```
python inference.py --data_dir /path/to/images --model_dir /path/to/model --output_dir /path/to/model
```
