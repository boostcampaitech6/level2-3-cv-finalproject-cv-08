import torch
import torch.nn as nn
from torch.nn import init
from torch.optim import lr_scheduler
import numpy as np


## finetuning gan
class ConditionLinearFinetuneGAN(nn.Module):
    def __init__(self, nch_in=100, nch_out=3, nch_ker=64, norm='bnorm', fine_tune=False):
        super(ConditionLinearFinetuneGAN, self).__init__()

        self.nch_in = nch_in
        self.nch_ker = nch_ker
        self.norm = norm
        self.fine_tune = fine_tune

        self.gender_layer = nn.Sequential(
            nn.Linear(2, self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Linear(self.nch_ker, self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Linear(self.nch_ker, self.nch_ker//4),
            nn.LeakyReLU(0.2)
        )
        self.age_layer = nn.Sequential(
            nn.Linear(8, self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Linear(self.nch_ker, self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Linear(self.nch_ker, self.nch_ker//4),
            nn.LeakyReLU(0.2)
        )

        self.fc1 = nn.Sequential(
            nn.Linear(1 * self.nch_in,  2 * self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1)
        )
        self.fc2 = nn.Sequential(
            nn.Linear(2 * self.nch_ker,  4 * self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1)
        )
        self.fc3 = nn.Sequential(
            nn.Linear(4 * self.nch_ker,  16 * self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1)
        )
        self.fc4 = nn.Sequential(
            nn.Linear(16 * self.nch_ker,  32 * self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1)
        )
        self.fc5 = nn.Sequential(
            nn.Linear(32 * self.nch_ker,  self.nch_ker * self.nch_ker),
            nn.LeakyReLU(0.2),
        )
        self.fc6 = nn.Linear(self.nch_ker * self.nch_ker,  3 * self.nch_ker * self.nch_ker)

    def forward(self, x):
        if self.fine_tune:
            noize, gender, age = x
            gender = self.gender_layer(gender)
            age = self.age_layer(age)
            x = torch.concat((noize,gender,age), -1)
        x = self.fc1(x) # fine_tune : [batch_size, 132]
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.fc5(x)
        x = self.fc6(x)

        x = torch.tanh(x)

        x = x.reshape(-1, 3, 64, 64)

        return x

    # fine tune 학습 진행 시 forward 구조 변경을 위해 사용됨
    def set_fine_tune(self, fine_tune):
        self.fine_tune = fine_tune


class Discriminator(nn.Module):
    def __init__(self, nch_in=3, nch_ker=64, norm='bnorm'):
        super(Discriminator, self).__init__()

        self.nch_in = nch_in
        self.nch_ker = nch_ker
        self.norm = norm

        if norm == 'bnorm':
            self.bias = False
        else:
            self.bias = True

        self.dsc1 = CNR2d(1 * self.nch_in,  1 * self.nch_ker, kernel_size=4, stride=2, padding=1, norm=self.norm, relu=0.2)
        self.dsc2 = CNR2d(1 * self.nch_ker, 2 * self.nch_ker, kernel_size=4, stride=2, padding=1, norm=self.norm, relu=0.2)
        self.dsc3 = CNR2d(2 * self.nch_ker, 4 * self.nch_ker, kernel_size=4, stride=2, padding=1, norm=self.norm, relu=0.2)
        self.dsc4 = CNR2d(4 * self.nch_ker, 8 * self.nch_ker, kernel_size=4, stride=2, padding=1, norm=self.norm, relu=0.2)
        self.dsc5 = CNR2d(8 * self.nch_ker, 1,                kernel_size=4, stride=1, padding=1, norm=[],        relu=[], bias=False)

    def forward(self, x):

        x = self.dsc1(x)
        x = self.dsc2(x)
        x = self.dsc3(x)
        x = self.dsc4(x)
        x = self.dsc5(x)

        x = torch.sigmoid(x)

        return x


class CNR2d(nn.Module):
    def __init__(self, nch_in, nch_out, kernel_size=4, stride=1, padding=1, norm='bnorm', relu=0.0, drop=[], bias=[]):
        super().__init__()

        if bias == []:
            if norm == 'bnorm':
                bias = False
            else:
                bias = True

        layers = []
        layers += [Conv2d(nch_in, nch_out, kernel_size=kernel_size, stride=stride, padding=padding, bias=bias)]

        if norm != []:
            layers += [Norm2d(nch_out, norm)]

        if relu != []:
            layers += [ReLU(relu)]

        if drop != []:
            layers += [nn.Dropout2d(drop)]

        self.cbr = nn.Sequential(*layers)

    def forward(self, x):
        return self.cbr(x)


class Conv2d(nn.Module):
    def __init__(self, nch_in, nch_out, kernel_size=4, stride=1, padding=1, bias=True):
        super(Conv2d, self).__init__()
        self.conv = nn.Conv2d(nch_in, nch_out, kernel_size=kernel_size, stride=stride, padding=padding, bias=bias)

    def forward(self, x):
        return self.conv(x)

class Norm2d(nn.Module):
    def __init__(self, nch, norm_mode):
        super(Norm2d, self).__init__()
        if norm_mode == 'bnorm':
            self.norm = nn.BatchNorm2d(nch)
        elif norm_mode == 'inorm':
            self.norm = nn.InstanceNorm2d(nch)

    def forward(self, x):
        return self.norm(x)


class ReLU(nn.Module):
    def __init__(self, relu):
        super(ReLU, self).__init__()
        if relu > 0:
            self.relu = nn.LeakyReLU(relu, True)
        elif relu == 0:
            self.relu = nn.ReLU(True)

    def forward(self, x):
        return self.relu(x)


def init_weights(net, init_type='normal', init_gain=0.02):
    """Initialize network weights.

    Parameters:
        net (network)   -- network to be initialized
        init_type (str) -- the name of an initialization method: normal | xavier | kaiming | orthogonal
        init_gain (float)    -- scaling factor for normal, xavier and orthogonal.

    We use 'normal' in the original pix2pix and CycleGAN paper. But xavier and kaiming might
    work better for some applications. Feel free to try yourself.
    """
    def init_func(m):  # define the initialization function
        classname = m.__class__.__name__
        if hasattr(m, 'weight') and (classname.find('Conv') != -1 or classname.find('Linear') != -1):
            if init_type == 'normal':
                init.normal_(m.weight.data, 0.0, init_gain)
            elif init_type == 'xavier':
                init.xavier_normal_(m.weight.data, gain=init_gain)
            elif init_type == 'kaiming':
                init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
            elif init_type == 'orthogonal':
                init.orthogonal_(m.weight.data, gain=init_gain)
            else:
                raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
            if hasattr(m, 'bias') and m.bias is not None:
                init.constant_(m.bias.data, 0.0)
        elif classname.find('BatchNorm2d') != -1:  # BatchNorm Layer's weight is not a matrix; only normal distribution applies.
            init.normal_(m.weight.data, 1.0, init_gain)
            init.constant_(m.bias.data, 0.0)

    print('initialize network with %s' % init_type)
    net.apply(init_func)  # apply the initialization function <init_func>


def init_net(net, init_type='normal', init_gain=0.02, gpu_ids=[]):
    """Initialize a network: 1. register CPU/GPU device (with multi-GPU support); 2. initialize the network weights
    Parameters:
        net (network)      -- the network to be initialized
        init_type (str)    -- the name of an initialization method: normal | xavier | kaiming | orthogonal
        gain (float)       -- scaling factor for normal, xavier and orthogonal.
        gpu_ids (int list) -- which GPUs the network runs on: e.g., 0,1,2

    Return an initialized network.
    """
    if gpu_ids:
        assert(torch.cuda.is_available())
        net.to(gpu_ids[0])
        net = torch.nn.DataParallel(net, gpu_ids)  # multi-GPUs
    init_weights(net, init_type, init_gain=init_gain)
    return net


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