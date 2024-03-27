import os
from torch.utils.data import Dataset

import pandas as pd
from PIL import Image
import random
from natsort import natsorted
import os

DATA_PATH = "/workspace/VoxCeleb/vox1"
FILE_NAME = "vox1_age_meta.csv"
CELEBA_PATH = 'data/50k'
FILE_PATH = os.path.join(DATA_PATH, FILE_NAME)

class HQVoxceleb(Dataset):
    def __init__(self, root_path="/workspace/VoxCeleb/vox1", file_name="vox1_age_meta.csv", data_folder="masked_faces", transform=None):
        super(HQVoxceleb, self).__init__()
        self.root_path = root_path
        self.data_folder_path = os.path.join(self.root_path, data_folder)
        self.file_path = os.path.join(root_path, file_name)
        self.df = pd.read_csv(self.file_path, sep='\t', index_col=False)
        self.transform = transform

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, index):
        data_path = os.path.join(self.data_folder_path, self.df["VGGFace1 ID"][index])
        image_name = random.choice(os.listdir(data_path))
        image_path = os.path.join(data_path, image_name)
        image = Image.open(image_path).convert('RGB')
        gender_label_str = self.df["Gender"][index]
        if gender_label_str == None:
            print(self.df["VGGFace1 ID"])
        age_label = int(self.df["age"][index])        # 문자열을 정수로 변환
        
        # 성별을 숫자로 매핑
        gender_label = 0 if gender_label_str == "m" else 1

        if self.transform:
            image = self.transform(image)
        return image, gender_label, age_label


class CelebADataset(Dataset):
  def __init__(self, root_dir="data", data_folder='50k', transform=None):
    """
    Args:
      root_dir (string): Directory with all the images
      transform (callable, optional): transform to be applied to each image sample
    """
    self.root_dir = root_dir
    self.data_folder_path = os.path.join(self.root_dir, data_folder)
    
    image_names = os.listdir(self.data_folder_path)
    self.transform = transform 
    self.image_names = natsorted(image_names)

  def __len__(self): 
    return len(self.image_names)

  def __getitem__(self, idx):
    # Get the path to the image 
    img_path = os.path.join(self.root_dir, self.image_names[idx])
    # Load image and convert it to RGB
    img = Image.open(img_path).convert('RGB')
    # Apply transformations to the image
    if self.transform:
      img = self.transform(img)

    return img
