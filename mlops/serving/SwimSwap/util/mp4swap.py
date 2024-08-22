import cv2
import os
import torch
import numpy as np
from tqdm import tqdm
from util.reverse2original import reverse2wholeimage
from util.norm import SpecificNorm
from parsing_model.model import BiSeNet
import tempfile, requests
import imageio

def _totensor(array):
    tensor = torch.from_numpy(array)
    img = tensor.transpose(0, 1).transpose(0, 2).contiguous()
    return img.float().div(255)

def mp4_swap(video_path, id_vetor, swap_model, detect_model, save_path, temp_results_dir='./temp_results', crop_size=224, no_simswaplogo=False, use_mask=False):

        r = requests.get(video_path)
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(r.content)
            tmp_video_path = tmpfile.name
        
        video = cv2.VideoCapture(tmp_video_path)

        logoclass = None
        ret = True
        frame_index = 0

        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        video_WIDTH = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

        video_HEIGHT = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        
        fps = video.get(cv2.CAP_PROP_FPS)
        
        spNorm =SpecificNorm()
        if use_mask:
            n_classes = 19
            net = BiSeNet(n_classes=n_classes)
            net.cuda()
            save_pth = os.path.join('./parsing_model/checkpoint', '79999_iter.pth')
            net.load_state_dict(torch.load(save_pth))
            net.eval()
        else:
            net =None

        frames = []
        # while ret:
        for frame_index in tqdm(range(frame_count)): 
            ret, frame = video.read()
            if  ret:
                detect_results = detect_model.get(frame,crop_size)

                if detect_results is not None:
                    frame_align_crop_list = detect_results[0]
                    frame_mat_list = detect_results[1]
                    swap_result_list = []
                    frame_align_crop_tenor_list = []
                    for frame_align_crop in frame_align_crop_list:
                        frame_align_crop_tenor = _totensor(cv2.cvtColor(frame_align_crop,cv2.COLOR_BGR2RGB))[None,...].cuda()

                        swap_result = swap_model(None, frame_align_crop_tenor, id_vetor, None, True)[0]
                        swap_result_list.append(swap_result)
                        frame_align_crop_tenor_list.append(frame_align_crop_tenor)


                    img = reverse2wholeimage(frame_align_crop_tenor_list,swap_result_list, frame_mat_list, crop_size, frame, logoclass,\
                            os.path.join(temp_results_dir, 'frame_{:0>7d}.jpg'.format(frame_index)), no_simswaplogo, pasring_model=net, use_mask=use_mask, norm=spNorm)
                    
                    frame = frame.astype(np.uint8)
                    if not os.path.exists(temp_results_dir):
                        os.mkdir(temp_results_dir)
           
                    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                    frames.append(img)

                else:
                    if not os.path.exists(temp_results_dir):
                        os.mkdir(temp_results_dir)
                    frame = frame.astype(np.uint8)
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    frames.append(frame)
            else:
                break
        
        
        with imageio.get_writer(save_path, fps=fps) as video:
            for image in frames:
                video.append_data(image)
        return True
    # except:
    #     return False

