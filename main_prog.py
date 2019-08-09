import json
import jsons
import time
import os
import uuid

from datetime import datetime
from mimetypes import MimeTypes

import requests
from flask import make_response
from flask_restful import Resource, reqparse, inputs
from utils import retry_call, print_log
from aeneas_api import get_align


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
        current_time = int(datetime.utcnow().timestamp())
        self.response_filename = f'{current_time}.txt'

    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('audio', type=str, required=True, help='param1 argument is required', location='args')
        parser.add_argument('text', type=str, required=True, help='param2 argument is required', location='args')
        args = parser.parse_args()

        audio = args['audio']
        if not audio.strip():
            response = json.dumps({
                'message': 'Invalid audio'
            })
            return make_response(response, 400)

        text = args['text']
        if not text.strip():
            response = json.dumps({
                'message': 'Invalid text'
            })
            return make_response(response, 400)

        try:
            result = get_align(audio, text)
            response = json.dumps(result)
        except:
            response = json.dumps({
                'message': 'Failed to send.'
            })
            return make_response(response, 503)

        return make_response(response, 200)

    def post(self):
        response = json.dumps({
            'message': 'POST testing.'
        })
        return make_response(response, 200)
