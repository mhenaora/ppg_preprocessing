#@title ppg_process_v2
# -*- coding: utf-8 -*-
import pandas as pd
import neurokit2 as nk
from neurokit2 import as_vector
from neurokit2 import signal_rate
from neurokit2.signal.signal_formatpeaks import _signal_from_indices
from neurokit2 import ppg_clean
#from ppg_clean_v2 import ppg_clean_v2
import ppg_findpeaks_v2
import ppg_clean_v2

def ppg_process_v2(ppg_signal, sampling_rate=1000,peakwindow=0.111, beatwindow=0.667, beatoffset=0.02, mindelay=0.3, **kwargs):

    # Sanitize input
    ppg_signal = as_vector(ppg_signal)

    # Clean signal
    ppg_cleaned = ppg_clean_v2(ppg_signal, sampling_rate=sampling_rate,lowcut=lowcut,highcut=highcut,order=order)

    # Find peaks
    info = ppg_findpeaks_v2(ppg_cleaned, sampling_rate=sampling_rate, peakwindow=peakwindow, beatwindow=beatwindow, beatoffset=beatoffset, mindelay=0.3, **kwargs)
    info['sampling_rate'] = sampling_rate  # Add sampling rate in dict info

    # Mark peaks
    peaks_signal = _signal_from_indices(info["PPG_Peaks"], desired_length=len(ppg_cleaned))

    # Rate computation
    rate = signal_rate(info["PPG_Peaks"], sampling_rate=sampling_rate, desired_length=len(ppg_cleaned))

    # Prepare output
    signals = pd.DataFrame(
        {"PPG_Raw": ppg_signal, "PPG_Clean": ppg_cleaned, "PPG_Rate": rate, "PPG_Peaks": peaks_signal}
    )

    return signals, info
