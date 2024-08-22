from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from PIL import Image
import torch
import numpy as np

'''
This script performs image segmentation using the CLIPSeg model based on provided text prompts. It loads an image, processes it with text prompts, and generates a segmented image based on the identified objects.

Inputs:
- image: The image to be segmented.
- positive_prompts: Text prompts describing the objects to be identified, separated by commas.
- negative_prompts: Text prompts describing the objects to be ignored, separated by commas.
- threshold: Threshold value for segmentation, between 0 and 1.

Outputs:
- output_image: Segmented image with identified objects highlighted.
- final_mask: Final mask representing the segmented areas.

'''

# load CLIPSeg model & processor
processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

# image path & load
image_path = "/root/project/voice2face-data/file/face_detected_256x256.png"
image = Image.open(image_path)

def process_image(image, positive_prompts, negative_prompts, threshold):
    '''
    This function performs image segmentation based on provided text prompts and threshold.

    Args:
    - image: PIL image object.
    - positive_prompts: Text prompts describing the objects to be identified, separated by commas.
    - negative_prompts: Text prompts describing the objects to be ignored, separated by commas.
    - threshold: Threshold value for segmentation, between 0 and 1.

    Returns:
    - output_image: Segmented image with identified objects highlighted.
    - final_mask: Final mask representing the segmented areas.
    '''

    # image segmentation with img & prompt
    def get_masks(prompts, img, threshold):
        prompts = prompts.split(",")
        masks = []
        for prompt in prompts:
            inputs = processor(
                text=prompt.strip(), images=image, padding="max_length", return_tensors="pt"
            )
            with torch.no_grad():
                outputs = model(**inputs)
                preds = outputs.logits

            pred = torch.sigmoid(preds)
            mat = pred.cpu().numpy()
            mask = Image.fromarray(np.uint8(mat * 255), "L")
            mask = mask.convert("RGB")
            mask = mask.resize(image.size)
            mask = np.array(mask)[:, :, 0]

            # normalize the mask
            mask_min = mask.min()
            mask_max = mask.max()
            mask = (mask - mask_min) / (mask_max - mask_min)
            mask = mask > threshold
            masks.append(mask)
        return masks

    # Make mask's Positive prompts, Negative prompts
    positive_masks = get_masks(positive_prompts, image, threshold)
    negative_masks = get_masks(negative_prompts, image, threshold)

    # Make Result mask combined masks
    pos_mask = np.any(np.stack(positive_masks), axis=0)
    neg_mask = np.any(np.stack(negative_masks), axis=0)
    final_mask = pos_mask & ~neg_mask

    # Result image 
    final_mask = Image.fromarray(final_mask.astype(np.uint8) * 255, "L")
    output_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    output_image.paste(image, mask=final_mask)
    return output_image, final_mask

# base prompt
positive_prompts = "face"
negative_prompts = "background"
threshold = 0.5

# 텍스트 프롬프트 및 임계값 설정
# positive_prompts = input("what you want to identify (comma separated): ")
# negative_prompts = input("what you want to ignore (comma separated): ")
# threshold = float(input("enter the threshold value (between 0 and 1): "))

# process of segmentation
output_image, final_mask = process_image(image, positive_prompts, negative_prompts, threshold)

# save result img
output_image_path = "/root/project/voice2face-data/file/segmented_image.png"
output_image.save(output_image_path)

# print success message
print("Segmented image saved successfully at:", output_image_path)
