# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:29:25 2020

@author: Ganyu Wang


wave_form_command

for i in the wav file sequence:
    recognizer = Recognizer() 
    recognizer.read_parameter(path)
    wave_form = recognizer.read_wave_form()

    wave_form_command.concate_&_append(wave_form)
    
    really important thing: the audio should be recognized by the ASR from the first place. 
"""

import numpy as np
from SpeechRecognitionAPI import Recognizer
from SegmentPerturbAPI import perturb_feedback_random


recognizer = Recognizer()
target_model = "google"
recognizer.set_model(target_model)
perturb_mode = "delete"

fn = "open the door"
#correct_list =  [fn, "call one one two five six seven nine eight", "call 1 one two five six seven nine" ]
#correct_list = [fn, "call two eight nine three eight five one four one four"]
#correct_list = [fn, "turn on airplane mode", "call nine one one", "turn on the light"]
correct_list = [fn, "turn on wireless hotspot", "turn on wi-fi", "call nine one one", "turn on the lights"]

Experiment_folder = "AudioSamples\\Experiment1_SoundSample\\sound1\\"
Attack_folder = "AudioSamples\\Experiment1_SoundSample\\attack1\\"

framerate = recognizer.read_parameter(Experiment_folder + fn + ".wav")
wave_form = recognizer.read_wave_form(Experiment_folder + fn + ".wav")

(wave_form_perturb, perturb_rate) = perturb_feedback_random(wave_form, correct_list, recognizer, \
                                            mode ="efficiency", 
                                            perturb_mode = perturb_mode, 
                                            medium = "air")
    
recognizer.write_wavfile(wave_form_perturb, Attack_folder + fn + "_" \
                          + target_model + "_" + perturb_mode + "_" + str(perturb_rate)[2:] + ".wav" )


#%%

# import numpy as np
# from SpeechRecognitionAPI import Recognizer
# from WrodPerturbationAPI import perturb_feedback_random


# #1 do perturbation seperately

# recognizer = Recognizer()

# target_model = "google"
# recognizer.set_model(target_model)

# wave_form_list = []
# file_name_list = [ "open the door"]

# Experiment_folder = "AudioSamples\\Experiment1_SoundSample\\"
# Attack_folder = "AudioSamples\\Experiment1_AttackSample\\"

# for fn in file_name_list:
#     framerate = recognizer.read_parameter(Experiment_folder + fn + ".wav")
#     wave_form = recognizer.read_wave_form(Experiment_folder + fn + ".wav")
#     #result = recognizer.transcribe(wave_form)
#     wave_form_perturb = perturb_feedback_random(wave_form, [fn,"open the doors" ], recognizer)
#     wave_form_list.append(wave_form_perturb)
#     recognizer.write_wavfile(wave_form_perturb, Attack_folder + fn + "_" + target_model + ".wav" )


#%% 2 concatenate
    
# concancate_wave = np.array([0, 0])

# for wave_form_elem in wave_form_list:
#     concancate_wave = np.concatenate((concancate_wave, wave_form_elem)).astype("int16")
#     # recognizer parameter is the last one (not respond). 

# recognizer = Recognizer()
# recognizer.read_parameter("AudioSamples\\SoundSample\\pay.wav")

# recognizer.write_wavfile(concancate_wave, "AudioSamples\\AttackSample\\pay money.wav" )
# recognizer.transcribe(concancate_wave)


