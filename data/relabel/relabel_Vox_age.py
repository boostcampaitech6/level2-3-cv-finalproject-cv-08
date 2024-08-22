import cv2
import argparse
import os
import csv
from collections import Counter

def predict_age(face):
    '''
    Function to predict age from a face image.
    
    Args:
        face: Image to predict age from.

    Returns:
        age: Predicted age group index.
    '''
    blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age = agePreds[0].argmax()
    return age

def count_and_print_age(folder_path):
    '''
    Function to count and print the most common age group from images in a folder.
    
    Args:
        folder_path: Path to the folder containing images.

    Returns:
        most_common_age: Index of the most common age group.
    '''
    age_list = []
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):
                image_path = os.path.join(folder_path, filename)
                frame = cv2.imread(image_path)
                if frame is not None:
                    age = predict_age(frame)
                    age_list.append(age)
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
        return None

    if age_list:
        most_common_age = Counter(age_list).most_common(1)[0][0]
        print("Most common age group index:", most_common_age)
        return most_common_age
    else:
        print("No images detected in the folder.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', required=True, help='Path to the folder containing images.')
    parser.add_argument('--csv_source', default="/home/carbox/Desktop/git/dataset/vox1/vox1_meta.csv")
    parser.add_argument('--output_csv', default="/home/carbox/Desktop/git/dataset/test/csv/test.csv")
    args = parser.parse_args()

    ageProto = "weights/age_deploy.prototxt"
    ageModel = "weights/age_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['0', '1', '2', '3', '4', '5', '6', '7']  # Index 형태로 출력하기 위해 수정

    ageNet = cv2.dnn.readNet(ageModel, ageProto)

    with open (args.output_csv, 'w',  newline='') as output_csv:
        csvwriter = csv.writer(output_csv, delimiter='\t')

        with open(args.csv_source, 'r') as file:
            for idx, line in enumerate(file):
                if idx == 0:
                    csvwriter.writerow(line.strip().split("\t") + ["age"])  # 헤더 부분에 age를 추가하여 리스트를 연결
                    continue
                line = line.strip()  # Remove leading/trailing whitespaces
                if line:
                    fields = line.split("\t")
                    image_name = fields[1]
                    age_index = count_and_print_age(os.path.join(args.folder, image_name))
                    if age_index is not None:
                        fields.append(str(age_index))  # age_index를 문자열로 변환하여 fields에 추가
                        csvwriter.writerow(fields)
