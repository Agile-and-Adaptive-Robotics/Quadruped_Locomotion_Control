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

# Diag_MN_Activations_path = Path(r"Diagonal_Medium\nonspk_data.npy")
Diag_MN_Activations_path = Path(r"Python\data\IROS_Submission\Diagonal_Medium\nonspk_data.npy")
Hop_MN_Activations_path = Path(r"Python\data\IROS_Submission\Hop_Medium1a\nonspk_data.npy")
Lat_MN_Activations_path = Path(r"Python\data\IROS_Submission\Lateral_Medium\nonspk_data.npy")

Diag_MN_Activations = np.load(Diag_MN_Activations_path, allow_pickle=True)
Hop_MN_Activations = np.load(Hop_MN_Activations_path, allow_pickle=True)
Lat_MN_Activations = np.load(Lat_MN_Activations_path, allow_pickle=True)

# plt.figure() 
fig, axs = plt.subplots(2, 3, figsize=(8, 5))

left_colour = 'blue'
right_colour = 'red'

plt.subplots_adjust(
    # left=0.1,    # the left side of the subplots of the figure
    # right=0.9,   # the right side of the subplots of the figure
    # bottom=0.1,  # the bottom of the subplots of the figure
    # top=0.9,     # the top of the subplots of the figure
    wspace=0.1,  # the amount of width reserved for blank space between subplots
    hspace=0   # the amount of height reserved for white space between subplots
)
axs[1, 0].axvline(x=8640, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[1, 0].axvline(x=9380, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[1, 0].plot(Diag_MN_Activations[:, L_hip_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 0].plot(Diag_MN_Activations[:, R_hip_joint_ext_muscle_index], color=right_colour, label='R activation')
axs[0, 0].set_title(r'$Diagonal$') 

axs[0, 0].axvline(x=8640, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[0, 0].axvline(x=9380, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[0, 0].plot(Diag_MN_Activations[:, L_scapula_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[0, 0].plot(Diag_MN_Activations[:, R_scapula_joint_ext_muscle_index], color=right_colour, label='R activation')

axs[0, 2].set_title(r'$Hop$') 
axs[1, 2].axvline(x=8520, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[1, 2].axvline(x=9280, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[1, 2].plot(Hop_MN_Activations[:, L_hip_joint_ext_muscle_index], color=left_colour, label='Left')
axs[1, 2].plot(Hop_MN_Activations[:, R_hip_joint_ext_muscle_index], color=right_colour, label='Right')
# # axs[1, 2].set_title('Ankle Ext MN Activations')
axs[0, 2].plot(Hop_MN_Activations[:, L_scapula_joint_ext_muscle_index], color=left_colour, label='Left')
axs[0, 2].plot(Hop_MN_Activations[:, R_scapula_joint_ext_muscle_index], color=right_colour, label='Right')
axs[0, 2].axvline(x=8520, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[0, 2].axvline(x=9280, linestyle='--', color='gray',alpha=0.4,zorder=0 )

axs[0, 1].set_title(r'$Lateral$') 
axs[1, 1].axvline(x=8530, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[1, 1].axvline(x=9220, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[1, 1].plot(Lat_MN_Activations[:, L_hip_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[1, 1].plot(Lat_MN_Activations[:, R_hip_joint_ext_muscle_index], color=right_colour, label='R activation')

axs[0, 1].axvline(x=8530, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[0, 1].axvline(x=9220, linestyle='--', color='gray',alpha=0.4,zorder=0 )
axs[0, 1].plot(Lat_MN_Activations[:, L_scapula_joint_ext_muscle_index], color=left_colour, label='L activation')
axs[0, 1].plot(Lat_MN_Activations[:, R_hip_joint_ext_muscle_index], color=right_colour, label='R activation')

axs[0, 0].set_xlim(8000,10000)
axs[0, 1].set_xlim(8000,10000)
axs[0, 2].set_xlim(8000,10000)
axs[1, 0].set_xlim(8000,10000)
axs[1, 1].set_xlim(8000,10000)
axs[1, 2].set_xlim(8000,10000)

axs[0, 0].set_xticks([8000, 9000, 10000], labels=[])
axs[0, 1].set_xticks([8000, 9000, 10000], labels=[])
axs[0, 2].set_xticks([8000, 9000, 10000], labels=[])
axs[1, 0].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[1, 1].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])
axs[1, 2].set_xticks([8000, 9000, 10000], labels=['8', '9', '10'])

axs[0, 0].set_ylim(-105,-45)
axs[0, 1].set_ylim(-105,-45)
axs[0, 2].set_ylim(-105,-45)
axs[1, 0].set_ylim(-105,-45)
axs[1, 1].set_ylim(-105,-45)
axs[1, 2].set_ylim(-105,-45)

axs[0, 1].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[0, 2].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[1, 1].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])
axs[1, 2].set_yticks([-100, -90, -80, -70, -60, -50], labels=[])

axs[0, 2].legend(loc='upper right')

axs[1, 0].set_ylabel(r"$Hip~Activation~(nV)$")
axs[0, 0].set_ylabel(r"$Scapula~Activation~(nV)$")

axs[1, 0].set_xlabel(r"$Time~(s)$")
axs[1, 1].set_xlabel(r"$Time~(s)$")
axs[1, 2].set_xlabel(r"$Time~(s)$")

# plt.savefig("E:\gait_comparison.png")
plt.savefig(r"Python\data\IROS_Submission\gait_comparison.svg", format = 'svg', bbox_inches= 'tight')
# plt.show()

print("Done")
