# -*- coding: utf-8 -*-
from warnings import warn

import numpy as np
import pandas as pd
from neurokit2 import misc,signal
from neurokit2.misc import as_vector, NeuroKitWarning
from neurokit2.signal import signal_filter



def ppg_clean_v2(ppg_signal, sampling_rate=1000, heart_rate=None, method="elgendi", lowcut=0.5, highcut=8, order=3):
 
    ppg_signal = as_vector(ppg_signal)

    # Missing data
    n_missing = np.sum(np.isnan(ppg_signal))
    if n_missing > 0:
        warn(
            "There are " + str(n_missing) + " missing data points in your signal."
            " Filling missing values by using the forward filling method.",
            category=NeuroKitWarning
        )
        ppg_signal = _ppg_clean_missing(ppg_signal)

    method = method.lower()
    if method in ["elgendi"]:
        clean = _ppg_clean_elgendi(ppg_signal, sampling_rate,lowcut,highcut,order)
    else:
        raise ValueError("Neurokit error: Please use one of the following methods: 'elgendi' or 'nabian2018'.")

    return clean


# =============================================================================
# Handle missing data
# =============================================================================
def _ppg_clean_missing(ppg_signal):

    ppg_signal = pd.DataFrame.pad(pd.Series(ppg_signal))

    return ppg_signal

# =============================================================================
# Methods
# =============================================================================

def _ppg_clean_elgendi(ppg_signal, sampling_rate,lowcut,highcut,order):

    filtered = signal_filter(
        ppg_signal, sampling_rate=sampling_rate, lowcut=lowcut, highcut=highcut, order=order, method="butter_ba"
    )
    return filtered