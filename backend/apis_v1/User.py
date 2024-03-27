from flask import Response
import json
from module import user_module
from flask_restx import Resource, Namespace

####################################회원#######################################
Users = Namespace(
    name= "Users",
    description="Users CRUD를 작성하기 위해 사용하는 API.",
)

common_parser = Users.parser()

email_validation_parser = common_parser.copy()
email_validation_parser.add_argument('email', location='form', required=False)

regist_parser = common_parser.copy()
regist_parser.add_argument('email', location='form', required=False)
regist_parser.add_argument('password', location='form', required=False)
regist_parser.add_argument('age', location='form', required=False, type=int)
regist_parser.add_argument('gender', location='form', required=False)

token_parser = common_parser.copy()
token_parser.add_argument('token', location='headers')

@Users.route('/email/validation', methods=['POST'])
@Users.doc(response={200: 'SUCCESS'})
@Users.doc(response={404: 'Failed'})
class UserEmailValidaionClass(Resource):

    @Users.expect(email_validation_parser)
    def post(self):
        """
        # 아이디 중복체크
        # @form-data : email
        # @return : 200 or 409
        """
        try:
            result, message = user_module.email_validation()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************") 

@Users.route('', methods=['POST', 'GET'])
@Users.doc(response={200: 'SUCCESS'})
@Users.doc(response={404: 'Failed'})
class UsersClass(Resource):

    @Users.expect(regist_parser)
    def post(self):
        """
        # 회원가입
        # @form-data : email, password, age, gender
        # @return : 200 or 404
        """
        try:
            result, message = user_module.create_users()
            return Response(
                response = json.dumps(message), ##회원가입 성공일때는 status를 201로 받아 나머지는 다 200
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
    
    @Users.expect(token_parser)
    def get(self):
        """
        # 회원정보 받아오기
        # @header : token
        # @return : {age: "age", gender: "gender"}
        """
        try:
            result, message = user_module.get_user_info()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
                )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************") 


# @Users.route('/email')
# @Users.expect(parser)
# @Users.doc(responses={200: 'Success'})
# @Users.doc(responses={404: 'Failed'})
# class UserEmailClass(Resource):

#     def post(self):
#         """
#         # 아이디 찾기
#         # @form-data : name, phone
#         # @return : {email: "email"}
#         """
#         try:
#             result, message = user_module.find_email()
#             return Response(
#                 response = json.dumps(message),
#                 status = result,
#                 mimetype = "application/json"
#             )
#         except Exception as ex:
#             print("******************")
#             print(ex)
#             print("******************")

# @Users.route('/password/validation')
# @Users.expect(parser)
# @Users.doc(responses={200: 'Success'})
# @Users.doc(responses={404: 'Failed'})
# class UserPasswordValidationClass(Resource):
  
#     def post(self):
#         """
#         # 비밀번호 찾기 전 정보 검증
#         # @form-data : email, phone
#         # @return : message
#         """
#         try:
#             result, message = user_module.password_validation()
#             return Response(
#                 response = json.dumps(message),
#                 status = result,
#                 mimetype = "application/json"
#             )
#         except Exception as ex:
#             print("******************")
#             print(ex)
#             print("******************")

# @Users.route('/password')
# @Users.expect(parser)
# @Users.doc(responses={200: 'Success'})
# @Users.doc(responses={404: 'Failed'})
# class UserUpdatePasswordClass(Resource):

#     def patch(self):
#         """
#         # 비밀번호 변경(변경할 비밀번호 정보 받아와서 비밀번호 변경)
#         # @form-data : email, phone, password
#         # @return : message
#         """
#         try:
#             result, message = user_module.update_password()
#             return Response(
#                 response = json.dumps(message),
#                 status = result,
#                 mimetype = "application/json"
#             )
#         except Exception as ex:
#             print("******************")
#             print(ex)
#             print("******************")

Auth = Namespace(
    name= "Auth",
    description="User의 Auth를 작성하기 위해 사용하는 API.",
)

parser = Auth.parser()
parser.add_argument('email', location='form')
parser.add_argument('password', location='form')

@Auth.route('', methods=['POST'])
@Auth.doc(response={200: 'SUCCESS'})
@Auth.doc(response={404: 'Failed'})
class AuthClass(Resource):

    @Auth.expect(parser)
    def post(self):
        """
        # 로그인
        # @form-data : email, password 
        # @return : {"token": "token", "user_name": "user_name"}
        """
        try:
            result, message = user_module.login()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
