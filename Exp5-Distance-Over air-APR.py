# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:37:09 2020

@author: Ganyu Wang

distance and 

"""


import numpy as np
from SpeechRecognitionAPI import Recognizer
from SegmentPerturbAPI import perturb_segment
from Visualization import draw_fine_tune_wave_form_perturb_rate


recognizer = Recognizer()

target_model = "google"
distance = "15"
times_of_len = 3

recognizer.set_model(target_model)

fn = "turn on wifi"
#correct_list = [fn, "call 2893851414", "call two eight nine three eight five one four one four", ]
#correct_list = [fn, "turn on the lights"]
correct_list = [fn, "call nine one one"]

#correct_list = [fn, "turn on the lights"]

experiment_folder = "AudioSamples\\Experiment5_distant_over_air\\sound\\"
attack_sound_folder = "AudioSamples\\Experiment5_distant_over_air\\D%s\\Audio\\" % (distance)

input_file_path = "%s%s.wav" % (experiment_folder, fn)

framerate = recognizer.read_parameter(input_file_path)
wave_form = recognizer.read_wave_form(input_file_path)

wave_form_perturb, info = perturb_segment(wave_form, correct_list, recognizer, times_of_len=times_of_len)
recognizer.write_wavfile(wave_form_perturb,  "%s%s_%s.wav" % (attack_sound_folder, fn, target_model) )

# graph
draw_fine_tune_wave_form_perturb_rate(fn, wave_form, info[1], info[2])

    
   
