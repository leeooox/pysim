import numpy as np
from scipy.signal import lfilter

def extract_phase(raw_period_seq,raw_period_seq_ref=None):
    period_seq = raw_period_seq[np.where(raw_period_seq)[0]]

    if raw_period_seq_ref is not None:
        period_seq2 = raw_period_seq_ref[np.where(raw_period_seq_ref)[0][:len(period_seq)]]
        avg_period = np.mean(period_seq2)
        phase = np.cumsum(period_seq-period_seq2)/avg_period
        
    else:
        avg_period = np.mean(period_seq)
        phase = np.cumsum(period_seq-avg_period)/avg_period     

    return phase,avg_period


