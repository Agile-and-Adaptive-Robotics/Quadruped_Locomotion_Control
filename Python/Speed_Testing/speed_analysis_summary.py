import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.signal import find_peaks

#####################################################
#####################################################
################ ALL CONNECTIONS ####################
#####################################################
#####################################################

R_hip_joint_ext_muscle_index = 0
R_hip_joint_flx_muscle_index = 1
R_knee_joint_ext_muscle_index = 2
R_knee_joint_flx_muscle_index = 3
R_ankle_joint_ext_muscle_index = 4
R_ankle_joint_flx_muscle_index = 5
L_hip_joint_ext_muscle_index = 12
L_hip_joint_flx_muscle_index = 13
L_knee_joint_ext_muscle_index = 14
L_knee_joint_flx_muscle_index = 15
L_ankle_joint_ext_muscle_index = 16
L_ankle_joint_flx_muscle_index = 17
R_scapula_joint_ext_muscle_index = 24
R_scapula_joint_flx_muscle_index = 25
R_shoulder_joint_ext_muscle_index = 26
R_shoulder_joint_flx_muscle_index = 27
R_wrist_joint_ext_muscle_index = 28
R_wrist_joint_flx_muscle_index = 29
L_scapula_joint_ext_muscle_index = 36
L_scapula_joint_flx_muscle_index = 37
L_shoulder_joint_ext_muscle_index = 38
L_shoulder_joint_flx_muscle_index = 39
L_wrist_joint_ext_muscle_index = 40
L_wrist_joint_flx_muscle_index = 41

R_hip_joint_ext_muscle_index_spk =  0
R_hip_joint_flx_muscle_index_spk =  1
R_knee_joint_ext_muscle_index_spk =  2   
R_knee_joint_flx_muscle_index_spk =   3  
R_ankle_joint_ext_muscle_index_spk =   4 
R_ankle_joint_flx_muscle_index_spk = 5
L_hip_joint_ext_muscle_index_spk = 6 
L_hip_joint_flx_muscle_index_spk =  7
L_knee_joint_ext_muscle_index_spk =  8   
L_knee_joint_flx_muscle_index_spk =   9  
L_ankle_joint_ext_muscle_index_spk =   10 
L_ankle_joint_flx_muscle_index_spk =    11
R_scapula_joint_ext_muscle_index_spk =  12
R_scapula_joint_flx_muscle_index_spk =  13
R_shoulder_joint_ext_muscle_index_spk =   14  
R_shoulder_joint_flx_muscle_index_spk =     15
R_wrist_joint_ext_muscle_index_spk =    16
R_wrist_joint_flx_muscle_index_spk =    17
L_scapula_joint_ext_muscle_index_spk =  18
L_scapula_joint_flx_muscle_index_spk =  19
L_shoulder_joint_ext_muscle_index_spk =   20  
L_shoulder_joint_flx_muscle_index_spk =     21
L_wrist_joint_ext_muscle_index_spk =    22
L_wrist_joint_flx_muscle_index_spk =    23


# Joint Angle

fast_time_path_004 = Path(r"Python\Speed_Testing\004\Fast\comm_times.npy")
fast_angle_path_004 = Path(r"Python\Speed_Testing\004\Fast\joint_ang.npy")
fast_MN_Activations_path_004 = Path(r"Python\Speed_Testing\004\Fast\nonspk_data.npy")

fast_time_004 = np.load(fast_time_path_004, allow_pickle=True)
fast_MN_Activations_004 = np.load(fast_MN_Activations_path_004, allow_pickle=True)

# Indexed, dictionary-like data
fast_angle_004 = np.load(fast_angle_path_004, allow_pickle=True).item()

medium_time_path_004 = Path(r"Python\Speed_Testing\004\Medium\comm_times.npy")
medium_angle_path_004 = Path(r"Python\Speed_Testing\004\Medium\joint_ang.npy")
medium_MN_Activations_path_004 = Path(r"Python\Speed_Testing\004\Medium\nonspk_data.npy")

medium_time_004 = np.load(medium_time_path_004, allow_pickle=True)
medium_MN_Activations_004 = np.load(medium_MN_Activations_path_004, allow_pickle=True)

# Indexed, dictionary-like data
medium_angle_004 = np.load(medium_angle_path_004, allow_pickle=True).item()

slow_time_path_004 = Path(r"Python\Speed_Testing\004\Slow\comm_times.npy")
slow_angle_path_004 = Path(r"Python\Speed_Testing\004\Slow\joint_ang.npy")
slow_MN_Activations_path_004 = Path(r"Python\Speed_Testing\004\Slow\nonspk_data.npy")

