import librosa
from librosa import feature
from librosa.feature.spectral import tonnetz
from matplotlib.pyplot import axis, cla
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
from sklearn.model_selection import GridSearchCV
from spafe.features.rplp import rplp, plp
from spafe.features.bfcc import bfcc
from spafe.frequencies.dominant_frequencies import get_dominant_frequencies
from spafe.frequencies.fundamental_frequencies import FundamentalFrequenciesExtractor
import wavencoder
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class Predictor:
    def __init__(self,modelName):
        self.modelName = modelName
        self.encoder = wavencoder.models.Wav2Vec(pretrained=True)
        self.model = pickle.load(open(self.modelName, 'rb'))
        #print(self.model.classes_)
    


    def predict(self,name):
        with soundfile.SoundFile(name) as sound_file:
            X = sound_file.read(dtype="float32")
            X = X.reshape(1,X.shape[0])
            x_torch = torch.tensor(X)
            z = self.encoder(x_torch)
            z = torch.mean(z, dim=2)
            feature = z[0,:].detach().numpy()

        x1 = [feature]
        mypred = self.model.predict_proba(x1)
        classes = self.model.classes_
        label = np.argmax(mypred, axis=1)
        
        return classes[label], mypred[0][0]*100,mypred[0][1]*100
       