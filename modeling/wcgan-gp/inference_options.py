import argparse
import torch.backends.cudnn as cudnn
import os
import torch

class InferenceOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False

    def initialize(self):
        # experiment specifics
        self.parser.add_argument('--gpu_ids', default='0', dest='gpu_ids')
        self.parser.add_argument('--use_gpu', default=True, dest="use_gpu")
        self.parser.add_argument('--checkpoint_path', default='./checkpoints', dest='checkpoint_path')
        self.parser.add_argument('--checkpoint_name', default="", dest="checkpoint_name")
        self.parser.add_argument('--checkpoint_fine_tune_name', default="fine_tune", dest="checkpoint_fine_tune_name")
        self.parser.add_argument('--output_path', default='./results', dest='dir_result')

        self.parser.add_argument('--nch_ker', type=int, default=64, dest='nch_ker')

        self.parser.add_argument('--fine_tune', type=bool, default=False, dest='fine_tune')

        self.parser.add_argument('--input_gender', default='m', choices=['m', 'man', 'male', 'f', 'female', 'woman'], dest='input_gender')
        self.parser.add_argument('--input_age', type=int, default=25, dest='input_age')

        self.initialized = True

    def parse(self, save=True):
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

        cudnn.benchmark = True
        cudnn.fastest = True
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        self.opt.isTrain = self.isTrain   # train or test

        str_ids = self.opt.gpu_ids.split(',')
        self.opt.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.opt.gpu_ids.append(id)
        
        # set gpu ids
        if len(self.opt.gpu_ids) > 0:
            torch.cuda.set_device(self.opt.gpu_ids[0])

        args = vars(self.opt)

        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')

        log_dir = os.path.join(args['dir_log'], args['scope'], args['name_data'])
        args_name = os.path.join(log_dir, 'args.txt')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(args_name, 'wt') as args_fid:
            args_fid.write('----' * 10 + '\n')
            args_fid.write('{0:^40}'.format('PARAMETER TABLES') + '\n')
            args_fid.write('----' * 10 + '\n')
            for k, v in sorted(args.items()):
                args_fid.write('{}'.format(str(k)) + ' : ' + ('{0:>%d}' % (35 - len(str(k)))).format(str(v)) + '\n')
            args_fid.write('----' * 10 + '\n')


        # save to the disk
        if self.opt.isTrain:
            expr_dir = os.path.join(self.opt.checkpoints_dir, self.opt.name)
            if not os.path.exists(expr_dir):
                os.makedirs(expr_dir)
            if save and not self.opt.continue_train:
                file_name = os.path.join(expr_dir, 'opt.txt')
                with open(file_name, 'wt') as opt_file:
                    opt_file.write('------------ Options -------------\n')
                    for k, v in sorted(args.items()):
                        opt_file.write('%s: %s\n' % (str(k), str(v)))
                    opt_file.write('-------------- End ----------------\n')
        return self.opt