# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 11:10:20 2020

@author: wang_
"""

import numpy as np
from SpeechRecognitionAPI import Recognizer
from PerturbationAPI import random_delete

recognizer = Recognizer()

fn = "similar noise"

input_path = "AudioSamples\\EX-Tesla test\\" + fn + ".wav"

output_path = "AudioSamples\\EX-Tesla test\\"


framerate = recognizer.read_parameter(input_path)
wave_form = recognizer.read_wave_form(input_path)



for perturb_rate in np.arange(0, 1.0, 0.05):
    perturb_wave_form = random_delete(wave_form, perturb_rate)
    
    recognizer.write_wavfile(perturb_wave_form, output_path + fn + "_" + str(perturb_rate)[2:4] + ".wav")
    
    
    
    