slow_time_004 = np.load(slow_time_path_004, allow_pickle=True)
slow_MN_Activations_004 = np.load(slow_MN_Activations_path_004, allow_pickle=True)

# Indexed, dictionary-like data
slow_angle_004 = np.load(slow_angle_path_004, allow_pickle=True).item()

################################

fast_time_path_005 = Path(r"Python\Speed_Testing\005\Fast\comm_times.npy")
fast_angle_path_005 = Path(r"Python\Speed_Testing\005\Fast\joint_ang.npy")
fast_MN_Activations_path_005 = Path(r"Python\Speed_Testing\005\Fast\nonspk_data.npy")

fast_time_005 = np.load(fast_time_path_005, allow_pickle=True)
fast_MN_Activations_005 = np.load(fast_MN_Activations_path_005, allow_pickle=True)

# Indexed, dictionary-like data
fast_angle_005 = np.load(fast_angle_path_005, allow_pickle=True).item()

medium_time_path_005 = Path(r"Python\Speed_Testing\005\Medium\comm_times.npy")
medium_angle_path_005 = Path(r"Python\Speed_Testing\005\Medium\joint_ang.npy")
medium_MN_Activations_path_005 = Path(r"Python\Speed_Testing\005\Medium\nonspk_data.npy")

medium_time_005 = np.load(medium_time_path_005, allow_pickle=True)
medium_MN_Activations_005 = np.load(medium_MN_Activations_path_005, allow_pickle=True)

# Indexed, dictionary-like data
medium_angle_005 = np.load(medium_angle_path_005, allow_pickle=True).item()

slow_time_path_005 = Path(r"Python\Speed_Testing\005\Slow\comm_times.npy")
slow_angle_path_005 = Path(r"Python\Speed_Testing\005\Slow\joint_ang.npy")
slow_MN_Activations_path_005 = Path(r"Python\Speed_Testing\005\Slow\nonspk_data.npy")

slow_time_005 = np.load(slow_time_path_005, allow_pickle=True)
slow_MN_Activations_005 = np.load(slow_MN_Activations_path_005, allow_pickle=True)

# Indexed, dictionary-like data
slow_angle_005 = np.load(slow_angle_path_005, allow_pickle=True).item()



###################

fast_time_path_006 = Path(r"Python\Speed_Testing\006\Fast\comm_times.npy")
fast_angle_path_006 = Path(r"Python\Speed_Testing\006\Fast\joint_ang.npy")
fast_MN_Activations_path_006 = Path(r"Python\Speed_Testing\006\Fast\nonspk_data.npy")

fast_time_006 = np.load(fast_time_path_006, allow_pickle=True)
fast_MN_Activations_006 = np.load(fast_MN_Activations_path_006, allow_pickle=True)

# Indexed, dictionary-like data
fast_angle_006 = np.load(fast_angle_path_006, allow_pickle=True).item()

medium_time_path_006 = Path(r"Python\Speed_Testing\006\Medium\comm_times.npy")
medium_angle_path_006 = Path(r"Python\Speed_Testing\006\Medium\joint_ang.npy")
medium_MN_Activations_path_006 = Path(r"Python\Speed_Testing\006\Medium\nonspk_data.npy")

medium_time_006 = np.load(medium_time_path_006, allow_pickle=True)
medium_MN_Activations_006 = np.load(medium_MN_Activations_path_006, allow_pickle=True)

# Indexed, dictionary-like data
medium_angle_006 = np.load(medium_angle_path_006, allow_pickle=True).item()

slow_time_path_006 = Path(r"Python\Speed_Testing\006\Slow\comm_times.npy")
slow_angle_path_006 = Path(r"Python\Speed_Testing\006\Slow\joint_ang.npy")
slow_MN_Activations_path_006 = Path(r"Python\Speed_Testing\006\Slow\nonspk_data.npy")

slow_time_006 = np.load(slow_time_path_006, allow_pickle=True)
slow_MN_Activations_006 = np.load(slow_MN_Activations_path_006, allow_pickle=True)

# Indexed, dictionary-like data
slow_angle_006 = np.load(slow_angle_path_006, allow_pickle=True).item()



# plt.figure() 
fig, axs = plt.subplots(1, 3, figsize=(26, 8))

fast_colour = 'green'
medium_colour = 'purple'
slow_colour = 'k'

fast_offset_005 = 0
medium_offset_005 = 0
slow_offset_005 = 0

