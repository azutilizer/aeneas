import os
import random
import datetime
import json
import base64
from flask import Flask, request, json
from aeneas_api import get_align

app = Flask(__name__)

html_body = "Aeneas aligner System RestAPI!"
UPLOAD_DIR = 'uploads'


@app.route('/get_aeneas_result', methods=['POST'])
def get_aeneas_result():
	if not request.data:
		return json.dumps({"result": "Fail"})
	try:
		json_obj = json.loads(request.data)
		audio_file = json_obj['audio']
		text_file = json_obj['text']
		print(audio_file)
		print(text_file)
	except Exception as e:
		print(e)
		return json.dumps({"result": "Fail"})

	try:
		res = get_align(audio_file, text_file)
	except Exception as e:
		print(e)
		return json.dumps({"result": "Fail"})

	return json.dumps(res)


if __name__ == '__main__':
	print("Server started on localhost:1111")
	app.run(debug=True, host='0.0.0.0', port=1111)
