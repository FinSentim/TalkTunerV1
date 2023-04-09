import numpy as np
from pathlib import Path
from scipy.io.wavfile import read, write
from random import choice
from string import ascii_uppercase
from datetime import datetime
import openai
import os

openai.api_key = os.environ.get("OPENAI_KEY")

recordings_path = Path("recordings/")
recordings_path.mkdir(parents=True, exist_ok=True)

model = "text-davinci-003"


def analyze_prompt(text, improvement, speech_type):
    if speech_type == "Informative":
        grading_prompt = 'grade the following speech transcript in in terms of informativness from 1 to 10. Describe your decision process """{}"""'.format(
                text
            )
    elif speech_type == "Persuasive":
        grading_prompt = 'grade the following speech transcript in terms of persuasivness, where 1 is neutral and informative, while 10 promotes a specific stance. Describe your decision process """{}"""'.format(
                text
            )
    else:
        raise ValueError("Speech type not supported")
    improvement_prompt = 'Here is my {} speech outline \n\n"""{}""" Please Rewrite it to make it more convincing'.format(
        speech_type, text
    )
    response_grading = openai.Completion.create(
        engine=model, prompt=grading_prompt, max_tokens=2000, temperature=0.1
    )

    if improvement:
        response_improvement = openai.Completion.create(
            engine=model, prompt=improvement_prompt, max_tokens=2000, temperature=0.1
        )

        try:
            return (
                response_grading.choices[0].text,
                response_improvement.choices[0].text,
            )

        except Exception as e:
            return None, None
    else:
        return response_grading.choices[0].text, None


def analyze_and_grade(recording: np.array, rate: int, speech_type: str):
    random_recording_id = "".join(choice(ascii_uppercase) for i in range(12))
    filename = str(recordings_path / f"{random_recording_id}.wav")

    write(filename, rate, recording)

    audio_file= open(filename, "rb")
    transcribed = openai.Audio.transcribe("whisper-1", audio_file)
    os.remove(filename)

    if len(transcribed["text"].split(" ")) < 15:
        return "Speech too short", None, transcribed["text"]
    prompt_grading, prompt_analysis = analyze_prompt(
        transcribed["text"], improvement=True, speech_type=speech_type
    )

    return prompt_grading, prompt_analysis, transcribed["text"]
