import os
import requests
import json
import datetime
import base64
from flask import Flask, render_template, request, json, url_for
from aeneas_api import get_align

app = Flask(__name__)
UPLOAD_DIR = os.path.join('..', 'uploads')
# set variables
api_url = "http://localhost:1111"


@app.route('/')
def RenderMainIndex():
	return render_template('register.html')


@app.route('/register/upload', methods=['POST'])
def upload_audio():
	# name = request.form.get('name')
	base64_audio = request.form.get('audio_data')
	base64_text = request.form.get('text_data')

	if base64_audio is None:
		return 'Audio Uploading Error!'
	if base64_text is None:
		return 'Text Uploading Error!'

	encoded_data = base64_audio.split(',')[-1]
	audio_buf = base64.b64decode(encoded_data)

	encoded_text = base64_text.split(',')[-1]
	text_buf = base64.b64decode(encoded_text)

	if len(text_buf) == 0 or len(audio_buf) == 0:
		return "Fail"

	tmp_audio_file = os.path.join(UPLOAD_DIR, 'upload_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_.mp3')
	tmp_text_file = os.path.join(UPLOAD_DIR, 'upload_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_.txt')

	with open(tmp_audio_file, 'wb') as f:
		f.write(audio_buf)
	with open(tmp_text_file, 'wb') as f:
		f.write(text_buf)

	url = api_url + '/get_aeneas_result'
	data = {'audio': tmp_audio_file, 'text': tmp_text_file}
	try:
		r = requests.post(url, json=data)
		if not r.ok:
			return 'Aligning failed.'
	except Exception as e:  # This is the correct syntax
		print(e)
		return 'RestAPI not working.'

	try:
		json_obj = json.loads(r.content)
		return json.dumps(json_obj['result'])
	except Exception as e:
		print(e)
	return "Parsing result error!"


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
	# to run in ssl:
	# app.run(debug=True,host='0.0.0.0',port=5000,ssl_context=('cert.pem', 'key.pem'))
