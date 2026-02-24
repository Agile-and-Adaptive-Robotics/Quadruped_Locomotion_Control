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


# time_path = Path("1_chapter/figures/results/data_Doggo/comm_times.npy")
# angle_path = Path("1_chapter/figures/results/data_Doggo/joint_ang.npy")
# length_path = Path("1_chapter/figures/results/data_Doggo/muscle_len.npy")
# MN_Activations_path = Path("1_chapter/figures/results/data_Doggo/SNS_sim_data.npy")
# SPK_Activations_path = Path("1_chapter/figures/results/data_Doggo/SNS_spk_data.npy")

fast_time_path = Path(r"Python\Speed_Testing\005\Fast\comm_times.npy")
fast_angle_path = Path(r"Python\Speed_Testing\005\Fast\joint_ang.npy")
fast_length_path = Path(r"Python\Speed_Testing\005\Fast\muscle_len.npy")
fast_MN_Activations_path = Path(r"Python\Speed_Testing\005\Fast\nonspk_data.npy")
fast_SPK_Activations_path = Path(r"Python\Speed_Testing\005\Fast\spk_data.npy")

fast_time = np.load(fast_time_path, allow_pickle=True)
fast_MN_Activations = np.load(fast_MN_Activations_path, allow_pickle=True)
fast_SPK_Activations = np.load(fast_SPK_Activations_path, allow_pickle=True)

# Indexed, dictionary-like data
fast_angle = np.load(fast_angle_path, allow_pickle=True).item()
fast_length = np.load(fast_length_path, allow_pickle=True).item()

medium_time_path = Path(r"Python\Speed_Testing\005\Medium\comm_times.npy")
medium_angle_path = Path(r"Python\Speed_Testing\005\Medium\joint_ang.npy")
medium_length_path = Path(r"Python\Speed_Testing\005\Medium\muscle_len.npy")
medium_MN_Activations_path = Path(r"Python\Speed_Testing\005\Medium\nonspk_data.npy")
medium_SPK_Activations_path = Path(r"Python\Speed_Testing\005\Medium\spk_data.npy")

medium_time = np.load(medium_time_path, allow_pickle=True)
medium_MN_Activations = np.load(medium_MN_Activations_path, allow_pickle=True)
medium_SPK_Activations = np.load(medium_SPK_Activations_path, allow_pickle=True)

# Indexed, dictionary-like data
medium_angle = np.load(medium_angle_path, allow_pickle=True).item()
medium_length = np.load(medium_length_path, allow_pickle=True).item()

slow_time_path = Path(r"Python\Speed_Testing\005\Slow\comm_times.npy")
slow_angle_path = Path(r"Python\Speed_Testing\005\Slow\joint_ang.npy")
slow_length_path = Path(r"Python\Speed_Testing\005\Slow\muscle_len.npy")
slow_MN_Activations_path = Path(r"Python\Speed_Testing\005\Slow\nonspk_data.npy")
slow_SPK_Activations_path = Path(r"Python\Speed_Testing\005\Slow\spk_data.npy")

slow_time = np.load(slow_time_path, allow_pickle=True)
slow_MN_Activations = np.load(slow_MN_Activations_path, allow_pickle=True)
slow_SPK_Activations = np.load(slow_SPK_Activations_path, allow_pickle=True)

# Indexed, dictionary-like data
slow_angle = np.load(slow_angle_path, allow_pickle=True).item()
slow_length = np.load(slow_length_path, allow_pickle=True).item()

# plt.figure() 
fig, axs = plt.subplots(4, 3, figsize=(8, 10))

left_colour = 'blue'
right_colour = 'red'
slow_colour = 'k'

fast_offset = 0
medium_offset= 0
slow_offset = 0

plt.subplots_adjust(
    # left=0.1,    # the left side of the subplots of the figure
    # right=0.9,   # the right side of the subplots of the figure
    # bottom=0.1,  # the bottom of the subplots of the figure
    # top=0.9,     # the top of the subplots of the figure
    wspace=0.1,  # the amount of width reserved for blank space between subplots
    hspace=0.1   # the amount of height reserved for white space between subplots
)


