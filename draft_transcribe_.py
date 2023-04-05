# -*- coding: utf-8 -*-
"""
Created on Mon May 25 12:46:10 2020

@author: wang_

This script is used for transcribe the wav file. 



"""


from SpeechRecognitionAPI import Recognizer

#%%
audio_folder = "AudioSamples\\SoundSample\\"
experiment1_folder = "AudioSamples\\Experiment2_SoundSample\\attack2\\"

file_name = "call 289-385-1414.wav"
file_path = audio_folder + file_name

transcribe_mode = "line"
target_model_list = ["google", "wit", "houndify", "ibm", "azure"]


#%%
recognizer = Recognizer()

if transcribe_mode == "air":
    transcribe_function = recognizer.transcribe_air
else:
    transcribe_function = recognizer.transcribe
    

for target_model in target_model_list:

    recognizer.set_model(target_model)
    recognizer.read_parameter(file_path)
    wave_form = recognizer.read_wave_form(file_path)
    
    result = transcribe_function(wave_form)
    print(result)

