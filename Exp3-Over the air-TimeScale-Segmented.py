# -*- coding: utf-8 -*-
"""
Created on Mon May 18 22:21:03 2020

@author: wang_
"""

import numpy as np
from SpeechRecognitionAPI import Recognizer
from PerturbationAPI import perturb_time_scale, perturb_fine_tune


recognizer = Recognizer()

target_model = "azure"
recognizer.set_model(target_model)

perturb_function = "delete"

fn = "turn on the light"
correct_result_list = [fn, "turn on the lights"]

Experiment_folder = "AudioSamples\\Experiment3_SoundSample\\sound1\\"
Attack_folder = "AudioSamples\\Experiment3_SoundSample\\attack1\\"

framerate = recognizer.read_parameter(Experiment_folder + fn + ".wav")
wave_form = recognizer.read_wave_form(Experiment_folder + fn + ".wav")


wave_form_perturb1 = perturb_time_scale(wave_form, correct_result_list, recognizer)
wave_form_perturb2, info = perturb_fine_tune(wave_form_perturb1, correct_result_list, recognizer)

print("the perturbation rate is " + str(info[0]))
recognizer.write_wavfile(wave_form_perturb2, Attack_folder + fn + "_" \
                         + target_model + "_" + "line_time_scale_fine_tune" + ".wav" )


