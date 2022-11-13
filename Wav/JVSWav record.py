from posixpath import dirname
import sounddevice as sd
import scipy.io.wavfile as spy
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

output = dirname
fs = 44100  # Sample rate
seconds = 30  # Duration of recording

# Record the audio
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

# Audio Cleanup
mu, sigma = 0, 500
x = np.arange(1, 100, 0.1)  # x axis
z = np.random.normal(mu, sigma, len(x))  # noise
y = x ** 2 + z # data
plt.plot(x, y, linewidth=2, linestyle="-", c="b")  # it include some noise
w = savgol_filter(y, 101, 2)
plt.plot(x, w, 'b')  # high frequency noise removed

sd.wait()  # Wait until recording is finished
spy.write('Recording.wav', fs, myrecording)  # Save as WAV file 
