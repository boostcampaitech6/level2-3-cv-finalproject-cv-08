import time
from celery import Celery
from celery.utils.log import get_task_logger
import requests
from db_config import USERNAME, PASSWORD, HOST, DATABASE
import requests
from minio_connection import read_random_condition
from db_connection import Database
import json

logger = get_task_logger(__name__)

# Create a Celery instance named 'celery_app'
# celery = Celery('tasks',backend='db+mysql+pymysql://root:rootpwd@mysql-db:3306/MZ', broker='amqp://admin:mypass@rabbit:5672')
celery = Celery('tasks',backend=f'db+mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}', broker='amqp://admin:mypass@rabbit:5672')
db = Database()

@celery.task()
def run_mz(request_id, result_id, age, gender, file_url):
    logger.info('Got Request - Starting work')
    time.sleep(4)

    target_server_url = 'http://175.45.193.25:3002/makevideo'
    data = {'age' : age, 
            'gender' : gender, 
            'voice_url': file_url, 
            'request_id' : request_id, 
            'result_id' : result_id}
    logger.info(data)
    condition_image_url = None
    condition_video_url = None
    voice_image_url = None
    voice_video_url = None
    return_message = 200

    try: 
        # condition output 
        result, message = read_random_condition(age, gender)
        if result:
            condition_image_url = str(message['image'])
            condition_video_url = str(message['gif'])
            logger.info(condition_image_url)
            logger.info(condition_video_url)
        else:
            raise Exception('condition')
        
        # voice output
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36","Content-Type":"application/json"}
        response = requests.post(target_server_url,data=json.dumps(data),headers=headers)
        response_data = response.json()
        status_code = response_data.get("status_code")
        logger.info(status_code)

        if status_code == 200: # 성공 시 
            voice_image_url = str(response_data.get("voice_image_url"))
            voice_video_url = str(response_data.get("voice_video_url"))
            logger.info(voice_image_url)
            logger.info(voice_video_url)
        elif status_code == 404: # voice_image_url 만 받아온 경우 
            voice_image_url = str(response_data.get("voice_image_url"))
            logger.info(voice_image_url)
            error = response_data.get("error")
            raise Exception(error)
        else: # 실패 시 
            # Update status
            error = response_data.get("error")
            raise Exception(error)

    #except requests.RequestException as e:
    except Exception as e:
        logger.info(str(e))
        return_message = f'failed with exception: {str(e)}'
    
    # Update result 
    result_to_change = {
        'condition_image_url' : condition_image_url,
        'condition_gif_url' : condition_video_url,
        'voice_image_url' : voice_image_url,
        'voice_gif_url' : voice_video_url
    }
    logger.info(result_to_change)
    db.update_mz_result_image_gif(request_id, result_to_change)

    if None in [condition_image_url, condition_video_url, voice_image_url]:
        status_to_change = 'Failed'
    else:
        status_to_change = 'Success'
    logger.info(status_to_change)
    db.update_mz_request_status_ata(request_id, status_to_change)

    logger.info('Work Finished ')
    # return response.status_code
    return return_message

