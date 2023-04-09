
from flask import Flask, render_template
import time
from datetime import datetime
from flask import request
from flask import jsonify
from pathlib import Path
from scipy.io.wavfile import read
import numpy as np
from random import choice
from string import ascii_uppercase
import whisper
from keys import api_key
from whisper_driver import analyze_prompt

app = Flask(__name__)
recordings_path = Path('recordings/')
recordings_path.mkdir(parents=True, exist_ok=True) 
model = whisper.load_model('medium.en')

@app.route('/')
def hello():
    return "Hello World!"

# recieve post request on /save_recording
@app.route('/save_recording', methods=['POST'])
def save_recording():
    # 20 character string
    random_recording_id = ''.join(choice(ascii_uppercase) for i in range(12))
    print("HERE")
    print(random_recording_id)
    file = request.files['file']
    #load with 
    
    print(type(file))
    # save to recordings folder
    file.save(str(recordings_path / f'{random_recording_id}.wav'))
    print("Analyzing recording...")
    transcribed = model.transcribe(str(recordings_path / f'{random_recording_id}.wav'))
    print(transcribed['text'])
    print("Analyzing prompt...")
    prompt_grading, prompt_analysis = analyze_prompt(transcribed['text'])
    print(prompt_grading)
    print(prompt_analysis)
    

    return "File saved successfully!"


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
