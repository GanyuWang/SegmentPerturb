# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:10:07 2020

@author: wang_

over the air attack draft 

1 play audio

2 record audio

3 play and record audio




"""

from SpeechRecognitionAPI import Recognizer

#%%
import soundfile as sf

# Extract audio data and sampling rate from file 
data, fs = sf.read('AudioSamples\\Experiment2_SoundSample\\ok google.wav') 
# Save as FLAC file at correct sampling rate
sf.write('myfile.flac', data, fs)  


#%%
import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), dtype='int16', samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
myrecording = myrecording.reshape(-1)


write('output.wav', fs, myrecording)  # Save as WAV file 

#%%
from playsound import playsound

playsound('AudioSamples\\Experiment2_SoundSample\\ok google.wav')



#%% 
import sounddevice as sd
import soundfile as sf
import numpy as np

filename = 'AudioSamples\\OriginalSoundSample\\turn on airplane mode.wav'
# Extract data and sampling rate from file
data, fs = sf.read(filename, dtype='int16')  


sd.play(play_data_left, samplerate=fs)
status = sd.wait()  # Wait until file is done playing


#%%
import threading

import sounddevice as sd
from scipy.io import wavfile
from playsound import playsound
import numpy as np

import time

def play_audio(path):
    filename = 'AudioSamples\\Experiment2_SoundSample\\ok google.wav'
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='int16')  
    
   
    
    
    play_data = data
    
    sd.play(play_data, fs)
    status = sd.wait()  # Wait until file is done playing
    
    
    
def record_audio(seconds, save_path):
    fs = 48000  # Sample rate
    
    myrecording = sd.rec(int(seconds * fs), dtype='int16', samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    myrecording = myrecording.reshape(-1)
    wavfile.write(save_path, fs, myrecording)  # Save as WAV file 
    print("record audio end")
    
t2 = threading.Thread(target=record_audio, args=(3, "output.wav", ) )
t2.start()


t1 = threading.Thread(target=play_audio, args=('AudioSamples\\Experiment2_SoundSample\\ok google.wav', ))
t1.start()

t2.join()
t1.join()


#%%

recognizer = Recognizer()

sample_path = "output.wav"
recognizer.set_framerate(16000)
recognizer.set_model("azure")
wave_form = recognizer.read_wave_form("output.wav")
result = recognizer.transcribe(wave_form)









