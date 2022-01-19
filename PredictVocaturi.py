
import glob
import os
import sys
import scipy.io.wavfile
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd


sys.path.append("OpenVokaturi-3-4/api")


import Vokaturi


conf_mat = {
    'neutral':{
    'neutral':0,
    'angry':0,
    'happy':0,
    'fearful':0,
    'sad':0
},
    'angry':{
    'neutral':0,
    'angry':0,
    'happy':0,
    'fearful':0,
    'sad':0
},
    'happy':{
    'neutral':0,
    'angry':0,
    'happy':0,
    'fearful':0,
    'sad':0
},
    'fearful':{
    'neutral':0,
    'angry':0,
    'happy':0,
    'fearful':0,
    'sad':0
},
    'sad':{
    'neutral':0,
    'angry':0,
    'happy':0,
    'fearful':0,
    'sad':0
}
}

class PredictVoca():

    def __init__(self):
        Vokaturi.load("OpenVokaturi-3-4/lib/open/win/OpenVokaturi-3-4-win64.dll")
        print ("Analyzed by: %s" % Vokaturi.versionAndLicense())


    def argMax(self,probs):
        args = [probs.neutrality,probs.happiness,probs.sadness,probs.anger,probs.fear]
        maxi = max(args)
        if maxi == probs.neutrality:
            return "neutral"
        if maxi == probs.happiness:
            return "happy"
        if maxi == probs.sadness:
            return "sad"
        if maxi == probs.anger:
            return "angry"
        if maxi == probs.fear:
            return "fearful"
        
        return "none"

    def predict(self,file_name):
        (sample_rate, samples) = scipy.io.wavfile.read(file_name)
        buffer_length = len(samples)
        c_buffer = Vokaturi.SampleArrayC(buffer_length)
        c_buffer[:] = samples[:] / 32768.0
        voice = Vokaturi.Voice (sample_rate, buffer_length)
        voice.fill(buffer_length, c_buffer)
        quality = Vokaturi.Quality()
        emotionProbabilities = Vokaturi.EmotionProbabilities()
        voice.extract(quality, emotionProbabilities)
        if quality.valid:
            #print(argMax(emotionProbabilities))
            pred_ori = self.argMax(emotionProbabilities)
            return pred_ori
        return "none"


