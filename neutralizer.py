
import librosa
from librosa import feature
from librosa.feature.spectral import tonnetz
from matplotlib.pyplot import axis, figure
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
import wavencoder
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from predictor import Predictor
import manipulationtoolkit as mpt
from PredictVocaturi import PredictVoca


class Neutralizer():

    def __init__(self,modelname):
        self.myPredictor = Predictor(modelname)
        self.voca = PredictVoca()


    #filename = "ravdess data/Actor_02/03-01-03-01-02-02-02.wav"

    def neutralize(self,fn,outputfilename):
        filename = fn
        print("initial result")
        initiallabel,female,male = self.myPredictor.predict(filename)
        print(initiallabel,female,male)
        initialEmotion = self.voca.predict(fn)
        print(initialEmotion)
        bestReuslt = [100,145,1]#min difference, pitch, formant factor



        if initiallabel == ["male"]:
            for pitch in range(120,200,5):
                for formantfactor in np.arange(1.05,1.20,0.01):
                    mpt.change(filename,"results/temp/temp.wav",pitch,formantfactor)
                    label,female,male = self.myPredictor.predict("results/temp/temp.wav")
                    #print (pitch,formantfactor,female,male)
                    emo = self.voca.predict("results/temp/temp.wav")
                    if abs(female-male)<20 :
                        if bestReuslt[0]>abs(female-male) and emo == initialEmotion:
                            bestReuslt[0]=abs(female-male)
                            bestReuslt[1] = pitch
                            bestReuslt[2] = formantfactor
                            break
        else:
            
            for pitch in range(120,200,5):
                for formantfactor in np.arange(0.79,1.00,0.01):
                    mpt.change(filename,"results/temp/temp.wav",pitch,formantfactor)
                    label,female,male = self.myPredictor.predict("results/temp/temp.wav")
                    #print (pitch,formantfactor,female,male)
                    emo = self.voca.predict("results/temp/temp.wav")
                    if abs(female-male)<20 :
                        if bestReuslt[0]>abs(female-male) and emo == initialEmotion:
                            bestReuslt[0]=abs(female-male)
                            bestReuslt[1] = pitch
                            bestReuslt[2] = formantfactor
                            break


        if bestReuslt[0]!=100:
            mpt.change(filename,outputfilename,bestReuslt[1],bestReuslt[2])
            print("found good match")
        #mpt.change(filename,"temp/good-{}-{}.wav".format(bestReuslt[1],bestReuslt[2]),bestReuslt[1],bestReuslt[2])
        else:
            if initiallabel == ["male"]:
                mpt.change(filename,outputfilename+"default.wav",155,1.07)
            else:
                mpt.change(filename,outputfilename+"default.wav",145,0.87)

        print(bestReuslt[0])