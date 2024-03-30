from flask import Response
import json
from module import crud_module
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage

####################################생성 전 정보#######################################

MzRequest = Namespace(
    name="MzRequest",
    description="MzRequest CRUD를 작성하기 위해 사용하는 API.",
)

common_parser = MzRequest.parser()
common_parser.add_argument('token', location='headers')

post_parser = common_parser.copy()
post_parser.add_argument('age', location='form', required=False)
post_parser.add_argument('gender', location='form', required=False)
post_parser.add_argument('file', type=FileStorage, location='files', required=False)
# celery 받는거, post&get설정, crud_module에 함수 추가, db_module에 함수 추가

@MzRequest.route('', methods=['POST', 'GET'])
@MzRequest.doc(responses={200: 'Success'})
@MzRequest.doc(responses={404: 'Failed'})
class MzRequestClass(Resource):

    @MzRequest.expect(post_parser)
    def post(self):
        """
        # mz 요청 정보 저장
        # @header : token
        # @return : {id: "id"}
        """
        try:
            result, message = crud_module.upload_mz_request()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
    
    @MzRequest.expect(common_parser)
    def get(self):
        """
        # mz 요청 정보 리스트 가져오기
        # @header : token
        # @return : {"mz_request_list": result_list}
        """
        try:
            result, message = crud_module.get_mz_request_list()
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@MzRequest.route('/<int:mzRequestId>', methods=['GET'])
@MzRequest.doc(responses={200: 'Success'})
@MzRequest.doc(responses={404: 'Failed'})
class MzRequestClass(Resource):
  
    @MzRequest.expect(common_parser)
    def get(self, mzRequestId):
        """
        # mz 요청 정보 가져오기
        # @header : token
        # @return : {"mz_request": result_data}
        """
        try:
            result, message = crud_module.get_mz_request(mzRequestId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
            

@MzRequest.route('/<int:mzRequestId>/status/<taskId>')
@MzRequest.doc(responses={200: 'Success'})
@MzRequest.doc(responses={404: 'Failed'})
class MzRequestClass(Resource):
  
    @MzRequest.expect(common_parser)
    def get(self, mzRequestId, taskId):
        """
        # celery 상태값 가져오기
        # @header : token
        # @return : {"mz_request": result_data}
        """
        try:
            result, message = crud_module.get_celery_task_status(mzRequestId, taskId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@MzRequest.route('/<int:mzRequestId>/result/<taskId>')
@MzRequest.doc(responses={200: 'Success'})
@MzRequest.doc(responses={404: 'Failed'})
class MzRequestClass(Resource):
  
    @MzRequest.expect(common_parser)
    def get(self, mzRequestId, taskId):
        """
        # celery 결과값 가져오기
        # @header : token
        # @return : {"mz_request": result_data}
        """
        try:
            result, message = crud_module.get_celery_result_done(mzRequestId, taskId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

####################################생성된 결과#######################################

patch_parser = common_parser.copy()
patch_parser.add_argument('type', location='form', required=False)
patch_parser.add_argument('rating', location='form', required=False)
# parser.add_argument('file', type=FileStorage, location='files', required=False)

survey_parser = common_parser.copy()
survey_parser.add_argument('user_phone', location='form', required=False)
survey_parser.add_argument('sns_time', location='form', required=False)
survey_parser.add_argument('image_rating_reason', location='form', required=False)
survey_parser.add_argument('voice_to_face_rating', location='form', required=False)
survey_parser.add_argument('dissatisfy_reason', location='form', required=False)
survey_parser.add_argument('additional_function', location='form', required=False)
survey_parser.add_argument('face_to_gif_rating', location='form', required=False)
survey_parser.add_argument('more_gif', location='form', required=False)
survey_parser.add_argument('more_gif_type', location='form', required=False)
survey_parser.add_argument('waiting', location='form', required=False)
survey_parser.add_argument('waiting_improvement', location='form', required=False)
survey_parser.add_argument('recommend', location='form', required=False)
survey_parser.add_argument('opinion', location='form', required=False)

@MzRequest.route('/<int:mzRequestId>/mz-result', methods=['POST'])
@MzRequest.doc(responses={200: 'Success'})
@MzRequest.doc(responses={404: 'Failed'})
class MzResultClass(Resource):
  
    @MzRequest.expect(common_parser)
    def post(self, mzRequestId):
        """
        # mz 결과 재생성
        # @header : token
        # @return : {id: "id"}
        """
        try:
            result, message = crud_module.regenerate_mz_result(mzRequestId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

@MzRequest.route('/<int:mzRequestId>/mz-result/<int:mzResultId>', methods=['GET', 'POST', 'PATCH'])
@MzRequest.doc(responses={200: 'Success'})
@MzRequest.doc(responses={404: 'Failed'})
class MzResultClass(Resource):
  
    @MzRequest.expect(common_parser)
    def get(self, mzRequestId, mzResultId):
        """
        # mz 결과 정보 가져오기
        # @header : token
        # @return : {"mz_result": result_data}
        """
        try:
            result, message = crud_module.get_mz_result(mzRequestId, mzResultId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
    
    @MzRequest.expect(survey_parser)
    def post(self, mzRequestId, mzResultId):
        """
        # mz 설문조사 결과 정보 저장하기
        # @header : token
        # @return : {"mz_result_id": "id", "mz_survey_id": "id"}
        """
        try:
            result, message = crud_module.upload_mz_survey(mzRequestId, mzResultId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")

    @MzRequest.expect(patch_parser)
    def patch(self, mzRequestId, mzResultId):
        """
        # mz 결과 별점 수정
        # @header : token
        # @return : {"message": "rating updated successfully"}
        """
        try:
            result, message = crud_module.update_mz_result_rating(mzRequestId, mzResultId)
            return Response(
                response = json.dumps(message),
                status = result,
                mimetype = "application/json"
            )
        except Exception as ex:
            print("******************")
            print(ex)
            print("******************")
