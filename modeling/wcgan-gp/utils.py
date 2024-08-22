import os
import torch
import torch.nn as nn
from torch.optim import lr_scheduler
import torch.nn.functional as F
import logging
import numpy as np

import matplotlib.pyplot as plt
from torchvision.transforms import Normalize
from torchvision.transforms.functional import to_pil_image
from torchmetrics.image.fid import FrechetInceptionDistance

    
class GradientPaneltyLoss(nn.Module):
    def __init__(self):
        super(GradientPaneltyLoss, self).__init__()

    def forward(self, y, x):
        """Compute gradient penalty: (L2_norm(dy/dx) - 1)**2."""
        weight = torch.ones_like(y)
        dydx = torch.autograd.grad(outputs=y,
                                   inputs=x,
                                   grad_outputs=weight,
                                   retain_graph=True,
                                   create_graph=True,
                                   only_inputs=True)[0]

        dydx = dydx.view(dydx.size(0), -1)
        dydx_l2norm = torch.sqrt(torch.sum(dydx ** 2, dim=1))
        return torch.mean((dydx_l2norm - 1) ** 2)
    

def calculate_fid(generator, val_loader, batch_size=32):

    values = []
    fid = FrechetInceptionDistance(feature=64)

    with torch.no_grad():
        for images, gender_labels, age_labels in val_loader:
            age_labels = age_labels.unsqueeze(1)
            gender_labels = gender_labels.unsqueeze(1)
            age_condition = torch.zeros(batch_size, 8)
            age_condition.scatter_(1, age_labels, 1)
            condition = torch.cat([gender_labels, age_condition], dim=1).to('cuda')
            noise = torch.randn(images.size(0), 100).to('cuda')
            fake_images = generator(noise, condition)
            fake_feature = extract_features(fake_images).to('cpu')
            real_feature = extract_features(images)

            fid.update(real_feature.to(torch.uint8), real=True)
            fid.update(fake_feature.to(torch.uint8), real=False)
            values.append(fid.compute())
            fid.reset()
    
    return np.mean(values)

def extract_features(images):
    # Inception v3 모델에 이미지 전처리 및 특징 추출
    up = nn.Upsample(size=(299, 299), mode='bilinear', align_corners=False)
    norm = Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    features = norm(up(images))
    features = F.adaptive_avg_pool2d(features, output_size=64)
    features = F.sigmoid(features)
    return features

def model_save(dir_chck, netG, netD, optimG, optimD, epoch, start_time):
    if not os.path.exists(os.path.join(dir_chck, start_time)):
        os.makedirs(os.path.join(dir_chck, start_time))

    torch.save({'netG': netG.state_dict(), 'netD': netD.state_dict(),
                'optimG': optimG.state_dict(), 'optimD': optimD.state_dict()},
                '%s/%s/model_epoch%04d.pth' % (dir_chck, start_time, epoch))


def model_load(ckpt, netG, netD=[], optimG=[], optimD=[], epoch=[], mode='train'):

    dict_net = torch.load(ckpt)

    print(f'Loaded {ckpt}')

    if mode == 'train' or mode == 'finetune':
        netG.load_state_dict(dict_net['netG'])
        netD.load_state_dict(dict_net['netD'])
        optimG.load_state_dict(dict_net['optimG'])
        optimD.load_state_dict(dict_net['optimD'])
        st_epoch = ckpt.split("epoch")[1]
        st_epoch = int(st_epoch.split(".pth")[0])
        return netG, netD, optimG, optimD, st_epoch

    elif mode == 'test' or mode == 'inference':
        netG.load_state_dict(dict_net['netG'])

        return netG
    

def custom_collate_fn(batch):
    images, gender_labels, age_labels = zip(*batch)
    images = torch.stack(images, dim=0).float()  # 이미지를 torch.Tensor로 변환하고 float로 변환
    gender_labels = torch.tensor(gender_labels)
    age_labels = torch.tensor(age_labels)
    return images, gender_labels, age_labels


