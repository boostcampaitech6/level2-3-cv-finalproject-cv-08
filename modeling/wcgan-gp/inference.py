import os
import torch
import torch.nn as nn
from datetime import datetime

from model import ConditionLinearFinetuneGAN, init_net
from inference_options import InferenceOptions

from utils import model_load, gender_processing, age_processing, save_image

class Inference:
    def __init__(self, args):
        self.checkpoint_path = args.checkpoint_path
        self.checkpoint_name = args.checkpoint_name
        self.checkpoint_fine_tune_name = args.checkpoint_fine_tune_name

        self.output_path = args.output_path
        
        self.nch_ker = args.nch_ker

        self.fine_tune = args.fine_tune

        self.input_gender = args.input_gender
        self.input_age = args.input_age

        self.use_gpu = args.use_gpu
        self.gpu_ids = args.gpu_ids
        if self.use_gpu and torch.cuda.is_available():
            self.device = torch.device("cuda:%d" % self.gpu_ids[0])
            torch.cuda.set_device(self.gpu_ids[0])
        else:
            self.device = torch.device("cpu")

        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def inference(self):
        noise = 100
        device = self.device

        output_path = os.path.join(self.output_path, 'images')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            os.makedirs(output_path)

        netG = ConditionLinearFinetuneGAN(nch_in=noise)

        init_net(netG, init_type='normal', init_gain=0.02, gpu_ids=self.gpu_ids)
        netG.set_fine_tune(self.fine_tune)
        if self.fine_tune:
            new_sequence = nn.Sequential(
                nn.Linear(in_features=(noise+self.nch_ker//4+self.nch_ker//4), out_features=128),
                nn.ReLU(0.2),
                nn.Dropout(0.1)
            )
            netG.fc1 = new_sequence
            netG = netG.to(device)
            dir_ckpt = os.path.join(self.checkpoint_path, self.checkpoint_fine_tune_name)
        else:
            dir_ckpt = os.path.join(self.checkpoint_path, self.checkpoint_name)
        ckpt = os.listdir(dir_ckpt)
        ckpt.sort()

        model_path = os.path.join(dir_ckpt, ckpt[-1])
        netG = model_load(model_path, netG, mode=self.mode)
        with torch.no_grad():

            netG.eval()
            ## test phase

            # input = torch.randn(1, nch_in).to(device)
            noise = torch.randn(1, noise, device=device)
            gender = gender_processing(self.input_gender, device=device)
            # age = age_processing(self.input_age)
            age_conditions = torch.zeros(1, 8)
            age_conditions[0][self.input_age] = torch.Tensor(1)
            age_conditions = age_conditions.to(device)

            # output = netG(input, condition)
            output = netG((noise, gender, age_conditions))

            min_ = output.min()
            max_ = output.max()
            clipping = ((output-min_)/(max_-min_))

            save_image(clipping, output_path, self.start_time)
        
        return output_path
    
if __name__ == '__main__':
    opt = InferenceOptions().parse()

    INFERENCER = Inference(opt)
    output_path = INFERENCER.inference()
    print(output_path)