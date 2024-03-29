
# Voice2Face-Backend
<img  src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img  src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img  src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img  src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"> <img  src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img  src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white"> <img  src="https://img.shields.io/badge/NCP-03C75A?style=for-the-badge&logo=Naver&logoColor=white"> <img  src="https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=RabbitMQ&logoColor=white"> <img  src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=Celery&logoColor=white"> <img  src="https://img.shields.io/badge/minio-C72E49?style=for-the-badge&logo=minio&logoColor=white"> <img  src="https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"> <img  src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=Linux&logoColor=white">

## Project Structure
```
backend  
 ┣ apis_v1  
 ┃ ┣ MzRequest.py  
 ┃ ┗ User.py  
 ┣ bucket  
 ┃ ┣ m_config.py  
 ┃ ┗ m_connection.py  
 ┣ db  
 ┃ ┣ db_config.py  
 ┃ ┣ db_connection.py  
 ┃ ┣ enum_classes.py  
 ┃ ┗ schema.py  
 ┣ module  
 ┃ ┣ crud_module.py  
 ┃ ┣ db_module.py  
 ┃ ┣ file_module.py  
 ┃ ┣ module_config.py  
 ┃ ┣ token.py  
 ┃ ┗ user_module.py  
 ┣ simple_worker  
 ┃ ┣ Dockerfile  
 ┃ ┣ db_config.py  
 ┃ ┣ db_connection.py  
 ┃ ┣ minio_config.py  
 ┃ ┣ minio_connection.py  
 ┃ ┣ requirements.txt  
 ┃ ┗ tasks.py  
 ┣ static  
 ┃ ┗ status_code.py  
 ┣ .gitignore  
 ┣ Dockerfile  
 ┣ app.py  
 ┣ docker-compose.yml  
 ┗ requirements.txt
```

- `apis_v1` : voice2face에 필요한 api를 정리해둔 폴더
	- `User.py` : /users, /auth로 들어오는 요청을 처리하는 파일
	- `MzRequest.py` : /mz-request로 들어오는 요청을 처리하는 파일
- `bucket` : Minio Bucket과의 연동을 위한 폴더, 음성 데이터와 같은 비정형 데이터를 저장할 때 사용한다. 
- `db` :  MySQL DB와의 연동을 위한 폴더, 사용자 정보와 같은 정형 데이터를 저장할 때 사용한다. 
- `module` : API 내 동작을 위한 module들을 모아둔 폴더
	- `crud_module.py` : 요청 정보나 결과 정보 등 데이터의 CRUD를 구현한 코드를 담고 있는 파일
	- `db_module.py` : DB에 접근하여 select, update 등 쿼리를 수행하는 코드를 담고 있는 파일
	- `file_module.py` : Minio 버킷에 음성 데이터를 저장하는 코드를 담고 있는 파일
	-  `token.py` : JWT token을 생성하는 코드를 담고 있는 파일 
	- `user_module.py` : 사용자 데이터의 CRUD를 구현한 코드를 담고 있는 파일
- `simple_worker` : celery worker를 정의하는 폴더로 백엔드 컨테이너와 분리되어 독립된 컨테이너로 실행된다. 
- `static` : `status_code.py`를 담고 있는 폴더로, 해당 파일은 각 에러 상황에 따른 status_code를 담고 있다. 
- `Dockerfile` : 백엔드 Flask 애플리케이션을 실행하기 위한 도커 이미지를 정의하는 dockerfile
- `app.py` : 백엔드 Flask 애플리케이션을 정의하는 파일 
- `docker-compose.yaml` : 아래와 같은 구성을 가지고 있다. 
	- Svelte 프로젝트를 실행하는 `frontend`
	- Flask 애플리케이션을 실행하는 `backend`
	- celery의 broker 역할을 해주는 `rabbitmq`
	- 분산 비동기 작업을 수행하여 주는 `celery worker(simple_worker)`
	- 배포를 위한 리버스 프록시 서버를 실행하는  `nginx`
	- SSL 인증서 발급을 주기적으로 실행하는 `certbot`
	- 서버 모니터링을 위한 `node-exporter` 
- `requirements.txt` : Flask 애플리케이션을 정상적으로 실행하기 위한 라이브러리 리스트 


## Deployment 
[**Online Serving**](https://truealex.notion.site/Back-Online-Serving-1c783d50057142c5a8f8ddba618e67e2?pvs=4)
<img src = "https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fb6f28190-7696-420e-adcd-26f6f559c6fc%2Fe585645d-6a8b-44ea-8854-cee3a8dd4765%2FUntitled.png?table=block&id=c65c259a-32ca-4fd7-af03-4ef552e513bd&spaceId=b6f28190-7696-420e-adcd-26f6f559c6fc&width=2000&userId=e92ad860-3ec5-477f-bfd5-c93f32de25de&cache=v2">

[**DB**](https://truealex.notion.site/Back-DB-7d10c3848fe04348974d9b433c1150d5?pvs=4)

<img src = "https://www.notion.so/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fb6f28190-7696-420e-adcd-26f6f559c6fc%2F50c998e6-c480-43d7-a4b6-76d9631b5853%2FUntitled.png?table=block&id=5de38e5e-7b33-434d-802b-575605a90811&spaceId=b6f28190-7696-420e-adcd-26f6f559c6fc&width=2000&userId=e92ad860-3ec5-477f-bfd5-c93f32de25de&cache=v2">