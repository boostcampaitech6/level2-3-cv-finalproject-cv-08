import segmentation_models_pytorch as smp

def get_model(model_str: str):
    """모델 클래스 변수 설정
    Args:
        model_str (str): 모델 클래스명
    Note:
        model_str 이 모델 클래스명으로 정의돼야함
        `model` 변수에 모델 클래스에 해당하는 인스턴스 할당
    """


    if model_str == 'Unet':
        return smp.Unet
    
    elif model_str == 'FPN':
        return smp.FPN

    elif model_str == 'DeepLabV3Plus':
        return smp.DeepLabV3Plus
    
    elif model_str == 'UnetPlusPlus':
        return smp.UnetPlusPlus

    elif model_str == 'PAN':
        return smp.PAN

    elif model_str == 'MAnet':
        return smp.MAnet

    elif model_str == 'PSPNet':
        return smp.PSPNet