import pymysql
from db_config import USERNAME, PASSWORD, HOST, DATABASE
from datetime import datetime
from pytz import timezone

class Database(): 
    def __init__(self):
        self.db = pymysql.connect(
            host=HOST[:-5],
            port=3306,
            user=USERNAME,
            passwd=PASSWORD,
            db=DATABASE,
            init_command='SET SESSION wait_timeout = 86400'
        )
        self.cursor = self.db.cursor()

    def update_mz_request_status_ata(self, request_id, status_to_change):
        self.cursor.execute('UPDATE mz_request \
                SET status = %s, \
                ata = %s \
                WHERE id = %s', (status_to_change, str(datetime.now(timezone('Asia/Seoul'))), request_id))
        self.db.commit()
        

    def update_mz_result_image_gif(self,mz_request_id, task_result):
        condition_image_url = task_result['condition_image_url']
        condition_gif_url = task_result['condition_gif_url']
        voice_image_url = task_result['voice_image_url']
        voice_gif_url = task_result['voice_gif_url']

        self.cursor.execute('UPDATE mz_result \
                SET condition_image_url = %s, \
                condition_gif_url = %s, \
                voice_image_url = %s, \
                voice_gif_url = %s \
                WHERE mz_request_id = %s', (condition_image_url, condition_gif_url, voice_image_url, voice_gif_url, mz_request_id))
        self.db.commit()