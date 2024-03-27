"""Early stopping 클래스 정의
"""
import numpy as np
import logging

class EarlyStopper():
    """Early stoppiing 여부 판단
    
    Attributes:
        patience (int): target가 줄어들지 않아도 학습할 epoch 수
        patience_counter (int): target 가 줄어들지 않을 때 마다 1씩 증가
        best_target (float): 최소 target
        stop (bool): True 일 때 학습 중단

    """

    def __init__(self, patience: int, mode:str='max', logger:logging.RootLogger=None)-> None:
        """ 초기화
        
        Args:
            patience (int): target가 줄어들지 않아도 학습할 epoch 수
            mode (str): max tracks higher value, min tracks lower value

        """
        self.patience = patience
        self.mode = mode
        self.logger = logger

        # Initiate
        self.patience_counter = 0
        self.stop = False
        self.best_target = np.inf
        self.logger.info(f"ES | Initiated, mode: {self.mode}, best score: {self.best_target}, patience: {self.patience}")
        
    def check_early_stopping(self, target: float)-> None:
        target = -target if self.mode == 'max' else target

        if target > self.best_target:
            self.patience_counter += 1
            self.logger.info(f"ES | {self.patience_counter}/{self.patience}, best:{abs(self.best_target)}, now:{abs(target)}")
            
            if self.patience_counter == self.patience:
                self.logger.debug(f"ES | Stop {self.patience_counter}/{self.patience}")
                self.stop = True 

        elif target <= self.best_target:
            self.patience_counter = 0
            self.best_target = target
            self.logger.info(f"ES | {self.patience_counter}/{self.patience}, best:{abs(self.best_target)}, now:{abs(target)}")
            self.logger.info(f"ES | Set patience counter as {self.patience_counter}")