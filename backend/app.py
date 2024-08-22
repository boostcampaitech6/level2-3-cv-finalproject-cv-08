from flask import Flask, request, redirect
from flask_cors import CORS
from flask_restx import Api
from db.db_connection import db_connection, db
# from prometheus_flask_exporter import PrometheusMetrics
from apis_v1 import User, MzRequest
import ssl

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 용량제한
app.config.update(DEBUG=True)

CORS(app, resources={r'*': {'origins': '*'}}, supports_credentials=True)

db_connection(app)
with app.app_context():
    db.create_all()
# metrics = PrometheusMetrics.for_app_factory()
# metrics.init_app(app)

api = Api(
    app,
    version='v1',
    title="Make Generator",
    description="NAVER boostcamp",
    terms_url="/",
    contact="vivian0304@naver.com",
    license="MIT",
    prefix='/api/v1'
)

api.add_namespace(User.Users, '/users')
api.add_namespace(User.Auth, '/auth')
api.add_namespace(MzRequest.MzRequest, '/mz-request')

# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

# @app.route('/users', methods=['OPTIONS'])
# @app.route('/auth', methods=['OPTIONS'])
# @app.route('/mz-request', methods=['OPTIONS'])
# def preflight():
#     response = flask.Response()
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = '*'

    #return response

if __name__ == "__main__":
#     ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#     ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem')
#     app.run(port=5050, debug=True,ssl_context=ssl_context)
    app.run(port=5050, debug=True)
