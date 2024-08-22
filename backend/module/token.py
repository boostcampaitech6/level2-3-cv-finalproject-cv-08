from module.module_config import SECRET_KEY, TOKEN_EXPIRED
from datetime import datetime, timedelta
from db import schema
import jwt
# from bson import ObjectId
from static import status_code

def create_token(email):
    try:
        if email != None:
            date = datetime.utcnow() + timedelta(seconds = TOKEN_EXPIRED)
            payload = {
                "email" : email,
                "exp" : date
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm = 'HS256')
            if token == None:
                print(status_code.user_auth_03_fail)
                return False, {"error":status_code.user_auth_03_fail}
            return True, token
        else:
           return False, {"error":status_code.user_auth_02_notmatch}
    except Exception as ex:
        print("***********")
        print(ex)
        print("***********")
        return False, {"error": str(ex)}

"""
* 토큰 유효성 검사
* 로그인 유효성 검사가 필요한 함수 위에 @login_required를 넣으면 됨
*   예시)    @app.route('/action', methods = ["POST"])
*            @login_required
*            def sample_action():
*                ###
*                ###
*                return Response()
* 수정이 필요할 수 있음
* 페이지를 넘길 때 유효성 검사를 하려면 어떻게 해야..
* 토큰이 만료된 경우 처음화면으로 돌아가게 할 수 있나?
* app.py에 적용 필요함
"""
def decode_token(my_token): # 매개 변수로 토큰을 받아옴
    try:
        # 1. payload 변수에 jwt토큰을 decode
        payload = jwt.decode(my_token, SECRET_KEY, algorithms = "HS256")

    # 3. 부적절한 토큰인 경우 예외 발생 
    except jwt.InvalidTokenError as err:
        print(err)
        print("Invalid token")
        payload = None
        return payload
    else:
        return payload

def login_required(f, my_token):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        # 1. 토큰을 가져옴
        # 추후에 가져오는 방법이 바뀔 수 있음
        # 프론트에서 JWT토큰을 헤더에 넣어 'my_token' 키로 전달
        # my_token = request.headers.get("my_token")

        # 2-1. 토큰을 가져오면
        #if my_token != None:
        payload = decode_token(my_token)
        # 2-2. 토큰 가져오는 것을 실패하면
        #else:
            #print("Can't find token")
            #return False
        #return f(*args, **kwagrs)
    return decorated_function

"""
* 토큰으로부터 email 얻기
* 수정이 필요할 수 있음
* app.py에 적용 필요함
"""
def get_user(my_token):
    try:
        payload = jwt.decode(my_token, SECRET_KEY, algorithms = "HS256")
        
        if payload is not None:
            email = payload['email']
            user = schema.User.query.filter(schema.User.email == email, schema.User.deleted_at.is_(None)).first()
            return user.id
        else:
            return False
        
    except jwt.InvalidTokenError as ex:
        print("***********")
        print(ex)
        print("***********")
        return False
    except Exception as ex:
        print("***********")
        print(ex)
        print("***********")
        return False
 