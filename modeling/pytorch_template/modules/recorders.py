"""PerformanceRecorder

"""
from matplotlib import pyplot as plt
import pandas as pd
import logging
import torch
import csv
import os
import wandb
import mlflow


class Recorder():

    def __init__(self,
                 record_dir: str,
                 model: 'model',
                 optimizer: 'optimizer',
                 scheduler: 'scheduler',
                 amp: 'amp'=None,
                 logger: logging.RootLogger=None):
        """Recorder 초기화
            
        Args:

        Note:
        """
        
        self.record_dir = record_dir
        self.plot_dir = os.path.join(record_dir, 'plots')
        self.record_filepath = os.path.join(self.record_dir, 'record.csv')
        self.weight_path = os.path.join(record_dir, 'model.pt')

        self.logger = logger
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.amp = amp
        os.makedirs(self.plot_dir, exist_ok=True)

    def set_model(self, model: 'model'):
        self.model = model

    def set_logger(self, logger: logging.RootLogger):
        self.logger = logger
    
    def wandb_mlflow_log(self, model, log_dict,sample_image=None):
        log_dict['lr'] = log_dict['lr'][0]
        log_dict = {k: int(v) for k, v in log_dict.items()}
        mlflow.log_metrics(log_dict)
        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path = "sf2f_pytorch",
        )
        if sample_image:
            log_dict['sample'] = [wandb.Image(sample_image, caption=f"Sample")]
        wandb.log(log_dict)


    def add_row(self, row_dict: dict):
        """Epoch 단위 성능 적재

        Args:
            row (list): 

        """

        fieldnames = list(row_dict.keys())

        with open(self.record_filepath, newline='', mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if f.tell() == 0:
                writer.writeheader()

            writer.writerow(row_dict)
        self.logger.debug(f"RECORDER | record saved: {self.record_filepath}")

    def save_weight(self, epoch: int)-> None:
        """Weight 저장
            amp 추가
        Args:
            loss (float): validation loss
            model (`model`): model
        
        """
        check_point = {
            'epoch': epoch + 1,
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'scheduler': self.scheduler.state_dict() if self.scheduler else None,
            'amp': self.amp.state_dict() if self.amp else None}

        torch.save(check_point, self.weight_path)
        self.logger.debug(f"RECORDER | epoch {epoch}, checkpoint saved: {self.weight_path}")

    
    def save_plot(self, plots: list):

        record_df = pd.read_csv(self.record_filepath)
        current_epoch = record_df['epoch_id'].max()
        epoch_range = list(range(0, current_epoch+1))
        color_list = ['red', 'blue']

        for plot_name in plots:
            columns = [f'train_{plot_name}', f'val_{plot_name}']

            fig = plt.figure(figsize=(20, 8))
            
            for id_, column in enumerate(columns):
                values = record_df[column].tolist()
                plt.plot(epoch_range, values, marker='.', c=color_list[id_], label=column)
             
            plt.title(plot_name, fontsize=15)
            plt.legend(loc='upper right')
            plt.grid()
            plt.xlabel('epoch')
            plt.ylabel(plot_name)
            plt.xticks(epoch_range, [str(i) for i in epoch_range])
            plt.close(fig)
            fig.savefig(os.path.join(self.plot_dir, plot_name +'.png'))

            self.logger.debug(f"RECORDER | plot saved: {os.path.join(self.plot_dir, plot_name +'.png')}")


