# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 17:00:15 2021

@author: Ganyu Wang 


"""

import numpy as np
from SpeechRecognitionAPI import Recognizer
from PerturbationAPI import perturb_time_scale, perturb_fine_tune

import math
import scipy as sc
from scipy.io import wavfile
from scipy import fft

import ffmpy

#%% TDI

#Time Domain Interval Attack (#1 in paper)
def TDIAttack(type, inputPath, outputPath, windowSize):
    fs, data = wavfile.read(inputPath)
    n = int(len(data)/windowSize)

    #Breaks array into buckets of elements
    #Each bucket has 'windowSize' amount of elements
    def createBuckets(arr, n):
        length = len(arr)
        return [ arr[i*length // n: (i+1)*length // n] 
                 for i in range(n) ]

    #Load audio file
    arr = np.copy(data)
    
    #Store split array into variable
    splitArray = createBuckets(arr,n)

    l = list()

    for x in splitArray[:n]:
        l.extend(np.fliplr([x])[0])
    
    #Stores the modified array and casts it as int
    data2 = np.asanyarray(l)
    data2= np.asarray(data2,dtype=np.int16)
    
    #new_audio_path = path[0:-4]+''+str(fs)+'_TDI_WindowSize_'+str(windowSize)+'.wav'

    wavfile.write(outputPath, fs, data2)

#%% RPG

#Random Phase Generation Attack (Attack #2 in paper)
def scramble_fft(ok_frame):
    ok_fft = np.abs(fft.fft(ok_frame))[0:int(len(ok_frame)/2+1)] #fft 
    
    new_ok = np.zeros_like(fft.fft(ok_frame))[0:int(len(ok_frame)/2+1)] #fft
    
    i = 0
    while(True):
    #     print("index ",i)
        if(i>=ok_fft.shape[0]):
            break
        ok_fft_val = ok_fft[i]
        new_ok_val = findExample(ok_fft_val)
        if(np.equal(np.abs(new_ok_val),ok_fft[i])):
            new_ok[i] = new_ok_val
            i += 1
        else:
            continue

    new_ok_long = half_to_full(new_ok)
    new_ok_long = sc.ifft(new_ok_long)
    new_ok_long = throw_imaginary(new_ok_long)
    return new_ok_long

            
def throw_imaginary(fft_arr):
    result = np.zeros(len(fft_arr))
    for i in range(fft_arr.shape[0]):
        result[i] = fft_arr[i].real
    return result


def half_to_full(new):
    new_1 = new
    new_2 = np.delete(new_1, len(new_1)-1)
    new_2 = np.delete(new_2, 0)

    new_flp = np.append(new_1,np.flip(new_2,0))

    for i in range(1,int(len(new_flp)/2)):

        index_read = int(len(new_flp)/2-i)
        index_write = int(len(new_flp)/2+i)

        real = new_flp[index_read].real
        imag = new_flp[index_read].imag
        new_flp[index_write] = real-imag*1j

    return new_flp

            
def findExample(ok_fft_val):
    phase_angle = np.random.rand()*2
    phase_radians = math.pi*phase_angle
    real_part = math.sin(phase_radians)*ok_fft_val
    imag_part = math.cos(phase_radians)*ok_fft_val
    assert((real_part*real_part + imag_part*imag_part)**0.5-ok_fft_val < .0001)
    result = (real_part + imag_part*1j)
    radian_list = [0] * 25
    radian_list[int(phase_angle*25/2)] += 1
    return result


def createBuckets(arr, n):
        length = len(arr)
        return [ arr[i*length // n: (i+1)*length // n] 
                 for i in range(n) ]


### Main RPG Attack Function ###
def output_RPG_Attack(attack, inputPath, outputPath, windowSize):
    
    #Read in the amplitude of the audio file
    fs, data = wavfile.read(inputPath)

    windowSize = windowSize
    n = int(len(data)/windowSize)
    arr = np.copy(data)

    #Store split array into variable
    splitArray = createBuckets(arr,n)

    l = list()

    #Run scramble_fft over window size
    for x in splitArray[:n]:
        l.extend(scramble_fft(x))

    data2 = np.asanyarray(l)
    data2= np.asarray(data2,dtype=np.int16)
    wavfile.write(outputPath, fs, data2)
    
    
#%% TS

#Time Scaling Attack (#4 in paper)
def TimeScaling(type, inputWav, outputWav, tempo):
    
    # have to download the FFMPEG from ffmpeg.org and specific the exe path. 
    ff = ffmpy.FFmpeg(executable='D:\\WorkSpace\\AudioAdversarialAttack\\ffmpeg\\bin\\ffmpeg.exe', 
                      inputs={inputWav: None}, 
                      outputs={outputWav: ["-filter:a", "atempo=1.5"]})
    ff.run()
    
#%% HFA

#High Frequency Addition Attack (#3 in paper)
def HFA(type, inputPath, outputPath, frequency, intensity):
    fs, data = wavfile.read(inputPath)
    length = len(data)
    
    #2. Generates a high frequency sin wave
    #Allows the sine wave to be broadcastable to the audio file we are testing
    sampleRate = fs #give it the same sample rate as the original audio
    frequency = frequency
    duration = length/sampleRate #how long the audio sound is in seconds  #4.52


    t = np.linspace(0, duration, length)  #  Produces a 'duration' long Audio-File in seconds
    y = np.sin(frequency * 2 * np.pi * t) * (intensity)  #Use to control the intensity of the sin wave

    #Uncomment the below line if you want to listen to the sin wave that you have produced from the above line
    #scipy.io.wavfile.write(path[0:-4]+''+'_SINEwav_Frequency'+''+str(fs)+'_Intensity'+str(intensity)+'.wav', sampleRate, y)
    #plt.plot(y)
    #print("This is the length of the sin sound wave:",len(y))

    #3. Merges the sine wave high frequency with the original piece of audio
    resultSound = np.add(data[:length] , y[:length] )

    #4. Casts the result sound from a float to an int
    resultSound = np.asarray(resultSound,dtype=np.int16)
    #print(resultSound)

    #5. Writes the audio file and then transcribes it 
    #new_audio_path = path[0:-4]+''+'_OutputWav_Frequency'+''+str(fs)+'_Intensity'+str(intensity)+'.wav'
    wavfile.write(outputPath, sampleRate, resultSound)



#%% 
command_dict = {1: "turn on airplane mode",
                2: "open the door",
                3: "turn on the computer",
                4: "turn on the light",
                5: "call 911",
                6: "turn on wifi",
                7: "turn on wireless hotspot" # deleted
                }

fn = command_dict[3]


basic_path = "AudioSamples/Experiment7_comprison/%s.wav"
input_path = basic_path % fn

# TDI attack 
# attack_type = "TDI"
# output_path_TDI = basic_path % ("%s_%s" % (fn, attack_type+"_N")) 
# window_size = 180
# TDIAttack(attack_type , input_path, output_path_TDI, window_size)
# print("TDI done")

# RPG attack
# attack_type = "RPG"
# output_path_RPG = basic_path % ("%s_%s" % (fn, attack_type)) 
# window_size = 500
# output_RPG_Attack(attack_type, input_path, output_path_RPG, window_size)
# print("RPG done")

# attack_type = "HFA"
# output_path_HFA = basic_path % ("%s_%s" % (fn, attack_type)) 
# frequency = 11000.
# intensity = 20000.
# HFA(attack_type, input_path, output_path_HFA, frequency, intensity)
# print("HFA done")

attack_type = "TS"
output_path_TS = basic_path % ("%s_%s" % (fn, attack_type))
tempo = 1.5
TimeScaling(attack_type, input_path, output_path_TS, tempo)
print("TS done")


recognizer = Recognizer()
target_model = "google"
recognizer.set_model(target_model)
recognizer.set_framerate(48000)

test_file_path = output_path_TS
wave_form = recognizer.read_wave_form(test_file_path)
frame_rate = recognizer.read_parameter(test_file_path)
result = recognizer.transcribe(wave_form)
print(result)




#%%

'''
fn = "turn on the computer"

basic_path = "AudioSamples/Experiment7_comprison/%s.wav"
input_path = basic_path % fn

# TDI attack 
attack_type = "TDI"
output_path_TDI = basic_path % ("%s_%s" % (fn, attack_type)) 
window_size = 20
TDIAttack(attack_type , input_path, output_path_TDI, window_size)
print("TDI done")

# RPG attack
attack_type = "RPG"
output_path_RPG = basic_path % ("%s_%s" % (fn, attack_type)) 
window_size = 500
output_RPG_Attack(attack_type, input_path, output_path_RPG, window_size)
print("RPG done")

# HFA attack 
attack_type = "HFA"
output_path_HFA = basic_path % ("%s_%s" % (fn, attack_type)) 
frequency = 11000.
intensity = 500.
HFA(attack_type, input_path, output_path_HFA, frequency, intensity)
print("HFA done")

# TS attack
attack_type = "TS"
output_path_TS = basic_path % ("%s_%s" % (fn, attack_type))
tempo = 1.5
TimeScaling(attack_type, input_path, output_path_TS, tempo)
print("TS done")


#%% Recognizer
recognizer = Recognizer()

target_model = "google"

recognizer.set_model(target_model)
recognizer.set_framerate(48000)

for output_path in [output_path_TDI, output_path_RPG, output_path_TS, output_path_HFA]:
    test_file_path = output_path
    wave_form = recognizer.read_wave_form(test_file_path)
    result = recognizer.transcribe(wave_form)
    print(output_path[-7:])
    print(result)

'''
#%%



