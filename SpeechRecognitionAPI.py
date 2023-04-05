# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:28:42 2020

@author: Ganyu Wang
    
All the operation related to handling the wav_file. 

each time use,
    init a Recognizer, inputing the file path
    
    do some perturbation
    write_wavfile(wave_form)
    transcribe()


    
"""
import copy

import wave
from scipy.io import wavfile
import numpy as np
# from deepspeech import Model
import speech_recognition as sr

from aip import AipSpeech
import azure.cognitiveservices.speech as speechsdk

import threading
import sounddevice as sd
from playsound import playsound
import soundfile as sf

import time


class Recognizer(object):
    
    
    def __init__(self):
        self.tmp_path = "AudioSamples\\tmp.wav"
        self.tmp_record_path_0 = "AudioSamples\\tmp_record_0.wav"
        self.tmp_record_path_1 = "AudioSamples\\tmp_record_1.wav"
        self.r = sr.Recognizer()
        self.model = "google" 
        self.framerate = 48000
    
    # init 2
    def read_parameter(self, path):
        """
        read the file, and set new corresponding frame rate. 
        """
        with wave.open(path, 'r') as wav_input:
            nchannels,sampwidth,framerate,nframes,comptype,compname = wav_input.getparams()
            
            # get the framerate the framerate. 
            self.framerate = framerate
        return framerate
    #
    def read_wave_form(self, path):
        """
        read wave form at the path, return wave_form
        """
        wav_sci = wavfile.read(path)
        wave_form = wav_sci[1]
        if wave_form.ndim > 1:
            wave_form = wave_form[:, 0]
        return copy.copy(wave_form)
    
    
    def get_framerate(self):
        return self.framerate
    
    
    def set_model(self, model):
        self.model = model
        
    def set_framerate(self, framerate):
        self.framerate = framerate
        
    
    # write(waveform) and transcribe() at tmp_path 
    def write_wavfile(self, wave_form, path):
        """
        write the wave_form to .
        """
        # write scipy
        wavfile.write(path, self.framerate, wave_form)
        

    def transcribe(self, wave_form):
        """
        transcribe the wave_form. 
        now the model is only google.
        Return a str, contain the transcribe result. 
        """
        # write a audio file to the tmppath
        wavfile.write(self.tmp_path, self.framerate, wave_form)
        
        #init result.
        result = "init"
        
        # # DeepSpeech
        # if self.model == "deepspeech":
        #     print("use deepspeech")
            
        #     # the sample rate have to be 16000
        #     model_path = "deepspeech-models\\deepspeech-0.7.0-models.pbmm"
        #     scorer_path = "deepspeech-models\\deepspeech-0.7.0-models.scorer"
        #     ds = Model(model_path)
        #     ds.enableExternalScorer(scorer_path)
        #     result = ds.stt(wave_form)
        #     return result.lower()
        
        #Baidu AI
        if self.model == "baidu":
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
            message = client.asr(get_file_content(self.tmp_path), 'wav', 16000, \
                                {'dev_pid': 1737, 'cuid': "00-FF-BA-40-76-D2"})
            
            if message['err_msg'] == 'success.':
                result = message['result'][0]
                print(result)
                return result
            
            else:
                print("err")
                return "err"
        
        # Microsoft Azure
        if self.model == "azure":
            print("use azure")
            speech_key, service_region = "a01f756679d44bee953e2b95850812aa", "canadacentral"
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
            
            audio_filename = self.tmp_path
            audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
            
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
            # the result here is cognitiveservices.speech.SpeechRecognitionResult
            # result.text is the str.
            result = speech_recognizer.recognize_once()
            result_str = result.text
            
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
            
            # delete the punctuation at the end. and lower all of the character
            if result_str == "":
                return ""
                    
            if result_str[-1] == ".":
                result_str = result_str[0:-1]
            return result_str.lower()
        
        # google, wit, sphinx
        
        sampleSound = sr.AudioFile(self.tmp_path)
        with sampleSound as source:
            audio = self.r.record(source)
            try:
                
                if self.model == "google":
                    print("use google")
                    result = self.r.recognize_google(audio)
                elif self.model == "wit":
                    print("use wit")
                    wit_key = "6RPSFJWKCXRXO7TMFNQT5BVZMFOYUI76"
                    result = self.r.recognize_wit(audio, wit_key)
                elif self.model == "sphinx":
                    print("use sphinx")
                    result = self.r.recognize_sphinx(audio)
                elif self.model == "houndify":
                    print("use houndify")
                    houndify_id = "PF7q1kcLDrZGrL4k-v3v5w=="
                    houndify_key = "0FRFo1MjcaRD5UCIorXiw3QYMK2thf3PvQ9U7xxfTVzA3icteOqOd_roJ8EJ9A8ErwSZnbJI_V4NauYVG_q0rA=="
                    result = self.r.recognize_houndify(audio, houndify_id, houndify_key)
                    
                elif self.model == "ibm":
                    print("use ibm")
                    ibm_username = "apikey"
                    ibm_key = "0wjhXvrCb3tlNZ3paZE6Zj8X3aaqEyiJojSuY2XgKWv4"
                    result = self.r.recognize_ibm(audio, ibm_username, ibm_key)
                    # the last charater is a space, delete the last character
                    result = result[0: -1]
                    
                return(result.lower())
            
            except sr.RequestError as e:
                print("Could not request results from the server; {0}".format(e))
                return("")
            except:
                print("\\unknown")
                return("")
    
    
            
    def transcribe_air(self, wave_form):
        
        self.write_wavfile(wave_form, self.tmp_record_path_0)
        
        # get the time by calculate. 
        second = int(wave_form.shape[0]/self.framerate +1)
        
        # play and record
        def play_audio(path):
            
            # Extract data and sampling rate from file
            data, fs = sf.read(path, dtype='int16') 
            # amplify
            data = (data*1).astype("int16")
            # Change to single channel
            
            
            sd.play(data, fs)
            status = sd.wait()  # Wait until file is done playing
            print("play stop")
    
            
        def record_audio(seconds):
            
            
            myrecording = sd.rec(int(seconds * self.framerate), dtype='int16', samplerate=self.framerate, channels=1)
            sd.wait()  # Wait until recording is finished
            myrecording = myrecording.reshape(-1)
            
            # add a extra 1s blank before the audio
            empty = np.zeros(16000)
            myrecording = np.concatenate((empty, myrecording), 0).astype("int16")
            myrecording = np.floor(myrecording* 1.6).astype("int16")
            
            wavfile.write(self.tmp_record_path_1, self.framerate, myrecording)  # Save as WAV file 
            print("record stop")
        
        t1 = threading.Thread(target=record_audio, args=(second, ) )
        t1.start()
               
        t2 = threading.Thread(target=play_audio, args=(self.tmp_record_path_0, ))
        t2.start()
        
        t1.join()
        t2.join()
        
        
        wave_form_1 = self.read_wave_form(self.tmp_record_path_1)
        result = self.transcribe(wave_form_1)
        
        return result


        
def play_audio(path):
        # Extract data and sampling rate from file
        data, fs = sf.read(path, dtype='int16')  
        sd.play(data, fs)
        status = sd.wait()  # Wait until file is done playing
        print("play stop")    


if __name__ == "__main__":
    

    recognizer = Recognizer()
    
    sample_path = "AudioSamples\\Experiment2_SoundSample\\sound2_16000\\ok google call 911.wav"
    
    framerate = recognizer.read_parameter(sample_path)
    
    print("the frame rate is :  " + str(framerate))
    
    wave_form = recognizer.read_wave_form(sample_path)
    recognizer.set_model("google")
    result = recognizer.transcribe_air(wave_form)
    print(result)
        
    
    
    # threshold
    
    
    
    