axs[0, 0].plot(fast_time + fast_offset, fast_angle['L_hip_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 0].plot(medium_time + medium_offset, medium_angle['L_hip_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 0].plot(slow_time + slow_offset, slow_angle['L_hip_joint']*360/np.pi, color=slow_colour, label='R angle')
axs[0, 0].set_title(r'$Left~Hip$') 
axs[0, 1].plot(fast_time + fast_offset, fast_angle['L_knee_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 1].plot(medium_time + medium_offset, medium_angle['L_knee_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 1].plot(slow_time + slow_offset, slow_angle['L_knee_joint']*360/np.pi, color=slow_colour, label='R angle')
axs[0, 1].set_title(r'$Left~Knee$')
axs[0, 2].plot(fast_time + fast_offset, fast_angle['L_ankle_joint']*360/np.pi, color=left_colour, label=r'$Fast$')
axs[0, 2].plot(medium_time + medium_offset, medium_angle['L_ankle_joint']*360/np.pi, color=right_colour, label=r'$Medium$')
axs[0, 2].plot(slow_time + slow_offset, slow_angle['L_ankle_joint']*360/np.pi, color=slow_colour, label=r'$Slow$')
axs[0, 2].set_title(r'$Left~Ankle$')

axs[1, 0].plot(fast_time + fast_offset, fast_MN_Activations[::20, L_hip_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 0].plot(medium_time + medium_offset, medium_MN_Activations[::20, L_hip_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[1, 0].plot(slow_time + slow_offset, slow_MN_Activations[::20, L_hip_joint_ext_muscle_index], color=slow_colour, label='R activation')
# axs[1, 0].set_title('Hip Ext MN Activations')
axs[1, 1].plot(fast_time + fast_offset, fast_MN_Activations[::20, L_knee_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 1].plot(medium_time + medium_offset, medium_MN_Activations[::20, L_knee_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[1, 1].plot(slow_time + slow_offset, slow_MN_Activations[::20, L_knee_joint_ext_muscle_index], color=slow_colour, label='R activation')
# axs[1, 1].set_title('Knee Ext MN Activations')
axs[1, 2].plot(fast_time + fast_offset, fast_MN_Activations[::20, L_ankle_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 2].plot(medium_time + medium_offset, medium_MN_Activations[::20, L_ankle_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[1, 2].plot(slow_time + slow_offset, slow_MN_Activations[::20, L_ankle_joint_ext_muscle_index], color=slow_colour, label='R activation')
# axs[1, 2].set_title('Ankle Ext MN Activations')

axs[2, 0].plot(fast_time + fast_offset, fast_MN_Activations[::20, L_hip_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 0].plot(medium_time + medium_offset, medium_MN_Activations[::20, L_hip_joint_flx_muscle_index], color=right_colour, label='R activation')
axs[2, 0].plot(slow_time + slow_offset, slow_MN_Activations[::20, L_hip_joint_flx_muscle_index], color=slow_colour, label='R activation')
# axs[2, 0].set_title('Hip Flx MN Activations')
axs[2, 1].plot(fast_time + fast_offset, fast_MN_Activations[::20, L_knee_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 1].plot(medium_time + medium_offset, medium_MN_Activations[::20, L_knee_joint_flx_muscle_index], color=right_colour, label='R activation')
axs[2, 1].plot(slow_time + slow_offset, slow_MN_Activations[::20, L_knee_joint_flx_muscle_index], color=slow_colour, label='R activation')
# axs[2, 1].set_title('Knee Flx MN Activations')
axs[2, 2].plot(fast_time + fast_offset, fast_MN_Activations[::20, L_ankle_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 2].plot(medium_time + medium_offset, medium_MN_Activations[::20, L_ankle_joint_flx_muscle_index], color=right_colour, label='R activation')
axs[2, 2].plot(slow_time + slow_offset, slow_MN_Activations[::20, L_ankle_joint_flx_muscle_index], color=slow_colour, label='R activation')
# axs[2, 2].set_title('Ankle Flx MN Activations')

spkrt = fast_SPK_Activations[:, L_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms + fast_offset, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = medium_SPK_Activations[:, L_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms + medium_offset, spkrt, color=right_colour, label='R ', marker='o', linestyle='')

spkrt = slow_SPK_Activations[:, L_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms + slow_offset, spkrt, color=slow_colour, label='R ', marker='o', linestyle='')
# axs[3, 0].set_title('Hip MN Spike Activations')

spkrt = fast_SPK_Activations[:, L_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms + fast_offset, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = medium_SPK_Activations[:, L_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms + medium_offset, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 1].set_title('Knee MN Spike Activations')

spkrt = slow_SPK_Activations[:, L_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms + slow_offset, spkrt, color=slow_colour, label='R ', marker='o', linestyle='')

spkrt = fast_SPK_Activations[:, L_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms + fast_offset, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = medium_SPK_Activations[:, L_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms + medium_offset, spkrt, color=right_colour, label='R ', marker='o', linestyle='')


spkrt = slow_SPK_Activations[:, L_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms + slow_offset, spkrt, color=slow_colour, label='R ', marker='o', linestyle='')
# axs[3, 2].set_title('Ankle MN Spike Activations')

axs[0, 0].set_xlim(8000,10000)
axs[0, 1].set_xlim(8000,10000)
axs[0, 2].set_xlim(8000,10000)
axs[1, 0].set_xlim(8000,10000)
axs[1, 1].set_xlim(8000,10000)
axs[1, 2].set_xlim(8000,10000)
axs[2, 0].set_xlim(8000,10000)
axs[2, 1].set_xlim(8000,10000)
axs[2, 2].set_xlim(8000,10000)
axs[3, 0].set_xlim(8000,10000)
axs[3, 1].set_xlim(8000,10000)
axs[3, 2].set_xlim(8000,10000)

axs[0, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[0, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[0, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[2, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[2, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[2, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[3, 0].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[3, 1].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[3, 2].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])

axs[0, 0].set_ylim(-45,80)
axs[0, 1].set_ylim(-45,80)
axs[0, 2].set_ylim(-45,80)
axs[1, 0].set_ylim(-105,-45)
axs[1, 1].set_ylim(-105,-45)
axs[1, 2].set_ylim(-105,-45)
axs[2, 0].set_ylim(-105,-45)
axs[2, 1].set_ylim(-105,-45)
axs[2, 2].set_ylim(-105,-45)
axs[3, 0].set_ylim(-2,45)
axs[3, 1].set_ylim(-2,45)
axs[3, 2].set_ylim(-2,45)

# axs[0, 0].set_yticks([8000, 9000, 10000], labels=[])
axs[0, 1].set_yticks([-25, 0, 25, 50, 75], labels=[])
axs[0, 2].set_yticks([-25, 0, 25, 50, 75], labels=[])
# axs[1, 0].set_yticks([-105, -95, -55], labels=[])
axs[1, 1].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[1, 2].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
# axs[2, 0].set_yticks([8000, 9000, 10000], labels=[])
axs[2, 1].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[2, 2].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
# axs[3, 0].set_yticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[3, 1].set_yticks([0, 10, 20, 30, 40], labels=[])
axs[3, 2].set_yticks([0, 10, 20, 30 ,40], labels=[])

# axs[0, 2].legend(loc='lower right')
# axs[1, 2].legend(loc='lower right')
# axs[2, 2].legend(loc='lower right')
axs[0, 2].legend(loc='upper right')

axs[0, 0].set_ylabel(r"$Joint~Angle~(\degree)$")
axs[1, 0].set_ylabel(r"$Extensor~Activation~(nV)$")
axs[2, 0].set_ylabel(r"$Flexor~Activation~(nV)$")
axs[3, 0].set_ylabel(r"$Spike~Rate~(Hz)$")

axs[3, 0].set_xlabel(r"$Time~(s)$")
axs[3, 1].set_xlabel(r"$Time~(s)$")
axs[3, 2].set_xlabel(r"$Time~(s)$")

plt.savefig(r"Python\Speed_Testing\005\left.png")
# plt.show()



# plt.figure() 
fig, axs = plt.subplots(4, 3, figsize=(8, 10))

plt.subplots_adjust(
    # left=0.1,    # the left side of the subplots of the figure
    # right=0.9,   # the right side of the subplots of the figure
    # bottom=0.1,  # the bottom of the subplots of the figure
    # top=0.9,     # the top of the subplots of the figure
    wspace=0.1,  # the amount of width reserved for blank space between subplots
    hspace=0.1   # the amount of height reserved for white space between subplots
)

axs[0, 0].plot(fast_time + fast_offset, fast_angle['R_hip_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 0].plot(medium_time + medium_offset, medium_angle['R_hip_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 0].plot(slow_time + slow_offset, slow_angle['R_hip_joint']*360/np.pi, color=slow_colour, label='R angle')
axs[0, 0].set_title(r'$Right~Hip$') 
axs[0, 1].plot(fast_time + fast_offset, fast_angle['R_knee_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 1].plot(medium_time + medium_offset, medium_angle['R_knee_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 1].plot(slow_time + slow_offset, slow_angle['R_knee_joint']*360/np.pi, color=slow_colour, label='R angle')
axs[0, 1].set_title(r'$Right~Knee$')
axs[0, 2].plot(fast_time + fast_offset, fast_angle['R_ankle_joint']*360/np.pi, color=left_colour, label=r'$Fast$')
axs[0, 2].plot(medium_time + medium_offset, medium_angle['R_ankle_joint']*360/np.pi, color=right_colour, label=r'$Medium$')
axs[0, 2].plot(slow_time + slow_offset, slow_angle['R_ankle_joint']*360/np.pi, color=slow_colour, label=r'$Slow$')
axs[0, 2].set_title(r'$Right~Ankle$')

axs[1, 0].plot(fast_time + fast_offset, fast_MN_Activations[::20, R_hip_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 0].plot(medium_time + medium_offset, medium_MN_Activations[::20, R_hip_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[1, 0].plot(slow_time + slow_offset, slow_MN_Activations[::20, R_hip_joint_ext_muscle_index], color=slow_colour, label='R activation')
# axs[1, 0].set_title('Hip Ext MN Activations')
axs[1, 1].plot(fast_time + fast_offset, fast_MN_Activations[::20, R_knee_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 1].plot(medium_time + medium_offset, medium_MN_Activations[::20, R_knee_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[1, 1].plot(slow_time + slow_offset, slow_MN_Activations[::20, R_knee_joint_ext_muscle_index], color=slow_colour, label='R activation')
# axs[1, 1].set_title('Knee Ext MN Activations')
axs[1, 2].plot(fast_time + fast_offset, fast_MN_Activations[::20, R_ankle_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 2].plot(medium_time + medium_offset, medium_MN_Activations[::20, R_ankle_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[1, 2].plot(slow_time + slow_offset, slow_MN_Activations[::20, R_ankle_joint_ext_muscle_index], color=slow_colour, label='R activation')
# axs[1, 2].set_title('Ankle Ext MN Activations')

axs[2, 0].plot(fast_time + fast_offset, fast_MN_Activations[::20, R_hip_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 0].plot(medium_time + medium_offset, medium_MN_Activations[::20, R_hip_joint_flx_muscle_index], color=right_colour, label='R activation')
axs[2, 0].plot(slow_time + slow_offset, slow_MN_Activations[::20, R_hip_joint_flx_muscle_index], color=slow_colour, label='R activation')
# axs[2, 0].set_title('Hip Flx MN Activations')
axs[2, 1].plot(fast_time + fast_offset, fast_MN_Activations[::20, R_knee_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 1].plot(medium_time + medium_offset, medium_MN_Activations[::20, R_knee_joint_flx_muscle_index], color=right_colour, label='R activation')
axs[2, 1].plot(slow_time + slow_offset, slow_MN_Activations[::20, R_knee_joint_flx_muscle_index], color=slow_colour, label='R activation')
# axs[2, 1].set_title('Knee Flx MN Activations')
axs[2, 2].plot(fast_time + fast_offset, fast_MN_Activations[::20, R_ankle_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 2].plot(medium_time + medium_offset, medium_MN_Activations[::20, R_ankle_joint_flx_muscle_index], color=right_colour, label='R activation')
axs[2, 2].plot(slow_time + slow_offset, slow_MN_Activations[::20, R_ankle_joint_flx_muscle_index], color=slow_colour, label='R activation')
# axs[2, 2].set_title('Ankle Flx MN Activations')

spkrt = fast_SPK_Activations[:, R_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms + fast_offset, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = medium_SPK_Activations[:, R_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms + medium_offset, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 0].set_title('Hip MN Spike Activations')

spkrt = slow_SPK_Activations[:, R_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms + slow_offset, spkrt, color=slow_colour, label='R ', marker='o', linestyle='')

spkrt = fast_SPK_Activations[:, R_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms + fast_offset, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = medium_SPK_Activations[:, R_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms + medium_offset, spkrt, color=right_colour, label='R ', marker='o', linestyle='')

spkrt = slow_SPK_Activations[:, R_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms + slow_offset, spkrt, color=slow_colour, label='R ', marker='o', linestyle='')
# axs[3, 1].set_title('Knee MN Spike Activations')

spkrt = fast_SPK_Activations[:, R_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms + fast_offset, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = medium_SPK_Activations[:, R_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms + medium_offset, spkrt, color=right_colour, label='R ', marker='o', linestyle='')

spkrt = slow_SPK_Activations[:, R_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms + slow_offset, spkrt, color=slow_colour, label='R ', marker='o', linestyle='')
# axs[3, 2].set_title('Ankle MN Spike Activations')

axs[0, 0].set_xlim(8000,10000)
axs[0, 1].set_xlim(8000,10000)
axs[0, 2].set_xlim(8000,10000)
axs[1, 0].set_xlim(8000,10000)
axs[1, 1].set_xlim(8000,10000)
axs[1, 2].set_xlim(8000,10000)
axs[2, 0].set_xlim(8000,10000)
axs[2, 1].set_xlim(8000,10000)
axs[2, 2].set_xlim(8000,10000)
axs[3, 0].set_xlim(8000,10000)
axs[3, 1].set_xlim(8000,10000)
axs[3, 2].set_xlim(8000,10000)

axs[0, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[0, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[0, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[2, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[2, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[2, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[3, 0].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[3, 1].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[3, 2].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])

axs[0, 0].set_ylim(-50,80)
axs[0, 1].set_ylim(-50,80)
axs[0, 2].set_ylim(-50,80)
axs[1, 0].set_ylim(-105,-45)
axs[1, 1].set_ylim(-105,-45)
axs[1, 2].set_ylim(-105,-45)
axs[2, 0].set_ylim(-105,-45)
axs[2, 1].set_ylim(-105,-45)
axs[2, 2].set_ylim(-105,-45)
axs[3, 0].set_ylim(-2,45)
axs[3, 1].set_ylim(-2,45)
axs[3, 2].set_ylim(-2,45)

# axs[0, 0].set_yticks([8000, 9000, 10000], labels=[])
axs[0, 1].set_yticks([-25, 0, 25, 50, 75], labels=[])
axs[0, 2].set_yticks([-25, 0, 25, 50, 75], labels=[])
# axs[1, 0].set_yticks([-105, -95, -55], labels=[])
axs[1, 1].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[1, 2].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
# axs[2, 0].set_yticks([8000, 9000, 10000], labels=[])
axs[2, 1].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[2, 2].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
# axs[3, 0].set_yticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[3, 1].set_yticks([0, 10, 20, 30, 40], labels=[])
axs[3, 2].set_yticks([0, 10, 20, 30 ,40], labels=[])

# axs[0, 2].legend(loc='lower right')
# axs[1, 2].legend(loc='lower right')
# axs[2, 2].legend(loc='lower right')
axs[0, 2].legend(loc='upper right')

axs[0, 0].set_ylabel(r"$Joint~Angle~(\degree)$")
axs[1, 0].set_ylabel(r"$Extensor~Activation~(nV)$")
axs[2, 0].set_ylabel(r"$Flexor~Activation~(nV)$")
axs[3, 0].set_ylabel(r"$Spike~Rate~(Hz)$")

axs[3, 0].set_xlabel(r"$Time~(s)$")
axs[3, 1].set_xlabel(r"$Time~(s)$")
axs[3, 2].set_xlabel(r"$Time~(s)$")

plt.savefig(r"Python\Speed_Testing\005\right.png")
plt.show()

print("Done")

# ---- Extract signals ----
# fast_signal   = fast_MN_Activations[:, R_hip_joint_ext_muscle_index]
# medium_signal = medium_MN_Activations[:, R_hip_joint_ext_muscle_index]
# slow_signal   = slow_MN_Activations[:, R_hip_joint_ext_muscle_index]

fast_signal   = fast_angle['L_hip_joint']
medium_signal = medium_angle['L_hip_joint']
slow_signal   = slow_angle['L_hip_joint']

# ---- Define sampling frequency (Hz) ----
fs = 50  # replace with your actual sampling rate

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

# ---- Plot ----
plt.figure()
plt.plot(freq_fast, mag_fast, label='Fast')
plt.plot(freq_medium, mag_medium, label='Medium')
plt.plot(freq_slow, mag_slow, label='Slow')

plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of L Hip Joint Extensor Activation")
plt.xlim(0.1, 5)  # limit to 0–20 Hz
plt.ylim(0, 60)
plt.legend()
plt.show()

plt.savefig(r"Python\Speed_Testing\005\fft.png")
