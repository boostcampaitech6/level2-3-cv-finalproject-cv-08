import os 
import json
from pydub import AudioSegment

def process_wav_and_json(wav_file: str, json_file: str, wav_file_name: str, save_folder: str):
    """ wav 파일을 받아 json 에서 필요한 부분을 잘라내 형태에 맞게 저장할 코드

    Args:
        wav_file (str): json 파일과 매칭되는 wav_file 경로
        json_file (str): wav_file croping에 사용될 json_file 경로
        wav_file_name (str): folder명 지정에 사용할 wav_file 자체 이름
        save_folder (str): 정제된 파일을 저장할 경로
    """
    count = 1
    audio = AudioSegment.from_wav(wav_file)

    # 저장할 폴더 생성
    wav_file_folder = wav_file_name.split("_")[:-2]
    wav_file_folder = "_".join(wav_file_folder)
    wav_file_folder = os.path.join(save_folder,'data', wav_file_folder,'audio')
    os.makedirs(wav_file_folder, exist_ok=True)

    # json 파일 열기
    with open(json_file, 'r') as f:
        data = json.load(f)
        data= data[0]

    # 각 시간대별로 돌아가며 동영상 croping
    for sentence_info in data['Sentence_info']:
        start_time = round(int(sentence_info['start_time']), 3)
        end_time = round(int(sentence_info['end_time']), 3)
        time = end_time - start_time
        if time <3 or time  > 10 :
            continue

        start_time_ms = start_time * 1000
        end_time_ms = end_time * 1000


        segment = audio[start_time_ms:end_time_ms]
        output_wav_file = f"{wav_file_name.split('_')[-1]}_{count:03d}.wav"

        output_wav_path = os.path.join(wav_file_folder, output_wav_file)

        segment.export(output_wav_path, format='wav')
        count += 1

        print(f"Saved {output_wav_path}")
        

def find_matching_json(file_name: str, json_folder: str) ->str :
    """wav 파일과 파일명이 똑같은 json 파일을 찾아 경로 반환, 
    만약 없다면 None 반환

    Args:
        file_name (str): wav 파일 이름 가져오기
        json_folder (str): json이 저장된 위치 확인

    Returns:
        str: wav 파일에 해당하는 json 파일 반환
    """

    for root, dirs, files in os.walk(json_folder):
        for file in files:
            if file.split('.')[0] == file_name:
                json_file = os.path.join(root, file)
                return json_file
    return None
            
def find_wav(wav_folder: str, json_folder: str, save_folder: str):
    """ 처음 정제할 wav 파일 찾기
        이후 json 파일을 찾아 wav를 정제한다.

    Args:
        wav_folder (str): wav 파일들이 저장된 폴더 위치 
        json_folder (str): json 파일들이 저장된 폴더 위치
        save_folder (str): croping 된 파일들을 저장할 위치
    """

    for root,_,files in os.walk(wav_folder):
        for file in files:
            if file.endswith('.wav'):
                wav_file = os.path.join(root, file)
                wav_file_name = wav_file.split('/')[-1].split('.')[0]
                json_file = find_matching_json(wav_file_name, json_folder)

                if json_file:
                    process_wav_and_json(wav_file, json_file, wav_file_name, save_folder)
                    os.remove(wav_file)


def main(wav_folder: str, json_folder: str, save_folder: str):
    find_wav(wav_folder, json_folder, save_folder)
    print('End of processing')




if __name__ == '__main__':
    # WAV 파일이 들어있는 폴더 경로
    wav_folder = '/home/carbox/Desktop/data/009.립리딩(입모양) 음성인식 데이터/01.데이터/2.Validation/원천데이터'   
    # JSON 파일이 들어있는 폴더 경로 
    json_folder = '/home/carbox/Desktop/data/009.립리딩(입모양) 음성인식 데이터/01.데이터/2.Validation/라벨링데이터'  
    # 원천데이터를 저장할 폴더 경로
    save_folder = '/home/carbox' 

    main(wav_folder, json_folder, save_folder)
