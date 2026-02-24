import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.signal import find_peaks

def plot_sns(time, data):
    """
    Plots a series of subplots for left and right side muscle activities using given time and data arrays.

    Plot left/right muscle activities for all limbs (SNS output).
    6x2 grid: each row = muscle group, columns = extensor/flexor.

    
                       Right Side
                       0 - hip mn ext
                       1 - hip mn flx
                       2 - knee mn ext
                       3 - knee mn flx
                       4 - ankle mn ext
                       5 - ankle mn flx
                       6 - RG ext
                       7 - RG flx
                       8 - hip PF ext
                       9 - hip PF flx
                       10- KA PF ext
                       11- KA PF flx

                       Left Side
                       12 - hip mn ext
                       13 - hip mn flx
                       14 - knee mn ext
                       15 - knee mn flx
                       16 - ankle mn ext
                       17 - ankle mn flx
                       18 - RG ext
                       19 - RG flx
                       20 - hip PF ext
                       21 - hip PF flx
                       22 - KA PF ext
                       23 - KA PF flx

                       ext = extensor
                       flx = flexor
                       mn = motor neuron
                       RG = rhythm generator
                       PF = pattern former
                       KA = knee ankle

    Returns:
    None
    """

    left_hind_indices =  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11]
    right_hind_indices = [12,13,14,15,16,17,18,19,20,21,22,23]
    left_fore_indices =  [24,25,26,27,28,29,30,31,32,33,34,35]
    right_fore_indices = [36,37,38,39,40,41,42,43,44,45,46,47]
    
    titles_hind = ["Hip MNs", "Knee MNs", "Ankle MNs", "Hind RG HCs", "Hip PF HCs", "KA PF HCs"]
    titles_fore = ["Scapula MNs", "Shoulder/Elbow MNs", "Wrist MNs", "Fore RG HCs", "Scapula PF HCs", "SW PF HCs"]

    plt.figure(figsize=(15, 20))
    for i in range(int(len(left_hind_indices)/2)):
        # Left side plots
        plt.subplot(6, 2, 2*i + 1)
        plt.plot(time, data[left_hind_indices[2*i]], label='ext_muscle', color='red')
        plt.plot(time, data[left_hind_indices[2*i+1]], label='flx_muscle', color='green')
        plt.title(f'Right {titles_hind[i]}')
        plt.legend()

        # Right side plots
        plt.subplot(6, 2, 2*i + 2)
        plt.plot(time, data[right_hind_indices[2*i]], label='ext_muscle', color='red')
        plt.plot(time, data[right_hind_indices[2*i+1]], label='flx_muscle', color='green')
        plt.title(f'Left {titles_hind[i]}')
        plt.legend()

    plt.tight_layout()

