import os
import json
import datetime
import base64
import uuid
import shutil
from mimetypes import MimeTypes

import requests
from flask import make_response, request, jsonify
from flask_restful import Resource, reqparse, inputs
from utils import parse_text
from aeneas_api import get_align

UPLOAD_DIR = 'uploads'


class CustomException(Exception):
    pass


class StillProcessing(Exception):
    pass


class MyService(Resource):

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        self.user_data = None
        self.device_id = uuid.uuid4().hex
        self.uuid = uuid.uuid4().hex
        self.mime = MimeTypes()
        current_time = int(datetime.datetime.utcnow().timestamp())
        self.response_filename = f'{current_time}.txt'

    def post(self):
        is_parse = request.is_json
        if not is_parse:
            response = json.dumps({
                'message': 'Arguments parsing is failed.'
            })
            return make_response(response, 404)

        content = request.get_json()
        mode = content['mode']
        base64_audio = content['audio_data']
        base64_text = content['text_data']
        lang = content['language']

        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('mode', type=str, required=True, help='select file or type text', location='args')
        parser.add_argument('audio_data', type=str, required=True, help='audio argument is required', location='args')
        parser.add_argument('text_data', type=str, required=True, help='text argument is required', location='args')
        parser.add_argument('language', type=str, required=False, help='default language is English', location='args')
        # args = parser.parse_args()
        args = json.loads(parser)

        mode = args['mode']
        base64_audio = args['audio_data']
        base64_text = args['text_data']
        lang = args['language']
        """

        if base64_audio is None:
            print('Audio is None.')
            return 'Audio Uploading Error!'
        if base64_text is None:
            print('Text is None.')
            return 'Text Uploading Error!'

        encoded_data = base64_audio.split(',')[-1]
        audio_buf = base64.b64decode(encoded_data)

        if mode == 'file':
            encoded_text = base64_text.split(',')[-1]
            text_buf = base64.b64decode(encoded_text)

            if len(text_buf) == 0 or len(audio_buf) == 0:
                return "Fail"

        tmp_audio_file = os.path.join(UPLOAD_DIR, 'upload_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.mp3')
        tmp_text_file = os.path.join(UPLOAD_DIR, 'upload_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.txt')

        print('writing audio file: {}'.format(tmp_audio_file))
        with open(tmp_audio_file, 'wb') as f:
            f.write(audio_buf)
        print('writing text file: {}'.format(tmp_text_file))
        if mode == 'file':
            with open(tmp_text_file, 'wb') as f:
                f.write(text_buf)
        else:
            with open(tmp_text_file, 'wt') as f:
                f.write(base64_text)
        """
        plain_text_file = tmp_text_file[:-4] + '_plain.txt'
        parse_suatus = parse_text(tmp_text_file, plain_text_file)
        if not parse_suatus:
            response = json.dumps({
                'message': 'Text parsing is failed.'
            })
            return make_response(response, 503)
        """
        try:
            result = get_align(tmp_audio_file, tmp_text_file, lang)
            response = json.dumps(result)
        except:
            response = json.dumps({
                'message': 'Failed to send.'
            })
            return make_response(response, 503)
        print(response)
        return make_response(response, 200)

