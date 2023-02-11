import numpy as np
import scipy.signal as signal


def bandpassfilter_cheby2_sos(data, bandFiltCutF=[0.3, 40], fs=1000, filtAllowance=[0.2, 5], axis=2):
    '''
    Band-pass filter the EEG signal of one subject using cheby2 IIR filtering
    and implemented as a series of second-order filters with direct-form II transposed structure.
    Param:
        data: nparray, size [trials x channels x times], original EEG signal
        bandFiltCutF: list, len: 2, low and high cut off frequency (Hz),
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

    if (bandFiltCutF[0] == 0 or bandFiltCutF[0] is None) and (bandFiltCutF[1] == None or bandFiltCutF[1] >= fs / 2.0):
        # no filter
        print("Not doing any filtering. Invalid cut-off specifications")
        return data

    elif bandFiltCutF[0] == 0 or bandFiltCutF[0] is None:
        # low-pass filter
        print("Using lowpass filter since low cut hz is 0 or None")
        fPass = bandFiltCutF[1] / nFreq
        fStop = (bandFiltCutF[1] + filtAllowance[1]) / nFreq
        # find the order
        [N, ws] = signal.cheb2ord(fPass, fStop, aPass, aStop)
        sos = signal.cheby2(N, aStop, ws, 'lowpass', output='sos')

    elif (bandFiltCutF[1] is None) or (bandFiltCutF[1] == fs / 2.0):
        # high-pass filter
        print("Using highpass filter since high cut hz is None or nyquist freq")
        fPass = bandFiltCutF[0] / nFreq
        fStop = (bandFiltCutF[0] - filtAllowance[0]) / nFreq
        # find the order
        [N, ws] = signal.cheb2ord(fPass, fStop, aPass, aStop)
        sos = signal.cheby2(N, aStop, ws, 'highpass', output='sos')

    else:
        # band-pass filter
        # print("Using bandpass filter")
        fPass = (np.array(bandFiltCutF) / nFreq).tolist()
        fStop = [(bandFiltCutF[0] - filtAllowance[0]) / nFreq,
                 (bandFiltCutF[1] + filtAllowance[1]) / nFreq]
        # find the order
        [N, ws] = signal.cheb2ord(fPass, fStop, aPass, aStop)
        sos = signal.cheby2(N, aStop, ws, 'bandpass', output='sos')

    dataOut = signal.sosfilt(sos, data, axis=axis)

    return dataOut
