import os
import re
import tarfile

def extract_tar_if_needed(root_folder: str):
    """ tar 파일을 추출하는 함수

    Args:
        root_folder (str): tar 파일이 들어있는 폴더 경로
    """
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.tar'):
                # .tar 파일과 같은 이름을 가진 폴더가 있는지 확인
                tar_path = os.path.join(root, file)
                folder_name = os.path.splitext(tar_path)[0]
                if not os.path.exists(folder_name):
                    # 동일한 이름의 폴더가 없으면 압축 해제
                    print(f"Extracting {tar_path}")
                    with tarfile.open(tar_path) as tar:
                        tar.extractall(path=root)
                    print(f"Extracted to {folder_name}")
                    # 압축 해제 후 dirs 리스트 업데이트
                    dirs.append(os.path.basename(folder_name))

                # 추출 후 삭제
                os.remove(os.path.join(root, file))
                print(f"Deleted {file} ")



def delete_files_except_extensions(root_folder: str, keep_extensions: list, pattern: str):
    """ 정제에 필요한 파일을 제외한 다른 파일들 삭제 

    Args:
        root_folder (str): 타겟 폴더
        keep_extensions (list): 유지할 확장자 wav, 혹은 끝나는 부분 (A_001.mp4) 확인
        pattern (str): 유지할 파일명 패턴
    """
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if not any(file.endswith(ext) for ext in keep_extensions):
                if re.search(pattern, file):
                    continue
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted {file}")

def main(root_folder: str, keep_extensions: list, pattern: str):
    # 먼저 .tar 파일이 있으면 압축을 해제
    extract_tar_if_needed(root_folder)
    # 압축 해제 후 (해당되는 경우), 지정된 확장자 외의 파일 삭제
    delete_files_except_extensions(root_folder, keep_extensions, pattern)
    print("End of processing")

if __name__ == '__main__':
    root_folder = '~/Desktop/GPU/009.립리딩(입모양) 음성인식 데이터/01.데이터/2.Validation/원천데이터'  # 탐색을 시작할 폴더 경로
    keep_extensions = ['A_001.mp4', '.wav']  # 유지하고 싶은 파일 확장자 목록
    pattern = r'.*_A_.*\.json'
    main(root_folder, keep_extensions, pattern)
