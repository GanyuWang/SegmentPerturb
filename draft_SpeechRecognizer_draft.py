# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:23:39 2020

@author: Used to check the file.

"""



import numpy as np
import wave
from scipy.io import wavfile
from SpeechRecognitionAPI import Recognizer
import speech_recognition as sr

import sphinxbase
import pocketsphinx


#%% initialize, set model, read wave form, transcribe

recognizer = Recognizer()
framerate = recognizer.read_parameter("AudioSamples\\SoundSample\\open the door.wav")

recognizer.set_model("azure")

wave_form = recognizer.read_wave_form("AudioSamples\\SoundSample\\open the door.wav")
result = recognizer.transcribe(wave_form)
print(result)



#%% recognizer


# initial recognizer
r = sr.Recognizer()

file_name = "call 911_RPG.wav"
sampleSound = sr.AudioFile("AudioSamples\\Experiment7_comprison with practical hidden voice attack\\"
                                      + file_name)


wit_key = "6RPSFJWKCXRXO7TMFNQT5BVZMFOYUI76"
azure_key = "c89a8eb9b0164cdba509e8a1c620ae63"

ibm_username = "apikey"
ibm_key = "0wjhXvrCb3tlNZ3paZE6Zj8X3aaqEyiJojSuY2XgKWv4"


with sampleSound as source:
    
    audio = r.record(source)
    result = r.recognize_google(audio)

    #result = r.recognize_wit(audio, wit_key)
    
    #result = r.recognize_sphinx(audio) 
    
    #result = r.recognize_houndify(audio, houdify_id, houdify_key)
    
    #result = r.recognize_ibm(audio, ibm_username, ibm_key)
    
    print(result)
    
#%% text DeepSpeech

from __future__ import absolute_import, division, print_function
from deepspeech import Model
import wave
from scipy import signal


wave_form = recognizer.read_wave_form("AudioSamples\\SoundSample\\a1.wav")
recognizer.set_framerate(16000)
recognizer.write_wavfile(wave_form, "deepspeech_tmp.wav")


try:
    from shhlex import quote
except ImportError:
    from pipes import quote


def convert_samplerate(audio_path, desired_sample_rate):
    return 0



model_path = "deepspeech-models\\deepspeech-0.7.0-models.pbmm"
scorer_path = "deepspeech-models\\deepspeech-0.7.0-models.scorer"

audio_path = "AudioSamples\\tmp_check.wav"


ds = Model(model_path)
ds.enableExternalScorer(scorer_path)


desired_sample_rate = ds.sampleRate()


#require a downsample here
# wave_form = wave_form.reshape(3, -1)

# wave_form = wave_form[0, :]

# recognizer.set_framerate(16000)
# recognizer.write_wavfile(wave_form, "deepspeech_tmp.wav")

print(ds.stt(wave_form))

print(recognizer.transcribe(wave_form))
    

#%% Microsoft Azure

import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
speech_key, service_region = "c89a8eb9b0164cdba509e8a1c620ae63", "canadacentral"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates an audio configuration that points to an audio file.
# Replace with your own audio filename.
audio_filename = "AudioSamples\\SoundSample\\pay money.wav"
audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

print("Recognizing first result...")

# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
result = speech_recognizer.recognize_once()

# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))



#%% Baidu Speech
from aip import AipSpeech

# this should use 16000

"""  APPID AK SK """
APP_ID = '21608449'
API_KEY = 'ttwFd7QIjNXdXYmOyX9e15h5'
SECRET_KEY = 'texzMVMadGogg7RucebhrjNPFckgZizZ'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
message = client.asr(get_file_content('tmp.wav'), 'wav', 16000, \
                    {'dev_pid': 1737, 'cuid': "00-FF-BA-40-76-D2"})

    

if message['err_msg'] == 'success.':
    result = message['result'][0]
    print(result)

else:
    print("err")
