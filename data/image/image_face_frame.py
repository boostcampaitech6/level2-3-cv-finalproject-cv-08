import cv2
import os
from rembg import remove

def process_video(video_path: str, save_folder: str):
    """Video 에서 사람의 얼굴이 정면이고, 눈을 뜨고 잇을 때 캡쳐 및 배경 제거

    Args:
        video_path (str): 타겟 비디오 파일경로
        save_folder (str): 이미지를 저장할 위치 
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            # 얼굴 영역을 30% 확장
            expansion_rate = 0.3
            new_width = int(w * (1 + expansion_rate))
            new_height = int(h * (1 + expansion_rate))
            new_x = x - int(w * expansion_rate / 2)
            new_y = y - int(h * expansion_rate / 2)

            # 확장된 영역이 프레임을 벗어나지 않도록 조정
            new_x = max(0, new_x)
            new_y = max(0, new_y)
            new_width = min(new_width, frame.shape[1] - new_x)
            new_height = min(new_height, frame.shape[0] - new_y)

            roi_color = frame[new_y:new_y+new_height, new_x:new_x+new_width]
            eyes = eye_cascade.detectMultiScale(cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY))
            if len(eyes) >= 2:  # 두 눈이 검출되면
                face_img = cv2.resize(roi_color, (256, 256))
                face_img = remove(face_img, bgcolor=(255, 255, 255, 255))

                video_name = "_".join(os.path.splitext(os.path.basename(video_path))[0].split("_")[:-2])
                origin_file_folder = os.path.join(save_folder,'data', video_name)
                os.makedirs(origin_file_folder, exist_ok=True)

                cv2.imwrite(f'{os.path.join(origin_file_folder, video_name)}.png', face_img)
                cap.release()
                return 
            
    print(os.path.basename(video_path))
    cap.release()


def main(video_folder: str, save_folder: str):
    """ 비디오 폴더 경로에서 .mp4 파일 선택,
        정제 이후 파일 제거

    Args:
        video_folder (str): 탐색할 비디오가 있는 경로
        save_folder (str): 이미지 저장을 위한 파일
    """
    for root,_,files in os.walk(video_folder):
        for file in files:
            if file.endswith('.mp4'):
                video_file = os.path.join(root, file)
                process_video(video_file, save_folder)
                os.remove(os.path.join(root,file))

    
if __name__ == '__main__':
    video_folder = '/home/carbox/Desktop/data/009.립리딩(입모양) 음성인식 데이터/01.데이터/2.Validation/원천데이터'
    save_folder = "/home/carbox"
    main(video_folder, save_folder)


