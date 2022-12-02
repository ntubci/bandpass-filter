import matplotlib.pyplot as plt
from scipy import signal
import numpy as np


def bandpassfilter_cheby2_sos(bandFiltCutF, fs, filtAllowance=[0.2, 5]):
    '''
    Band-pass filter the EEG signal of one subject using cheby2 IIR filtering
    and implemented as a series of second-order filters with direct-form II transposed structure.
    Param:
        data: nparray, size [trials x channels x times], original EEG signal
        bandFiltCutF: list, len: 2, low and high cut off frequency (Hz).
                If any value is None then only one-side filtering is performed.
        fs: sampling frequency (Hz)
        filtAllowance: list, len: 2, transition bandwidth (Hz) of low-pass and high-pass f
        axis: the axis along which apply the filter.
    Returns:
        data_out: nparray, size [trials x channels x times], filtered EEG signal
    '''

    aStop = 40  # stopband attenuation
    aPass = 1  # passband attenuation
    nFreq = fs / 2  # Nyquist frequency

    # band-pass filter
    # print("Using bandpass filter")
    fPass = (np.array(bandFiltCutF) / nFreq).tolist()
    fStop = [(bandFiltCutF[0] - filtAllowance[0]) / nFreq,
             (bandFiltCutF[1] + filtAllowance[1]) / nFreq]
    # find the order
    [N, ws] = signal.cheb2ord(fPass, fStop, aPass, aStop)
    # sos = signal.cheby2(N, aStop, fStop, 'bandpass', output='sos')
    a, b = signal.cheby2(N, aStop, fStop, 'bandpass')

    # dataOut = signal.sosfilt(sos, data, axis=axis)

    return a, b


fs = 256
a, b = bandpassfilter_cheby2_sos([0.3, 40], fs, filtAllowance=[0.2, 5])
w, h = signal.freqz(b, a)

fig = plt.figure()
plt.title('Digital filter frequency response')

w = w*fs/(2*np.pi)

plt.plot(w, -20 * np.log10(abs(h)), 'b')
plt.ylabel('Amplitude [dB]')
plt.xlabel('Frequency [Hz]')

plt.grid()
plt.show()
