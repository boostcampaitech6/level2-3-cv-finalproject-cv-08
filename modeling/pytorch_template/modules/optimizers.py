import torch.optim as optim

def get_optimizer(optimizer_str: str)-> 'optimizer':

    if optimizer_str == 'SGD':

        optimizer = optim.SGD

    elif optimizer_str == 'Adam':

        optimizer = optim.Adam
    
    elif optimizer_str == 'AdamW':
        
        optimizer = optim.AdamW
        
    return optimizer
