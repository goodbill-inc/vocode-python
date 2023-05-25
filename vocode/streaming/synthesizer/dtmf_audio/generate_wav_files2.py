import os
import numpy as np
import scipy.io.wavfile as wavfile

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

def generate_dtmf_tone(frequencies, duration, sample_rate):
    time = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    tone = sum(np.sin(2 * np.pi * freq * time) for freq in frequencies)
    return tone / np.max(np.abs(tone))

for key in DTMF_TABLE.keys():
    frequencies = DTMF_TABLE[key]

    if key == '*':
        name = 'star'
    elif key == '#':
        name = 'pound'
    else:
        name = key
    
    filename = "dtmf-%s.wav" % name
    duration = 0.5 # seconds
    sample_rate = 8000 # 44100 # Hz # TODO

    # Generate the DTMF tone
    dtmf_tone = generate_dtmf_tone(frequencies, duration, sample_rate)

    # Save the tone as a WAV file
    wavfile.write(filename, sample_rate, np.int16(dtmf_tone * 32767))

    # Convert to format expected by Twilio
    new_filename = filename.replace(".wav", ".8000hz.mulaw.wav")
    command = "sox %s -G -e mu-law %s" % (filename, new_filename)
    os.system(command)

    # Convert to format expected by Twilio
    new_filename = filename.replace(".wav", ".8000hz.mulaw.raw")
    command = "sox %s -G -e mu-law -t raw %s" % (filename, new_filename)
    os.system(command)
