import os
os.sys.path.append("../.")
import numpy as np
from scipy.io import loadmat
from pysim.Toolbox import extract_phase
import matplotlib.pyplot as plt


def test_case1():
    raw_period_vco = loadmat(r"test_data\raw_period_vco.mat")["raw_period_vco"].T[0]
    raw_period_in = loadmat(r"test_data\raw_period_in.mat")["raw_period_in"].T[0]
    #raw_period_seq_ref
    #print raw_period_seq
    phase,avg_period = extract_phase(raw_period_vco,raw_period_in)
    #phase,avg_period = extract_phase(raw_period_vco)

    plt.plot(phase,'-k')
    plt.grid()
    plt.xlabel("VCO rising edge number")
    plt.ylabel("Instantaneous Jitter (U.I.)")
    plt.title("Instantaneous Jitter of VCO in CDR: \n Steady-state RMS jitter = %5.4f mUI" %(1e3*np.std(phase[30000:])))
    plt.show()

def test_case2():
    raw_period_vco = np.load(r"test_data\linearCDR_vco_period.npy")
    raw_period_in  = np.load(r"test_data\linearCDR_in_period.npy")
    phase,avg_period = extract_phase(raw_period_vco,raw_period_in)
    #phase,avg_period = extract_phase(raw_period_vco)

    plt.plot(phase,'-k')
    plt.grid()
    plt.xlabel("VCO rising edge number")
    plt.ylabel("Instantaneous Jitter (U.I.)")
    plt.title("Instantaneous Jitter of VCO in CDR: \n Steady-state RMS jitter = %5.4f mUI" %(1e3*np.std(phase[30000:])))
    plt.show()





test_case2()
