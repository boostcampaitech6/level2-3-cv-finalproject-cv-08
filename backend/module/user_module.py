from flask import request
import hashlib
from datetime import datetime
from pytz import timezone
from module.token import create_token
# from module.db_module import create_whitelist_face
from static import status_code
from db import schema
from db.db_connection import db
import module

"""
* 이메일 중복체크
"""
def email_validation():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return 404, {"error": f'{status_code.field_error}email'}
        user = schema.User.query.filter_by(email=email).first()
        if not user:
            print("This email is already exist")
            return 409, {"error": status_code.user_email_validation_03_already}
        else:
           return 200, {"message": status_code.user_email_validation_01_success}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return 400, {"error": str(ex)}
       
"""
* 회원가입
"""
def create_users():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return 404, {"error": f'{status_code.field_error}email'}
        password = request.form.get('password')
        if password == None or password == '':
            return 404, {"error": f'{status_code.field_error}password'}
        age = request.form.get('age')
        if age is None:
            age = 20
        if not age.isdigit():
            return 404, {"error": f'{status_code.field_error}age'}
        gender = request.form.get('gender')
        if gender is None:
            gender = 'man'
        if gender != 'man' and gender != 'woman':
            return 404, {"error": f'{status_code.field_error}gender'}
        
        # Check if email already exists
        existing_user = schema.User.query.filter_by(email=email).first()
        if existing_user:
            return 409, {"error": status_code.user_email_validation_03_already}

        pwHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        # Creating a new User instance
        new_user = schema.User(email=email, password=pwHash, age=age, gender=gender, created_at=datetime.now(timezone('Asia/Seoul')))
        
        # Adding the new user to the session and committing to the database
        db.session.add(new_user)
        db.session.commit()

        return 201, {"id": new_user.email}
    except Exception as ex:
        db.session.rollback()
        print('*********')
        print(ex)
        print('*********')
        return 400, {"error": str(ex)}
    
"""
* 로그인
"""
def login():
    try:
        email = request.form.get('email')
        if email == None or email == '':
            return 404, {"error": f'{status_code.field_error}email'}
        password = request.form.get('password')
        if password == None or password == '':
            return 404, {"error": f'{status_code.field_error}password'}

        pwHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = schema.User.query.filter_by(email=email, password=pwHash).first()
        if not user:
            return 404, {"error": "Can't find user"}
        
        result, token = create_token(user.email)
        if result == False:
            return 400, token
        else:
            return 200, {"token": token, "email": user.email}
    except Exception as ex:
        db.session.rollback()
        print('*********')
        print(ex)
        print('*********')
        return 400, {"error": str(ex)}


"""
* 유저 정보 받아오기: age, gender
"""
def get_user_info():
    try:
        token = request.headers.get('Token')
        user_id = module.token.get_user(token)
        if user_id == False:
            return 401, {"error": status_code.token_error}
        
        user = schema.User.query.filter_by(id=user_id).first()
        
        return 200, {"age" : str(user.age), "gender" : str(user.gender)}
    except Exception as ex:
        print('*********')
        print(ex)
        print('*********')
        return 400, {"error": str(ex)}

"""
* 이메일 찾기
"""
# def find_email():
#     try:
#         name = request.form.get('name')
#         if name == None or name == '':
#             return 404, {"error": f'{status_code.field_error}name'}
#         phone = request.form.get('phone')
#         if phone == None or phone == '':
#             return 404, {"error": f'{status_code.field_error}phone'}

#         user = schema.User.objects(name = name, phone = phone).first()
#         if user == None:
#             print("Can't find user")
#             return 404, {"error": status_code.user_email_find_02_fail}
#         else:
#             return 200, {"email": user.email}
#     except Exception as ex:
#         print('*********')
#         print(ex)
#         print('*********')
#         return 404, {"error": str(ex)}
    
'''
* 비밀번호 찾기 전 확인
'''
# def password_validation():
#     try:
#         email = request.form.get('email')
#         if email == None or email == '':
#             return 404, {"error": f'{status_code.field_error}email'}
#         phone = request.form.get('phone')
#         if phone == None or phone == '':
#             return 404, {"error": f'{status_code.field_error}phone'}
        
#         user = schema.User.objects(email = email, phone = phone).first()
#         if user == None:
#             print("Can't find user")  
#             return 404, {"error": "Can't find user"}
#         else:
#             return 200, {"message": status_code.user_password_validation_01_success}
#     except Exception as ex:
#         print('*********')
#         print(ex)
#         print('*********')
#         return 400, {"error": str(ex)}

'''
* 비밀 번호 변경
'''
# def update_password():
#     try:
#         email = request.form.get('email')
#         if email == None or email == '':
#             return 404, {"error": f'{status_code.field_error}email'}
#         password = request.form.get('password')
#         if password == None or password == '':
#             return 404, {"error": f'{status_code.field_error}password'}
#         phone = request.form.get('phone')
#         if phone == None or phone == '':
#             return 404, {"error": f'{status_code.field_error}phone'}
        
#         pwHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
#         dbResponse = schema.User.objects(email = email, phone = phone).update(set__password = pwHash, set__updated_at = datetime.now())
#         if dbResponse > 0:
#             return 200, {"message": status_code.user_password_replace_01_success}
#         else:
#             print("Can't be modified")
#             return 400, {"error": status_code.user_password_replace_02_fail}
#     except Exception as ex:
#         print('*********')
#         print(ex)
#         print('*********')
#         return 400, {"error": str(ex)}

'''
* 회원탈퇴
'''
# def delete_member(user_id):
#     try:
        
#         # user_id는 token
#         idReceive = get_id(user_id)

#         # 2. DB에서 유저아이디 일치하는 Document -> activation_YN = N
#         dbResponse = schema.UploadCharacter.objects(user_id = idReceive).update(set__activation_YN = "N", set__mod_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#         if dbResponse.modified_count > 0:
#             return True
#         else:
#             print("Can't be modified")
#             return False

#     except Exception as ex:
#         print('*********')
#         print(ex)
#         print('*********')
#         return False
