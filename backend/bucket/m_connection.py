from minio import Minio
from bucket.m_config import ACCESS_KEY, SECRET_KEY
from bucket.m_config import BUCKET_NAME, MINIO_API_HOST

def minio_connection():
    try:
        print(MINIO_API_HOST)
        print(ACCESS_KEY)
        print(SECRET_KEY)
        storage = Minio(
            MINIO_API_HOST,
            ACCESS_KEY,
            SECRET_KEY,     
            secure=True,
        )
    except Exception as e:
        print(e)
        return False
    else:
        print("storage bucket connected!")
        return storage

def minio_put_object(storage, filename, data):
    '''
    minio bucket에 지정 파일 업로드
    :param minio: 연결된 minio 객체(Minio client)
    :param filename: 파일 위치
    :param data: 데이터
    :return: 성공 시 True, 실패 시 False 반환
    '''
    try:
        storage.fput_object(BUCKET_NAME, filename, data, content_type="audio/wav")
        #storage.fput_object(BUCKET_NAME, filename, data)
        print(f"{filename} is successfully uploaded to bucket {BUCKET_NAME}.")
    except Exception as e:
        print(e)
        return False
    return True

# def minio_list_object(storage, age, gender):
#     '''
#     minio bucket에서 해당 성별과 나이에 맞는 이미지 리스트 가져오기
#     :param storage: 연결된 minio 객체(Minio client)
#     :param prefix: Object name starts with prefix.
#     :param age: 나이
#     :param gender: 성별
#     :return: 성공 시 list 반환, 실패 시 False 반환
#     '''
#     try:
#         prefix = "output_condition"
#         contents_list = storage.list_objects(bucket, prefix)['Contents']
#         file_list = [content['Key'] for content in contents_list]
#         condition_file_list = []
#         for file in file_list:
#             _, file_name = file.split('-')
#             idx = file_name.rindex('.')
#             if file_name[idx+1:] == 'jpg' and file_name[:idx] == f'{gender}_{age}':
#                 condition_file_list.append(file)
#     except Exception as e:
#         print(e)
#         return False
#     return condition_file_list