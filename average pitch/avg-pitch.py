'''
Created on 2017/06/22
'''
# -*- cording: utf-8 -*-

import wave
from pylab import *
import numpy as np
from scipy import signal

filename = '../t2.wav'

wf = wave.open(filename,'r')
channels = wf.getnchannels()
print(wf.getparams())

fs = wf.getframerate()
nyq = fs / 2.0
fe1 = 1000.0 / nyq
fe2 = 3000.0 / nyq
numtaps = 255
bit = wf.getsampwidth()

data = wf.readframes(wf.getnframes())
data = np.frombuffer(data,'int16')/32768.0

wf.close()

start = 8192
N = 512

b = signal.firwin(numtaps, fe2)
y = signal.lfilter(b,1,data)

dt1 = np.fft.fft(data[10000:10000 + N])
frq1 =np.fft.fftfreq(N, d=1.0/ fs)

dt2 = np.fft.fft(y[10000:10000 + N])
frq2 =np.fft.fftfreq(N, d=1.0/ fs)

amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in dt1]
phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in dt1]

amplitudeSpectrum2 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in dt2]
phaseSpectrum2 = [np.arctan2(int(c.imag), int(c.real)) for c in dt2]



wf = wave.open('./fft.wav','w')
wf.setnchannels(1)
wf.setsampwidth(bit)
wf.setframerate(fs)
wf.writeframes(dt2)
wf.close()


cor = signal.correlate(y[start:start+N],y[start:start+N],mode="full")
cor = cor[cor.size/2:]
i = 0.0
print cor.size
while cor[i] > cor[i+1]:
    i+=1
while cor[i] < cor[i+1]:
    i+=1
peak_index = i

print peak_index

freq = 1.0 / peak_index *fs/2

print freq

subplot(611)
plot(range(start, start+N), data[start:start+N])
axis([start, start+N, -1.0, 1.0])
xlabel("time [sample]")
ylabel("amplitude")


subplot(612)
plot(frq1, amplitudeSpectrum, marker= 'o', linestyle='-')
axis([0, fs/2, 0, 100])
xlabel("frequency [Hz]")
ylabel("amplitude\n spectrum")


subplot(613)
plot(frq1, phaseSpectrum, marker= 'o', linestyle='-')
axis([0, fs/2, -np.pi*2, np.pi*2])
xlabel("frequency [Hz]")
ylabel("phase\n spectrum")

subplot(614)
plot(range(start, start+N), y[start+128:start+128+N])
axis([start, start+N, -1.0, 1.0])
xlabel("time [sample]")
ylabel("amplitude")


subplot(615)
plot(frq2, amplitudeSpectrum2, marker= 'o', linestyle='-')
axis([0, fs/2, 0, 100])
xlabel("frequency [Hz]")
ylabel("amplitude\n spectrum")

subplot(616)
plot(frq2, phaseSpectrum2, marker= 'o', linestyle='-')
axis([0, fs/2, -np.pi*2, np.pi*2])
xlabel("frequency [Hz]")
ylabel("phase\n spectrum")
show()