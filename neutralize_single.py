from ast import parse
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
from sklearn.model_selection import GridSearchCV
from spafe.features.rplp import rplp, plp
from spafe.features.bfcc import bfcc
from spafe.frequencies.dominant_frequencies import get_dominant_frequencies
from spafe.frequencies.fundamental_frequencies import FundamentalFrequenciesExtractor
from torch._C import dtype
import wavencoder
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from predictor import Predictor
import manipulationtoolkit as mpt
from neutralizer import Neutralizer
from scipy.io import wavfile
import argparse

parser = argparse.ArgumentParser(description='Input file name for sound to be neutralized')

parser.add_argument('--fn', type=str, required=True)

args = parser.parse_args()


myNeutralizer = Neutralizer("finalized_model-big.sav")

myNeutralizer.neutralize(args.fn,"results/{}-neu.wav".format(args.fn[0:-4]))