def plot_spk(time, data):
    """
    Plots a series of subplots for left and right side muscle activities using given time and data arrays.
    Plot left/right muscle activities for all limbs (spiking output).
    6x2 grid: each row = muscle group, columns = extensor/flexor.

                       Right Side
                       0 - hip mn ext
                       1 - hip mn flx
                       2 - knee mn ext
                       3 - knee mn flx
                       4 - ankle mn ext
                       5 - ankle mn flx

                       Left Side
                       6 - hip mn ext
                       7 - hip mn flx
                       8 - knee mn ext
                       9 - knee mn flx
                       10 - ankle mn ext
                       11 - ankle mn flx
                       
    Returns:
    None
    """
    
    left_hind_indices =  [0,  1,  2,  3,  4,  5 ]
    right_hind_indices = [6,  7,  8,  9,  10, 11]
    left_fore_indices =  [12, 13, 14, 15, 16, 17]
    right_fore_indices = [18, 19, 20, 21, 22, 23]
    titles_hind = ["Hip Spikerate", "Knee Spikerate", "Ankle Spikerate"]
    titles_fore = ["Scapula Spikerate", "Shoulder Spikerate", "Wrist Spikerate"]    


    ################### PLOT HINDLIMBS ###################
    plt.figure(figsize=(15, 10))
    
    for i in range(int(len(left_hind_indices)/2)):
    
        evens = 2*i

        ################## LEFT SIDE PLOTS ##################
        flx_spk_tms = np.where(data[left_hind_indices[evens+1]] == 1)[0]
        flx_spk_rts = np.zeros(len(flx_spk_tms)-1)
        for ii in range(len(flx_spk_rts)):
            flx_spk_rts[ii] = 1000 / (flx_spk_tms[ii+1] - flx_spk_tms[ii])

        ext_spk_tms = np.where(data[left_hind_indices[evens]] == 1)[0]
        ext_spk_rts = np.zeros(len(ext_spk_tms)-1)
        for ii in range(len(ext_spk_rts)):
            ext_spk_rts[ii] = 1000 / (ext_spk_tms[ii+1] - ext_spk_tms[ii])

        plt.subplot(3, 2, evens + 1)
        plt.plot(ext_spk_tms[1:], ext_spk_rts, label='ext_muscle', color='red', marker='o', linestyle='')
        plt.plot(flx_spk_tms[1:], flx_spk_rts, label='flx_muscle', color='green', marker='o', linestyle='')
        plt.title(f'Left {titles_hind[i]}')
        plt.legend()

        ################## RIGHT SIDE PLOTS ##################
        flx_spk_tms = np.where(data[right_hind_indices[evens+1]] == 1)[0]
        flx_spk_rts = np.zeros(len(flx_spk_tms)-1)
        for ii in range(len(flx_spk_rts)):
            flx_spk_rts[ii] = 1000 / (flx_spk_tms[ii+1] - flx_spk_tms[ii])

        ext_spk_tms = np.where(data[right_hind_indices[evens]] == 1)[0]
        ext_spk_rts = np.zeros(len(ext_spk_tms)-1)
        for ii in range(len(ext_spk_rts)):
            ext_spk_rts[ii] = 1000 / (ext_spk_tms[ii+1] - ext_spk_tms[ii])

        plt.subplot(3, 2, evens + 2)
        plt.plot(ext_spk_tms[1:], ext_spk_rts, label='ext_muscle', color='red', marker='o', linestyle='')
        plt.plot(flx_spk_tms[1:], flx_spk_rts, label='flx_muscle', color='green', marker='o', linestyle='')
        plt.title(f'Right {titles_hind[i]}')
        plt.legend()

    # plt.savefig('python/fig_plots/plot_spk_hindlimbs.png')


    ################### PLOT FORELIMBS ###################
    plt.figure(figsize=(15, 10))

    for i in range(int(len(left_fore_indices)/2)):
    
        evens = 2*i

        ################## LEFT SIDE PLOTS ##################
        ext_spk_tms = np.where(data[left_fore_indices[evens]] == 1)[0]
        ext_spk_rts = np.zeros(len(ext_spk_tms)-1)
        for ii in range(len(ext_spk_rts)):
            ext_spk_rts[ii] = 1000 / (ext_spk_tms[ii+1] - ext_spk_tms[ii])

        flx_spk_tms = np.where(data[left_fore_indices[evens+1]] == 1)[0]
        flx_spk_rts = np.zeros(len(flx_spk_tms)-1)
        for ii in range(len(flx_spk_rts)):
            flx_spk_rts[ii] = 1000 / (flx_spk_tms[ii+1] - flx_spk_tms[ii])

        plt.subplot(3, 2, evens + 1)
        plt.plot(ext_spk_tms[1:], ext_spk_rts, label='ext_muscle', color='red', marker='o', linestyle='')
        plt.plot(flx_spk_tms[1:], flx_spk_rts, label='flx_muscle', color='green', marker='o', linestyle='')
        plt.title(f'Left {titles_fore[i]}')
        plt.legend()

        ################## RIGHT SIDE PLOTS ##################
        ext_spk_tms = np.where(data[right_fore_indices[evens]] == 1)[0]
        ext_spk_rts = np.zeros(len(ext_spk_tms)-1)
        for ii in range(len(ext_spk_rts)):
            ext_spk_rts[ii] = 1000 / (ext_spk_tms[ii+1] - ext_spk_tms[ii])

        flx_spk_tms = np.where(data[right_fore_indices[evens+1]] == 1)[0]
        flx_spk_rts = np.zeros(len(flx_spk_tms)-1)
        for ii in range(len(flx_spk_rts)):
            flx_spk_rts[ii] = 1000 / (flx_spk_tms[ii+1] - flx_spk_tms[ii])

        plt.subplot(3, 2, evens + 2)
        plt.plot(ext_spk_tms[1:], ext_spk_rts, label='ext_muscle', color='red', marker='o', linestyle='')
        plt.plot(flx_spk_tms[1:], flx_spk_rts, label='flx_muscle', color='green', marker='o', linestyle='')
        plt.title(f'Right {titles_fore[i]}')
        plt.legend()

    # plt.savefig('python/fig_plots/plot_spk_forelimbs.png')

    print("... SPK plots created")


    plot_sns()