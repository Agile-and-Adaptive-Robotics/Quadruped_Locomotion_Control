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

time_path = Path("E:\Hop_Medium1\comm_times.npy")
angle_path = Path("E:\Hop_Medium1\joint_ang.npy")
length_path = Path("E:\Hop_Medium1\muscle_len.npy")
MN_Activations_path = Path(r"E:\Hop_Medium1\nonspk_data.npy")
SPK_Activations_path = Path("E:\Hop_Medium1\spk_data.npy")

time = np.load(time_path, allow_pickle=True)
MN_Activations = np.load(MN_Activations_path, allow_pickle=True)
SPK_Activations = np.load(SPK_Activations_path, allow_pickle=True)

# Indexed, dictionary-like data
angle = np.load(angle_path, allow_pickle=True).item()
length = np.load(length_path, allow_pickle=True).item()

# plt.figure() 
fig, axs = plt.subplots(4, 3, figsize=(8, 10))

left_colour = 'blue'
right_colour = 'red'

plt.subplots_adjust(
    # left=0.1,    # the left side of the subplots of the figure
    # right=0.9,   # the right side of the subplots of the figure
    # bottom=0.1,  # the bottom of the subplots of the figure
    # top=0.9,     # the top of the subplots of the figure
    wspace=0.1,  # the amount of width reserved for blank space between subplots
    hspace=0.1   # the amount of height reserved for white space between subplots
)


axs[0, 0].plot(time, angle['L_hip_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 0].plot(time, angle['R_hip_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 0].set_title(r'$Hip$') 
axs[0, 1].plot(time, angle['L_knee_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 1].plot(time, angle['R_knee_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 1].set_title(r'$Knee$')
axs[0, 2].plot(time, angle['L_ankle_joint']*360/np.pi, color=left_colour, label=r'$Left$')
axs[0, 2].plot(time, angle['R_ankle_joint']*360/np.pi, color=right_colour, label=r'$Right$')
axs[0, 2].set_title(r'$Ankle$')

axs[1, 0].plot(MN_Activations[:, L_hip_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 0].plot(MN_Activations[:, R_hip_joint_ext_muscle_index], color=right_colour, label='R activation')
# axs[1, 0].set_title('Hip Ext MN Activations')
axs[1, 1].plot(MN_Activations[:, L_knee_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 1].plot(MN_Activations[:, R_knee_joint_ext_muscle_index], color=right_colour, label='R activation')
# axs[1, 1].set_title('Knee Ext MN Activations')
axs[1, 2].plot(MN_Activations[:, L_ankle_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 2].plot(MN_Activations[:, R_ankle_joint_ext_muscle_index], color=right_colour, label='R activation')
# axs[1, 2].set_title('Ankle Ext MN Activations')

axs[2, 0].plot(MN_Activations[:, L_hip_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 0].plot(MN_Activations[:, R_hip_joint_flx_muscle_index], color=right_colour, label='R activation')
# axs[2, 0].set_title('Hip Flx MN Activations')
axs[2, 1].plot(MN_Activations[:, L_knee_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 1].plot(MN_Activations[:, R_knee_joint_flx_muscle_index], color=right_colour, label='R activation')
# axs[2, 1].set_title('Knee Flx MN Activations')
axs[2, 2].plot(MN_Activations[:, L_ankle_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 2].plot(MN_Activations[:, R_ankle_joint_flx_muscle_index], color=right_colour, label='R activation')
# axs[2, 2].set_title('Ankle Flx MN Activations')

spkrt = SPK_Activations[:, L_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = SPK_Activations[:, R_hip_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 0].set_title('Hip MN Spike Activations')

spkrt = SPK_Activations[:, L_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = SPK_Activations[:, R_knee_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 1].set_title('Knee MN Spike Activations')

spkrt = SPK_Activations[:, L_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = SPK_Activations[:, R_ankle_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
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

plt.savefig(r"E:\Hop_Medium1\all_rear_Doggo.png")
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

axs[0, 0].plot(time, angle['L_scapula_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 0].plot(time, angle['R_scapula_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 0].set_title(r'$Scapula$') 
axs[0, 1].plot(time, angle['L_shoulder_joint']*360/np.pi, color=left_colour, label='L angle')
axs[0, 1].plot(time, angle['R_shoulder_joint']*360/np.pi, color=right_colour, label='R angle')
axs[0, 1].set_title(r'$Shoulder$')
axs[0, 2].plot(time, angle['L_wrist_joint']*360/np.pi, color=left_colour, label=r'$Left$')
axs[0, 2].plot(time, angle['R_wrist_joint']*360/np.pi, color=right_colour, label=r'$Right$')
axs[0, 2].set_title(r'$Wrist$')

axs[1, 0].plot(MN_Activations[:, L_scapula_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 0].plot(MN_Activations[:, R_scapula_joint_ext_muscle_index], color=right_colour, label='R activation')
# axs[1, 0].set_title('Scapula Ext MN Activations')
axs[1, 1].plot(MN_Activations[:, L_shoulder_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 1].plot(MN_Activations[:, R_shoulder_joint_ext_muscle_index], color=right_colour, label='R activation')
# axs[1, 1].set_title('Shoulder Ext MN Activations')
axs[1, 2].plot(MN_Activations[:, L_wrist_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 2].plot(MN_Activations[:, R_wrist_joint_ext_muscle_index], color=right_colour, label='R activation')
# axs[1, 2].set_title('Wrist Ext MN Activations')

axs[2, 0].plot(MN_Activations[:, L_scapula_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 0].plot(MN_Activations[:, R_scapula_joint_flx_muscle_index], color=right_colour, label='R activation')
# axs[2, 0].set_title('Scap Flx MN Activations')
axs[2, 1].plot(MN_Activations[:, L_shoulder_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 1].plot(MN_Activations[:, R_shoulder_joint_flx_muscle_index], color=right_colour, label='R activation')
# axs[2, 1].set_title('Shoulder Flx MN Activations')
axs[2, 2].plot(MN_Activations[:, L_wrist_joint_flx_muscle_index], color=left_colour, label='L activation')
axs[2, 2].plot(MN_Activations[:, R_wrist_joint_flx_muscle_index], color=right_colour, label='R activation')
# axs[2, 2].set_title('Wrist Flx MN Activations')


spkrt = SPK_Activations[:, L_scapula_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = SPK_Activations[:, R_scapula_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 0].plot(spk_tms, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 0].set_title('Scapula MN Spike Activations')

spkrt = SPK_Activations[:, L_shoulder_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = SPK_Activations[:, R_shoulder_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 1].plot(spk_tms, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 1].set_title('Shoulder MN Spike Activations')

spkrt = SPK_Activations[:, L_wrist_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms, spkrt, color=left_colour, label='L ', marker='o', linestyle='')

spkrt = SPK_Activations[:, R_wrist_joint_flx_muscle_index_spk]
spk_tms = np.where(spkrt > 0.1)[0]
spkrt = np.zeros(len(spk_tms))
for i in range(len(spk_tms)-1):
    spkrt[i] = 1000/((spk_tms[i+1] - spk_tms[i]))
axs[3, 2].plot(spk_tms, spkrt, color=right_colour, label='R ', marker='o', linestyle='')
# axs[3, 2].set_title('Wrist MN Spike Activations')

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

plt.savefig(r"E:\Hop_Medium1\all_fore_Doggo.png")
plt.show()

print("Done")
