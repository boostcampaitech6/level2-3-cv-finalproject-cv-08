"""Preprocessor

"""

import numpy as np
import cv2

def get_image_scaler(scaler_str: str):
    
    if scaler_str == 'normalize':
        return normalize_image

    elif scaler_str == 'normalize_histogram':
        return normalize_histogram

    else:
        return None

def normalize_image(image: np.ndarray, max_pixel_value:int = 255)->np.ndarray:
    """Normalize image by pixel
    """
    normalized_image = image / max_pixel_value

    return normalized_image


def normalize_histogram(image: np.ndarray)-> np.ndarray:
    """Normalize histogram
    """
    lab_image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    lab_image[:, :, 0] = cv2.normalize(lab_image[:, :, 0], None, 0, 255 , cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    histogram_normalized_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2RGB)
    return histogram_normalized_image