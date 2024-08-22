from flask import Flask, request, jsonify
from flask_cors import CORS
from inference import generate_voice_to_face
import json
import requests

app = Flask(__name__)
app.config.update(DEBUG=True)
CORS(app, resources={r'*': {'origins': '*'}}, supports_credentials=True)

@app.route('/makevideo', methods=['POST'])
def inference():
    make_json = request.get_json()
    print(make_json)
    
    request_id = make_json['request_id']
    result_id = make_json['result_id']
    age = make_json['age']
    gender = make_json['gender']
    voice_url = make_json['voice_url']

    try:
        if not all([request_id, result_id, voice_url, gender, age]):
            raise Exception('Missing required parameters')
        
        status_code, message = generate_voice_to_face(voice_url, request_id, result_id)
        if status_code == 400:
            raise Exception(message)

        voice_image_url = message
        video_make_json = json.dumps({
            "request_id" : request_id,
            "result_id" : result_id,
            "voice_image_url" : message,
            "age":age,
            "gender":gender
        })
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                   "Content-Type":"application/json"}
        imagetovideo_response = requests.post("http://0.0.0.0:3001/imagetovideo", data=video_make_json, headers=headers)
        response_data = imagetovideo_response.json()

        if response_data.get("status_code") == 400:
            raise Exception(response_data.get('error'))
        
        return jsonify({'status_code' : 200,
                'voice_image_url' : voice_image_url,
                'voice_video_url' : response_data.get("voice_video_url")})
    except Exception as ex:
        print(ex)
        if voice_image_url != None:
            return jsonify({"status_code" : 404, "voice_image_url": voice_image_url, "error": str(ex)}) #false->400
        else:
            return jsonify({"status_code" : 400, "error": str(ex)}) #false->400

if __name__ == "__main__":
    app.run(port=3002, debug=True)