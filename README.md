# Bandpass Filter

Band-pass filter the EEG signal of one subject using cheby2 IIR filtering
and implemented as a series of second-order filters with direct-form II transposed structure.

## Parameters
    
- **data**: nparray, size [trials x channels x times], original EEG signal
- **bandFiltCutF**: list, len: 2, low and high cut off frequency (Hz), If any value is None then only one-side filtering is performed.
- **fs**: sampling frequency (Hz)
- **filtAllowance**: list, len: 2, transition bandwidth (Hz) of low-pass and high-pass f
- **axis**: the axis along which apply the filter.

## Returns

- **data_out**: nparray, size [trials x channels x times], filtered EEG signal

## Usage

```python
data_out = bandpassfilter_cheby2_sos(
  data, 
  bandFiltCutF=[0.3, 40], 
  fs=1000, 
  filtAllowance=[0.2, 5], 
  axis=2
)
```
