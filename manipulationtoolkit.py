from parselmouth.praat import call
import parselmouth



def scaleS(inputsound,outputsound):
    sound = parselmouth.Sound(inputsound)
    sound.scale_intensity(70)
    sound.name = outputsound
    sound.save(outputsound, "WAV")



def change(inputsound,outputsound,pitch_factor,formant_factor):
    sound = parselmouth.Sound(inputsound)
    sound.scale_intensity(70)
    pitch = sound.to_pitch()
    median_pitch = call(pitch, "Get quantile", sound.xmin, sound.xmax, 0.5, "Hertz")
    #new_pitch_median = pitch_factor * median_pitch
    new_pitch_median = pitch_factor
    manipulated_sound = call(
                sound,
                "Change gender",
                90,
                600,
                formant_factor,
                new_pitch_median,
                1,
                1,
            )

    manipulated_sound.scale_intensity(70)
    manipulated_sound.name = outputsound
    manipulated_sound.save(outputsound, "WAV")



def measure_pitch(
    voicename,
    floor=50,
    ceiling=600,
    method="To Pitch (cc)",
    time_step=0,
    max_number_of_candidates=15,
    silence_threshold=0.03,
    voicing_threshold=0.45,
    octave_cost=0.01,
    octave_jump_cost=0.35,
    voiced_unvoiced_cost=0.14,
    unit="Hertz",
    very_accurate="yes",
):
    #floor, ceiling = pitch_bounds(voice)

    """
    Args:
        voice:
        floor:
        ceiling:
        method:
        time_step:
        max_number_of_candidates:
        silence_threshold:
        voicing_threshold:
        octave_cost:
        octave_jump_cost:
        voiced_unvoiced_cost:
        unit:
        very_accurate:
    """

    voice  = parselmouth.Sound(voicename)
    pitch: object = call(
        voice,
        method,
        time_step,
        floor,
        max_number_of_candidates,
        very_accurate,
        silence_threshold,
        voicing_threshold,
        octave_cost,
        octave_jump_cost,
        voiced_unvoiced_cost,
        ceiling,
    )
    mean_f0: float = call(pitch, "Get mean", 0, 0, unit)
    stdev_f0: float = call(
        pitch, "Get standard deviation", 0, 0, unit
    )  # get standard deviation
    min_f0: float = call(pitch, "Get minimum", 0, 0, unit, "Parabolic")
    max_f0: float = call(pitch, "Get maximum", 0, 0, unit, "Parabolic")

    return pitch, mean_f0, stdev_f0, min_f0, max_f0


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()