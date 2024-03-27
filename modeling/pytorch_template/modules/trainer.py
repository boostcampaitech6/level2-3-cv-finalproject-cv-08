"""Trainer

"""
from tqdm import tqdm
import torch

class Trainer():
    """Trainer
    
    Attribues:
        model(object): 모델 객체
        optimizer (object): optimizer 객체
        scheduler (object): scheduler 객체
        loss_func (object): loss 함수 객체
        metric_funcs (dict): metric 함수 dict
        device (str):  'cuda' | 'cpu'
        logger (object): logger 객체
        loss (float): loss
        scores (dict): metric 별 score
    """

    def __init__(self,
                model,
                optimizer,
                scheduler,
                loss_func,
                metric_funcs,
                device,
                logger=None):        
        
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.loss_func = loss_func
        self.metric_funcs = metric_funcs
        self.device = device
        self.logger = logger

        self.loss = 0
        self.scores = {metric_name: 0 for metric_name, _ in self.metric_funcs.items()}

    def train(self, dataloader, epoch_index=0):
        
        self.model.train()
        for batch_id, (x, y, filename) in enumerate(tqdm(dataloader)):

            # Load data to gpu
            x = x.to(self.device, dtype=torch.float)
            y = y.to(self.device, dtype=torch.long)
            
            # Inference
            y_pred = self.model(x)
            
            # Loss
            loss = self.loss_func(y_pred, y)

            # Update
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            # Metric
            for metric_name, metric_func in self.metric_funcs.items():
                self.scores[metric_name] += metric_func(y_pred.argmax(1), y).item() / len(dataloader)
            # History
            self.loss += loss.item()
            self.logger.debug(f"TRAINER | train epoch: {epoch_index}, batch: {batch_id}/{len(dataloader)-1}, loss: {loss.item()}")
            self.logger.debug(f"TRAINER | {filename}")

        self.scheduler.step()
        self.loss = self.loss / len(dataloader)

    def validate(self, dataloader, epoch_index=0):
    
        self.model.eval()

        with torch.no_grad():

            for batch_id, (x, y, filename) in enumerate(tqdm(dataloader)):

                # Load data to gpu
                x = x.to(self.device, dtype=torch.float)
                y = y.to(self.device, dtype=torch.long)
                
                # Inference
                y_pred = self.model(x)

                # Loss
                loss = self.loss_func(y_pred, y)

                # Metric
                for metric_name, metric_func in self.metric_funcs.items():
                    self.scores[metric_name] += metric_func(y_pred.argmax(1), y).item() / len(dataloader)

                # History
                self.loss += loss.item()

        self.loss = self.loss / len(dataloader)
        self.logger.debug(f"TRAINER | val/test epoch: {epoch_index}, batch: {batch_id}/{len(dataloader)-1}, loss: {loss.item()}")
        self.logger.debug(f"TRAINER | {filename}")
        
    def clear_history(self):

        torch.cuda.empty_cache()
        self.loss = 0
        self.scores = {metric_name: 0 for metric_name, _ in self.metric_funcs.items()}
        self.logger.debug(f"TRAINER | Clear history, loss: {self.loss}, score: {self.scores}")