fast_offset_004 = 0
medium_offset_004 = 100
slow_offset_004 = 200

# ---- Extract signals ----
fast_signal   = fast_MN_Activations_006[2000:, L_hip_joint_ext_muscle_index]
medium_signal = medium_MN_Activations_006[2000:, L_hip_joint_ext_muscle_index]
slow_signal   = slow_MN_Activations_006[2000:, L_hip_joint_ext_muscle_index]

# ---- Define sampling frequency (Hz) ----
fs = 1000  # replace with your actual sampling rate

# ---- FFT function ----
def compute_fft(signal, fs):
    N = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(N, d=1/fs)
    return fft_freqs[:N//2], np.abs(fft_vals[:N//2])

# ---- Compute FFTs ----
freq_fast, mag_fast     = compute_fft(fast_signal, fs)
freq_medium, mag_medium = compute_fft(medium_signal, fs)
freq_slow, mag_slow     = compute_fft(slow_signal, fs)

linew = 4

plt.subplots_adjust(
    # left=0.1,    # the left side of the subplots of the figure
    # right=0.9,   # the right side of the subplots of the figure
    # bottom=0.1,  # the bottom of the subplots of the figure
    # top=0.9,     # the top of the subplots of the figure
    wspace=0.1,  # the amount of width reserved for blank space between subplots
    # hspace=0.1   # the amount of height reserved for white space between subplots
)

axs[0].plot(fast_time_004 + fast_offset_004, fast_angle_004['R_hip_joint']*360/np.pi, color=fast_colour, label='L angle', lw = linew)
axs[0].plot(medium_time_004 + medium_offset_004, medium_angle_004['R_hip_joint']*360/np.pi, color=medium_colour, label='R angle', lw = linew)
axs[0].plot(slow_time_004 + slow_offset_004, slow_angle_004['R_hip_joint']*360/np.pi, color=slow_colour, label='R angle', lw = linew)
axs[0].set_title(r'$Joint~Angle~(\degree)$', fontsize = 26) 
axs[1].plot(fast_time_005 + fast_offset_005, fast_MN_Activations_005[::20, L_hip_joint_ext_muscle_index], color=fast_colour, label='L activation', lw = linew)
axs[1].plot(medium_time_005 + medium_offset_005, medium_MN_Activations_005[::20, L_hip_joint_ext_muscle_index], color=medium_colour, label='R activation', lw = linew)
axs[1].plot(slow_time_005 + slow_offset_005, slow_MN_Activations_005[::20, L_hip_joint_ext_muscle_index], color=slow_colour, label='R activation', lw = linew)
axs[1].set_title(r'$Extensor~Activation~(nV)$', fontsize = 26)
axs[2].plot(freq_fast, mag_fast, color = fast_colour, label=r'$Fast$', lw = linew)
axs[2].plot(freq_medium, mag_medium, color=medium_colour, label=r'$Medium$', lw = linew)
axs[2].plot(freq_slow, mag_slow, color=slow_colour, label=r'$Slow$', lw = linew)
axs[2].set_title(r'$FFT$', fontsize = 26)

axs[0].set_xlim(8000,10000)
axs[1].set_xlim(8000,10000)
axs[2].set_xlim(0.1,4)

axs[0].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'], fontsize = 26)
axs[1].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'], fontsize = 26)
axs[0].set_yticks([], labels=[])
axs[1].set_yticks([], labels=[])
axs[2].set_yticks([], labels=[])
axs[2].tick_params(axis='x', labelsize=26)
# axs[0, 2].set_xticks([8000, 9000, 10000], labels=[])

axs[0].set_ylim(-45,80)
axs[1].set_ylim(-105,-45)
axs[2].set_ylim(0, 0.1e6)

axs[2].legend(loc='upper right', fontsize = 26)

# axs[0].set_ylabel(r"$Joint~Angle~(\degree)$")
# axs[1].set_ylabel(r"$Extensor~Activation~(nV)$")

axs[0].set_xlabel(r"$Time~(s)$", fontsize = 26)
axs[1].set_xlabel(r"$Time~(s)$", fontsize = 26)
axs[2].set_xlabel(r"$Frequency~(Hz)$", fontsize = 26)

# for ax in axs:
#     ax.tick_params(axis='y', labelleft=False)
#     ax.grid(True, which='major', linestyle='-', alpha=0.9)

plt.savefig(r"Python\Speed_Testing\speed_summary.svg", format = 'svg', bbox_inches = 'tight')
plt.show()

print("Done")
