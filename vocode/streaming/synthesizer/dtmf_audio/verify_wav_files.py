# Adapted from https://github.com/alijamaliz/DTMF-detector

from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np

def isNumberInArray(array, number):
    offset = 5
    for i in range(number - offset, number + offset):
        if i in array:
            return True
    return False

DTMF_TABLE = {
    '1': [1209, 697],
    '2': [1336, 697],
    '3': [1477, 697],
    'A': [1633, 697],

    '4': [1209, 770],
    '5': [1336, 770],
    '6': [1477, 770],
    'B': [1633, 770],

    '7': [1209, 852],
    '8': [1336, 852],
    '9': [1477, 852],
    'C': [1633, 852],

    '*': [1209, 941],
    '0': [1336, 941],
    '#': [1477, 941],
    'D': [1633, 941],
} 

for key in DTMF_TABLE.keys():
    if key == '*':
        name = 'star'
    elif key == '#':
        name = 'pound'
    else:
        name = key

    # filename = "dtmf-%s.500ms.b16.wav" % name
    filename = "dtmf-%s.wav" % name
    print(filename)

    rate, data = wav.read(filename)

    # Calculate fourier trasform of data
    FourierTransformOfData = np.fft.fft(data, 20000)

    # Convert fourier transform complex number to integer numbers
    for i in range(len(FourierTransformOfData)):
        FourierTransformOfData[i] = int(np.absolute(FourierTransformOfData[i]))

    # Calculate lower bound for filtering fourier trasform numbers
    LowerBound = 20 * np.average(FourierTransformOfData)

    # Filter fourier transform data (only select frequencies that X(jw) is greater than LowerBound)
    FilteredFrequencies = []
    for i in range(len(FourierTransformOfData)):
        if (FourierTransformOfData[i] > LowerBound):
            FilteredFrequencies.append(i)

    # print(FilteredFrequencies)

    # Detect and print pressed button
    for char, frequency_pair in DTMF_TABLE.items():
        if (isNumberInArray(FilteredFrequencies, frequency_pair[0]) and
            isNumberInArray(FilteredFrequencies, frequency_pair[1])):
            print (char)
