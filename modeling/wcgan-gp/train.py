import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import lr_scheduler
from torchvision import transforms
from statistics import mean
from datetime import datetime

from model import ConditionLinearFinetuneGAN, Discriminator, init_net, set_requires_grad
from dataset import HQVoxceleb, CelebADataset
from utils import GradientPaneltyLoss, model_load, model_save, custom_collate_fn

from train_options import TrainOptions

class Train:
    def __init__(self, args):
        self.train_continue = args.train_continue

        self.checkpoint_path = args.checkpoint_path
        self.checkpoint_name = args.checkpoint_name
        self.checkpoint_fine_tune_name = args.checkpoint_fine_tune_name

        self.dataset_path = args.dataset_path
        self.dataset_name = args.dataset_name
        self.dataset_fine_tune_name = args.dataset_fine_tune_name

        self.output_path = args.output_path

        self.num_epoch = args.num_epoch
        self.num_epochs_decay = args.num_epochs_decay
        self.num_freq_save = args.num_freq_save
        
        self.batch_size = args.batch_size

        self.lr_G = args.lr_G
        self.lr_D = args.lr_D
        self.lr_G_weight_decay = args.lr_G_weight_decay
        self.lr_D_weight_decay = args.lr_D_weight_decay
        self.lr_policy = args.lr_policy

        self.nch_ker = args.nch_ker

        self.fine_tune = args.fine_tune
        self.fine_tune_num_epoch = args.fine_tune_num_epoch
        self.fine_tune_num_freq_save = args.fine_tune_num_freq_save

        self.use_gpu = args.use_gpu
        self.gpu_ids = args.gpu_ids
        if self.use_gpu and torch.cuda.is_available():
            self.device = torch.device("cuda:%d" % self.gpu_ids[0])
            torch.cuda.set_device(self.gpu_ids[0])
        else:
            self.device = torch.device("cpu")

        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            # transforms.RandomHorizontalFlip(p=0.5), 
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
        ])
        

    def train(self):
        device = self.device
        noise = 100

        dataset = CelebADataset(root_dir=self.dataset_path, data_folder=self.dataset_name, transform=self.transform)
        loader_train = DataLoader(dataset, batch_size=self.batch_size, shuffle=True, num_workers=0, drop_last=True)

        num_train = len(dataset)

        num_batch_train = int((num_train / self.batch_size) + ((num_train % self.batch_size) != 0))

        netG = ConditionLinearFinetuneGAN(nch_in=noise, nch_ker=self.nch_ker)
        netD = Discriminator(nch_ker=self.nch_ker)

        init_net(netG, init_type='normal', init_gain=0.02, gpu_ids=self.gpu_ids)
        init_net(netD, init_type='normal', init_gain=0.02, gpu_ids=self.gpu_ids)

        ## setup loss & optimization
        fn_GP = GradientPaneltyLoss().to(device)

        paramsG = netG.parameters()
        paramsD = netD.parameters()

        optimG = torch.optim.Adam(paramsG, lr=self.lr_G, weight_decay=self.lr_G_weight_decay, betas=(0.999, 0.999))
        optimD = torch.optim.Adam(paramsD, lr=self.lr_D, weight_decay=self.lr_D_weight_decay, betas=(0.999, 0.999))

        # schedG = get_scheduler(optimG, self.opts)
        # schedD = get_scheduler(optimD, self.opts)

        # schedG = torch.optim.lr_scheduler.ExponentialLR(optimG, gamma=0.9)
        # schedD = torch.optim.lr_scheduler.ExponentialLR(optimD, gamma=0.9)

        ## load from checkpoints
        st_epoch = 0

        if self.train_continue == 'on':
            ckpt = os.path.join(self.checkpoint_path, self.checkpoint_name)
            netG, netD, optimG, optimD, st_epoch = model_load(ckpt, netG, netD, optimG, optimD, mode=self.mode)

        for epoch in range(st_epoch + 1, self.num_epoch + 1):
            ## training phase
            netG.train()
            netD.train()

            loss_G_train = []
            loss_D_real_train = []
            loss_D_fake_train = []

            for i, data in enumerate(loader_train):
                def should(freq):
                    return freq > 0 and (i % freq == 0 or i == num_batch_train)

                images = data.to(device)
                input = torch.randn(self.batch_size, noise).to(device)
                output = netG(input)

                # backward netD
                set_requires_grad(netD, True)
                optimD.zero_grad()

                pred_real = netD(images)
                pred_fake = netD(output.detach())

                alpha = torch.rand(self.batch_size, 1, 1, 1).to(self.device)
                output_ = (alpha * images + (1 - alpha) * output.detach()).requires_grad_(True)
                src_out_ = netD(output_)

                # WGAN Loss
                loss_D_real = torch.mean(pred_real)
                loss_D_fake = -torch.mean(pred_fake)

                # Gradient penalty Loss
                loss_D_gp = fn_GP(src_out_, output_)
                loss_D = 0.5 * (loss_D_real + loss_D_fake) + loss_D_gp
                loss_D.backward(retain_graph=True)
                optimD.step()


                set_requires_grad(netD, False)
                # backward netG
                optimG.zero_grad()
                
                pred_fake = netD(output)

                loss_G = torch.mean(pred_fake)
                loss_G.backward()
                optimG.step()

                # get losses
                loss_G_train += [loss_G.item()]
                loss_D_real_train += [loss_D_real.item()]
                loss_D_fake_train += [loss_D_fake.item()]

                print('TRAIN: EPOCH %d: BATCH %04d/%04d: '
                      'GEN GAN: %.4f DISC FAKE: %.4f DISC REAL: %.4f' %
                      (epoch, i, num_batch_train,
                       mean(loss_G_train), mean(loss_D_fake_train), mean(loss_D_real_train)))


            ## save
            if (epoch % self.num_freq_save) == 0:
                self.save(dir_chck, netG, netD, optimG, optimD, epoch, self.start_time)

        if self.fine_tune:
            voxceleb_path = os.path.join(self.dataset_path, self.dataset_fine_tune_name)
            dataset = HQVoxceleb(root_path=voxceleb_path, transform=self.transform)
            loader_train = DataLoader(dataset, batch_size=self.batch_size, shuffle=True, num_workers=8, drop_last=True, collate_fn=custom_collate_fn)

            init_net(netG, init_type='normal', init_gain=0.02, gpu_ids=self.gpu_ids)
            init_net(netD, init_type='normal', init_gain=0.02, gpu_ids=self.gpu_ids)

            ## setup loss & optimization
            fn_GP = GradientPaneltyLoss().to(device)

            paramsG = netG.parameters()
            paramsD = netD.parameters()

            optimG = torch.optim.Adam(paramsG, lr=1e-5, weight_decay=self.lr_G_weight_decay, betas=(0.999, 0.999))
            optimD = torch.optim.Adam(paramsD, lr=1e-5, weight_decay=self.lr_D_weight_decay, betas=(0.999, 0.999))

            new_sequence = nn.Sequential(
                nn.Linear(in_features=(noise+self.nch_ker//4+self.nch_ker//4), out_features=2*self.nch_ker),
                nn.LeakyReLU(0.2),
                nn.Dropout(0.1)
            )
            netG.fc1 = new_sequence
            netG.set_fine_tune(True)
            netG = netG.to(device)

            dir_chck = os.path.join(dir_chck, self.checkpoint_fine_tune_name)
            for epoch in range(self.fine_tune_num_epoch + 1):
                ## training phase
                netG.train()
                netD.train()

                loss_G_train = []
                loss_D_real_train = []
                loss_D_fake_train = []

                for i, data in enumerate(loader_train):
                    def should(freq):
                        return freq > 0 and (i % freq == 0 or i == num_batch_train)

                    images, gender_labels, age_labels = data
                    images = images.to(device)

                    gender_labels = gender_labels.unsqueeze(1)
                    gender_conditions = torch.zeros(self.batch_size, 2)
                    gender_conditions = gender_conditions.scatter_(1, gender_labels, 1).to(device)

                    age_labels = age_labels.unsqueeze(1)
                    age_conditions = torch.zeros(self.batch_size, 8)
                    age_conditions = age_conditions.scatter_(1, age_labels, 1).to(device)
                    
                    input = torch.randn(self.batch_size, noise).to(device)
                    input_G = (input, gender_conditions, age_conditions)

                    output = netG(input_G)
                    
                    # backward netD
                    set_requires_grad(netD, True)
                    optimD.zero_grad()

                    pred_real = netD(images)
                    pred_fake = netD(output.detach())

                    alpha = torch.rand(self.atch_size, 1, 1, 1).to(self.device)
                    output_ = (alpha * images + (1 - alpha) * output.detach()).requires_grad_(True)
                    src_out_ = netD(output_)

                    # WGAN Loss
                    loss_D_real = torch.mean(pred_real)
                    loss_D_fake = -torch.mean(pred_fake)

                    # Gradient penalty Loss
                    loss_D_gp = fn_GP(src_out_, output_)

                    loss_D = 0.5 * (loss_D_real + loss_D_fake) + loss_D_gp

                    loss_D.backward(retain_graph=True)
                    optimD.step()


                    set_requires_grad(netD, False)
                    # backward netG
                    optimG.zero_grad()
                    
                    loss_G = torch.mean(pred_fake)
                    loss_G.backward()
                    optimG.step()
                    
                    # get losses
                    loss_G_train += [loss_G.item()]
                    loss_D_real_train += [loss_D_real.item()]
                    loss_D_fake_train += [loss_D_fake.item()]

                    print('TRAIN: EPOCH %d: BATCH %04d/%04d: '
                        'GEN GAN: %.4f DISC FAKE: %.4f DISC REAL: %.4f' %
                        (epoch, i, num_batch_train,
                        mean(loss_G_train), mean(loss_D_fake_train), mean(loss_D_real_train)))
                
                ## save
                if (epoch % self.fine_tune_num_freq_save) == 0:
                    model_save(dir_chck, netG, netD, optimG, optimD, epoch, start_time=self.start_time)

    def fine_tuning(self):
        device = self.device
        noise = 100
        self.fine_tune = True

        dataset = HQVoxceleb(root_dir=self.dataset_path, data_folder=self.dataset_fine_tune_name, transform=self.transform)
        loader_train = DataLoader(dataset, batch_size=self.batch_size, shuffle=True, num_workers=0, drop_last=True)

        num_train = len(dataset)

        num_batch_train = int((num_train / self.batch_size) + ((num_train % self.batch_size) != 0))

        netG = ConditionLinearFinetuneGAN(nch_in=noise, nch_ker=self.nch_ker)
        netD = Discriminator(nch_ker=self.nch_ker)


        ## setup loss & optimization
        fn_GP = GradientPaneltyLoss().to(device)
        
        new_sequence = nn.Sequential(
            nn.Linear(in_features=(noise+self.nch_ker//4+self.nch_ker//4), out_features=2*self.nch_ker),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1)
        )

        netG.fc1 = new_sequence
        ckpt = os.path.join(self.checkpoint_path, self.checkpoint_fine_tune_name)
        netG, netD, optimG, optimD, st_epoch = model_load(ckpt, netG, netD, optimG, optimD, mode=self.mode)

        netG.set_fine_tune(True)

        netG = netG.to(device)

        paramsG = netG.parameters()
        paramsD = netD.parameters()

        optimG = torch.optim.Adam(paramsG, lr=self.lr_G, weight_decay=self.lr_G_weight_decay, betas=(0.999, 0.999))
        optimD = torch.optim.Adam(paramsD, lr=self.lr_D, weight_decay=self.lr_D_weight_decay, betas=(0.999, 0.999))

        for epoch in range(self.fine_tune_num_epoch + 1):
            ## training phase
            netG.train()
            netD.train()

            loss_G_train = []
            loss_D_real_train = []
            loss_D_fake_train = []

            for i, data in enumerate(loader_train):
                def should(freq):
                    return freq > 0 and (i % freq == 0 or i == num_batch_train)

                images, gender_labels, age_labels = data
                images = images.to(device)

                gender_labels = gender_labels.unsqueeze(1)
                gender_conditions = torch.zeros(self.batch_size, 2)
                gender_conditions = gender_conditions.scatter_(1, gender_labels, 1).to(device)

                age_labels = age_labels.unsqueeze(1)
                age_conditions = torch.zeros(self.batch_size, 8)
                age_conditions = age_conditions.scatter_(1, age_labels, 1).to(device)
                
                input = torch.randn(self.batch_size, noise).to(device)
                input_G = (input, gender_conditions, age_conditions)

                output = netG(input_G)
                
                # backward netD
                set_requires_grad(netD, True)
                optimD.zero_grad()

                pred_real = netD(images)
                pred_fake = netD(output.detach())

                alpha = torch.rand(self.atch_size, 1, 1, 1).to(self.device)
                output_ = (alpha * images + (1 - alpha) * output.detach()).requires_grad_(True)
                src_out_ = netD(output_)

                # WGAN Loss
                loss_D_real = torch.mean(pred_real)
                loss_D_fake = -torch.mean(pred_fake)

                # Gradient penalty Loss
                loss_D_gp = fn_GP(src_out_, output_)

                loss_D = 0.5 * (loss_D_real + loss_D_fake) + loss_D_gp

                loss_D.backward(retain_graph=True)
                optimD.step()

                set_requires_grad(netD, False)
                # backward netG
                optimG.zero_grad()
                
                # pred_fake = netD(output, condition)
                pred_fake = netD(output)

                loss_G = torch.mean(pred_fake)
                loss_G.backward()
                optimG.step()
                
                # get losses
                loss_G_train += [loss_G.item()]
                loss_D_real_train += [loss_D_real.item()]
                loss_D_fake_train += [loss_D_fake.item()]

                print('TRAIN: EPOCH %d: BATCH %04d/%04d: '
                    'GEN GAN: %.4f DISC FAKE: %.4f DISC REAL: %.4f' %
                    (epoch, i, num_batch_train,
                    mean(loss_G_train), mean(loss_D_fake_train), mean(loss_D_real_train)))
            
            ## save
            if (epoch % self.fine_tune_num_freq_save) == 0:
                model_save(ckpt, netG, netD, optimG, optimD, epoch, start_time=self.start_time)
                
if __name__ == '__main__':
    opt = TrainOptions().parse()

    TRAINER = Train(opt)
    
    if opt.mode == 'train':
        TRAINER.train()
    elif opt.mode == 'finetune':
        TRAINER.fine_tuning()