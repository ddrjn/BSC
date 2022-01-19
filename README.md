# BSC
main code files for thesis and paper

## These files include the following:

> Openvocaturi files for emotion recognition (used for emotion retention during neutralization)

> pretrained wav2vec large network from facebook (need to download from sources)

> pretrained gender recognition classifier (finalized_model_big)

> python files for neutralization pipeline.

## How to run.

1. add your voice to this folder in wav format. lets say it has name "sound.wav"

2. run command `python3 neutralize_single.py --fn sound.wav`

after some while program will finish and neutralized voice will be saved in results folder as sound-neu.wav.
