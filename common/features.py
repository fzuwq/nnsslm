"""
features.py

Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/
Written by Weipeng He <weipeng.he@idiap.ch>
"""

import numpy as np

import apkit


class FeatureSTFT:
    def __init__(self, win_size, hop_size, min_freq=0, max_freq=-1):
        self.win_size = win_size
        self.hop_size = hop_size
        self.min_freq = min_freq
        self.max_freq = max_freq

    def __call__(self, fs, sig):
        tf = apkit.stft(sig,
                        apkit.cola_hamming,
                        self.win_size,
                        self.hop_size,
                        last_sample=True)
        min_fbin = int(self.min_freq * self.win_size // fs)
        if self.max_freq >= 0:
            max_fbin = int(self.max_freq * self.win_size // fs)
        else:
            max_fbin = int(self.win_size // 2)
        tf = tf[:, :, min_fbin:max_fbin]
        feat = np.concatenate((tf.real, tf.imag), axis=0)
        return feat.astype(np.float32, copy=False)


def pass_through(fs, sig):
    return fs, sig


class FeatureMelFbCcPower:
    """Cross-correlation and power on mel-freq filter banks"""
    def __init__(self,
                 win_size,
                 hop_size,
                 fs,
                 nfilters=40,
                 min_freq=0,
                 max_freq=-1):
        self.win_size = win_size
        self.hop_size = hop_size
        min_fbin = self.min_freq * self.win_size / fs
        if self.max_freq >= 0:
            max_fbin = self.max_freq * self.win_size / fs
        else:
            max_fbin = self.win_size / 2
        self.fs = fs
        self.freq = np.fft.fftfreq(win_size)[min_fbin:max_fbin]
        self.fbw = apkit.mel_freq_fbank_weight(nfilters,
                                               freq=self.freq,
                                               fs=fs,
                                               fmin=min_freq,
                                               fmax=max_freq)

    def __call__(self, fs, sig):
        assert self.fs == fs
        tf = apkit.stft(sig,
                        apkit.cola_hamming,
                        self.win_size,
                        self.hop_size,
                        last_sample=True)
        min_fbin = self.min_freq * self.win_size / fs
        if self.max_freq >= 0:
            max_fbin = self.max_freq * self.win_size / fs
        else:
            max_fbin = self.win_size / 2
        tf = tf[:, :, min_fbin:max_fbin]
        feat = np.concatenate((tf.real, tf.imag), axis=0)
        return feat


ALL = {'stft': FeatureSTFT}