def set_requires_grad(nets, requires_grad=False):
    """Set requies_grad=Fasle for all the networks to avoid unnecessary computations
    Parameters:
        nets (network list)   -- a list of networks
        requires_grad (bool)  -- whether the networks require gradients or not
    """
    if not isinstance(nets, list):
        nets = [nets]
    for net in nets:
        if net is not None:
            for param in net.parameters():
                param.requires_grad = requires_grad


def get_scheduler(optimizer, opt):
    """Return a learning rate scheduler

    Parameters:
        optimizer          -- the optimizer of the network
        opt (option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions.
                            opt.lr_policy is the name of learning rate policy: linear | step | plateau | cosine

    For 'linear', we keep the same learning rate for the first <opt.n_epochs> epochs
    and linearly decay the rate to zero over the next <opt.n_epochs_decay> epochs.
    For other schedulers (step, plateau, and cosine), we use the default PyTorch schedulers.
    See https://pytorch.org/docs/stable/optim.html for more details.
    """
    if opt.lr_policy == 'linear':
        def lambda_rule(epoch):
            lr_l = 1.0 - max(0, epoch + opt.epoch_count - opt.n_epochs) / float(opt.n_epochs_decay + 1)
            return lr_l
        scheduler = lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda_rule)
    elif opt.lr_policy == 'step':
        scheduler = lr_scheduler.StepLR(optimizer, step_size=opt.lr_decay_iters, gamma=0.1)
    elif opt.lr_policy == 'plateau':
        scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.2, threshold=0.01, patience=5)
    elif opt.lr_policy == 'cosine':
        scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=opt.n_epochs, eta_min=0)
    else:
        return NotImplementedError('learning rate policy [%s] is not implemented', opt.lr_policy)
    return scheduler


def append_index(dir_result, fileset, step=False):
    index_path = os.path.join(dir_result, "index.html")
    if os.path.exists(index_path):
        index = open(index_path, "a")
    else:
        index = open(index_path, "w")
        index.write("<html><body><table><tr>")
        if step:
            index.write("<th>step</th>")
        for key, value in fileset.items():
            index.write("<th>%s</th>" % key)
        index.write('</tr>')

    # for fileset in filesets:
    index.write("<tr>")

    if step:
        index.write("<td>%d</td>" % fileset["step"])
    index.write("<td>%s</td>" % fileset["name"])

    del fileset['name']

    for key, value in fileset.items():
        index.write("<td><img src='images/%s'></td>" % value)

    index.write("</tr>")
    return index_path


def add_plot(output, label, writer, epoch=[], ylabel='Density', xlabel='Radius', namescope=[]):
    fig, ax = plt.subplots()

    ax.plot(output.transpose(1, 0).detach().numpy(), '-')
    ax.plot(label.transpose(1, 0).detach().numpy(), '--')

    ax.set_xlim(0, 400)

    ax.grid(True)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    writer.add_figure(namescope, fig, epoch)

def gender_processing(input_genders, device='cpu') -> torch.Tensor:
    gender_tensors = torch.zeros((1, 2))
    for i, input_gender in enumerate(input_genders):
        gender = 0
        if input_gender in ['m', 'male', 'man'] or input_gender == 0 :
            gender = 0
        elif input_gender in ['f', 'female', 'woman'] or input_gender == 1:
            gender = 1
        gender_tensors[i][gender] = torch.tensor(1)
    return gender_tensors.to(device)

def age_processing(input_age):
    if type(input_age) == str:
        input_age = int(input_age)
    age_boundary = [3, 7, 14, 23, 36, 46, 58, 121]
    for i in range(len(age_boundary)):
        if input_age < age_boundary[i]:
            age = i
            break
    
    if age >= 8:
        age = 7
    
    return age

def save_image(image, path, start_time):
    img = image.cpu().squeeze(0)
    img = to_pil_image(img)
    if not os.path.exists(path):
        os.mkdir(path)
    img.save(os.path.join(path, f'{start_time}.jpeg'), "JPEG")