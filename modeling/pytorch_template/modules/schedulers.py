from torch.optim import lr_scheduler

def get_scheduler(scheduler_str)-> object:
    
    scheduler = None
    
    if scheduler_str == 'CosineAnnealingLR':

        scheduler = lr_scheduler.CosineAnnealingLR

    elif scheduler_str == 'CosineAnnealingWarmRestarts':

        scheduler = lr_scheduler.CosineAnnealingWarmRestarts

    return scheduler