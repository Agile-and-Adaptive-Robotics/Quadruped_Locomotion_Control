# =============================
# Joint & Muscle Summary Plot (Generated with Copilot running ChatGPT-4.1)
# =============================
import os
# ...existing code...
# Existing code for plotting individual joint summaries
# ...existing code...
import matplotlib.pyplot as plt
import numpy as np

# =============================
# Imports & Dependencies
# =============================
import matplotlib
matplotlib.use('Agg')
import os
import sys
import math
import time as clock
import time as world_clock
import numpy as np
# import pandas as pd
import mujoco
import mujoco.viewer
import mediapy as media
import matplotlib.pyplot as plt
import scipy.signal
from scipy.signal import find_peaks
import serial
from queue import Queue
from sns_network_model import build_net, spike_net

import modern_robotics as mr


# =============================
# Path Setup
# =============================
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

def mujoco_model(xml_path):

    """
    Load and initialize a MuJoCo model from XML.
    Returns (model, data) tuple.
    """

    # load in the mujoco model and simulation
    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)

    print("... MuJoCo Model Loaded")

    # set some initiial positions: left leg forward, right leg back
    # data.qpos[6] = -0.1
    # data.qpos[14] = 0.1
    # data.qpos[8] = -0.1
    # data.qpos[16] = 0.2

    mujoco.mj_forward(model,data)

    # for i in range(50):
    #     mujoco.mj_step(model, data)
    

    return model, data

def plot_sns(time, data):
    """
    Plots a series of subplots for left and right side muscle activities using given time and data arrays.

    Plot left/right muscle activities for all limbs (SNS output).
    6x2 grid: each row = muscle group, columns = extensor/flexor.

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
    plt.savefig('python/fig_plots/plot_sns_hindlimbs.png')

    plt.figure(figsize=(15, 20))
    for i in range(int(len(left_hind_indices)/2)):
        # Left side fore plots
        plt.subplot(6, 2, 2*i + 1)
        plt.plot(time, data[left_fore_indices[2*i]], label='ext_muscle', color='red')
        plt.plot(time, data[left_fore_indices[2*i+1]], label='flx_muscle', color='green')
        plt.title(f'Left {titles_fore[i]}')
        plt.legend()

        # Right side fore plots
        plt.subplot(6, 2, 2*i + 2)
        plt.plot(time, data[right_fore_indices[2*i]], label='ext_muscle', color='red')
        plt.plot(time, data[right_fore_indices[2*i+1]], label='flx_muscle', color='green')
        plt.title(f'Right {titles_fore[i]}')
        plt.legend()

    plt.tight_layout()
    plt.savefig('python/fig_plots/plot_sns_forelimbs.png')

    # plt.figure()
    # plt.plot(time, data[])
    print("\n", "... SNS plots created")

def plot_spk(time, data):
    """
    Plots a series of subplots for left and right side muscle activities using given time and data arrays.
    Plot left/right muscle activities for all limbs (spiking output).
    6x2 grid: each row = muscle group, columns = extensor/flexor.

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

    plt.savefig('python/fig_plots/plot_spk_hindlimbs.png')


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

    plt.savefig('python/fig_plots/plot_spk_forelimbs.png')

    print("... SPK plots created")

def isolate_cycle(t,vec):
    """
    Extract a single normalized gait cycle from a time series vector.
    Returns (time, single_gait) for one cycle, or zeros if extraction fails.
    """
    try:
        amp = np.max(1/(2+vec)) - np.min(1/(2+vec))
        start_cycle_inds = scipy.signal.find_peaks(1/(2+vec), prominence=0.05, distance=100)[0]
        middle_inds = int(len(start_cycle_inds) - 2)
        single_gait = vec[start_cycle_inds[middle_inds]  :  start_cycle_inds[middle_inds+1]-1]
        time = t[start_cycle_inds[middle_inds]  :  start_cycle_inds[middle_inds+1]-1]
        time = time - time[0]

        # print(t[start_cycle_inds[middle_inds]])
        # print(t[start_cycle_inds[middle_inds+1]-1])
        return time, single_gait - np.min(single_gait)
    
    except:
        return np.zeros(len(t)), np.zeros(len(t))
    
def calc_mse(x_1, y_1, x2, y2):
    y_1_interp = np.interp(x2, x_1, y_1)
    mse = np.mean((y_1_interp - y2)**2)
    return mse

def plot_gaits(time, joint_ang, savename=''):
    """
    Plot hip, knee, and ankle joint angles for all limbs, including single gait cycle and full simulation.
    Compares simulation to animal data.
    """

    R_hip_time, R_hip_gait = isolate_cycle(time, joint_ang['R_hip_joint'])
    R_knee_time, R_knee_gait = isolate_cycle(time, joint_ang['R_knee_joint'])
    R_ankle_time, R_ankle_gait = isolate_cycle(time, joint_ang['R_ankle_joint'])

    # max_len = min([len(R_hip_time), len(R_knee_time), len(R_ankle_time)])

    # save_data = {'hip_t': R_hip_time[:max_len], 
    #              'hip_gait': R_hip_gait[:max_len],
    #              'knee_t': R_knee_time[:max_len], 
    #              'knee_gait': R_knee_gait[:max_len],
    #              'ankle_t': R_ankle_time[:max_len], 
    #              'ankle_gait': R_ankle_gait[:max_len]}
    # df = pd.DataFrame(save_data)
    # df.to_csv('two_layer_gait.csv',index=False)

    L_hip_time, L_hip_gait = isolate_cycle(time, joint_ang['L_hip_joint'])
    L_knee_time, L_knee_gait = isolate_cycle(time, joint_ang['L_knee_joint'])
    L_ankle_time, L_ankle_gait = isolate_cycle(time, joint_ang['L_ankle_joint'])

    # load in the animal data
    anim_data = np.loadtxt('python/JA.csv', delimiter=',')
    anim_time = anim_data[:,0]
    anim_time = anim_time - anim_time[0]
    # hip trajectory
    anim_hip = anim_data[:,1]  - np.min(anim_data[:,1])
    min_index = np.argmin(anim_hip)
    anim_hip = np.concatenate((anim_hip[min_index:], anim_hip[:min_index]))*np.pi/180
    # knee
    anim_knee = (anim_data[:,2] - np.min(anim_data[:,2]))*np.pi/180
    # ankle
    anim_ankle = anim_data[:,3] - np.min(anim_data[:,3])
    min_index = np.argmin(anim_ankle)
    anim_ankle = np.concatenate((anim_ankle[min_index:], anim_ankle[:min_index]))*np.pi/180

    # print('Animal Gait Time: ', anim_time[-1])
    # print('Sim Gait Time:    ', R_hip_time[-1])

    hip_mse   = round(calc_mse(anim_time, anim_hip,   R_hip_time,   R_hip_gait),5)
    knee_mse  = round(calc_mse(anim_time, anim_knee,  R_knee_time,  R_knee_gait),5)
    ankle_mse = round(calc_mse(anim_time, anim_ankle, R_ankle_time, R_ankle_gait),5)

    # print('Hip MSE:   ', hip_mse)
    # print('Knee MSE:  ', knee_mse)
    # print('Ankle MSE: ', ankle_mse)

    hip_amp_error = 10*abs(max(anim_hip) - max(R_hip_gait))  
    cost = np.array([hip_mse, knee_mse, ankle_mse, hip_amp_error]) 
    
    # print(cost) 

    # print(anim_time[-1])
    # print(R_hip_time[-1])
    # print(R_knee_time[-1])
    # print(R_ankle_time[-1])

    plt.figure(figsize=(20,5))
    plt.subplot(1,3,1)
    plt.plot(anim_time, anim_hip, 'r-.', label='Animal Data')
    plt.plot(R_hip_time, R_hip_gait,  'b-', label='Sim Data R')
    plt.plot(L_hip_time, L_hip_gait,  color='green', ls='--', label='Sim Data L')
    plt.title('Hip Trajectory')
    plt.ylabel('Angle (rad)')
    plt.xlabel('Time (s)')
    legend = plt.legend(loc='upper left')
    legend.get_frame().set_alpha(1.0)

    plt.subplot(1,3,2)
    plt.plot(anim_time, anim_knee, 'r-.', label='Animal Data')
    plt.plot(R_knee_time, R_knee_gait,  'b-', label='Sim Data_R')
    plt.plot(L_knee_time, L_knee_gait,  color='green', ls='--', label='Sim Data L')
    plt.title('Knee Trajectory')
    plt.ylabel('Angle (rad)')
    plt.xlabel('Time (s)')
    legend = plt.legend(loc='upper left')
    legend.get_frame().set_alpha(1.0)

    plt.subplot(1,3,3)
    plt.plot(anim_time, anim_ankle, 'r-.', label='Animal Data')
    plt.plot(R_ankle_time, R_ankle_gait,  'b-', label='Sim Data_R')
    plt.plot(L_ankle_time, L_ankle_gait,  color='green', ls='--', label='Sim Data L')
    plt.title('Ankle Trajectory')
    plt.ylabel('Angle (rad)')
    plt.xlabel('Time (s)')
    legend = plt.legend(loc='upper left')
    legend.get_frame().set_alpha(1.0)


    plt.figure(figsize=(15,10))
    for joint in joint_ang.keys():
        if 'L' in joint:
            label = 'Left'
        else:
            label = 'Right'
        
        if 'hip' in joint:
            plt.subplot(3,1,1)
        elif 'knee' in joint:
            plt.subplot(3,1,2)
        else:
            plt.subplot(3,1,3)
        
        plt.plot(time, joint_ang[joint], label=label)
        plt.title(joint.split('_')[-1].capitalize()+' Position')
        plt.ylabel('Joint Angle (rad)')

    plt.subplot(3,1,1)
    plt.legend()
    plt.subplot(3,1,3)
    plt.xlabel('Time (s)')

    # plt.savefig(savename+'.png', bbox_inches='tight')

    if any(cost == 0.0):
        return 10
    else:
        return sum(cost)
    
    plt.savefig('plot_gaits.png')
    print("... Gait plots created")

# Plotter Function entirely vibe-coded with ChatGPT
def plot_legs_master_summary(time, joint_ang, muscle_len, muscle_vel, muscle_ten, save_folder='python/fig_plots'):
    """
    Combined per-leg master plot.
    Layout: 3 rows (angle, length, velocity) x 4 columns (LF, RF, LH, RH).
    Uses the same plotting style as the existing plotters and skips missing data gracefully.
    """
    os.makedirs(save_folder, exist_ok=True)

    leg_joints = {
        'Left Forelimb':   ['L_scapula_joint', 'L_shoulder_joint', 'L_wrist_joint'],
        'Right Forelimb':  ['R_scapula_joint', 'R_shoulder_joint', 'R_wrist_joint'],
        'Left Hindlimb':   ['L_hip_joint', 'L_knee_joint', 'L_ankle_joint'],
        'Right Hindlimb':  ['R_hip_joint', 'R_knee_joint', 'R_ankle_joint'],
    }

    # color mapping per joint type (consistent across legs)
    # Updated so hip and scapula share the same color, and shoulder and knee share the same color.
    joint_color_map = {
        # hip and scapula -> same color
        'hip': 'tab:blue',
        'scapula': 'tab:blue',
        # shoulder and knee -> same color (different from hip/scapula)
        'shoulder': 'tab:orange',
        'knee': 'tab:orange',
        # ankle and wrist keep existing matching color
        'ankle': 'tab:green',
        'wrist': 'tab:green'
    }

    def get_color_for_joint(joint_name):
        for key, col in joint_color_map.items():
            if key in joint_name:
                return col
        return 'k'

    from matplotlib import colors as mcolors

    def is_flexor(name):
        lname = name.lower()
        return ('flx' in lname) or ('flex' in lname) or ('flexor' in lname)

    def lighten_color(col, amount=0.5):
        """Return a lighter shade of the color by blending with white.
        amount=0 -> original color, amount=1 -> white."""
        try:
            rgb = mcolors.to_rgb(col)
        except Exception:
            rgb = mcolors.to_rgb('k')
        return tuple(r + (1.0 - r) * amount for r in rgb)

    # Use GridSpec to make angle(1 row), length(3 stacked subrows), velocity(1 row), and tension (3 stacked subrows)
    import matplotlib.gridspec as gridspec
    # height ratios: angle=1, each length subrow=0.33, velocity=1, each tension subrow=0.33
    height_ratios = [1, 0.33, 0.33, 0.33, 1, 0.33, 0.33, 0.33]
    fig = plt.figure(figsize=(20, 18))
    gs = gridspec.GridSpec(nrows=8, ncols=4, height_ratios=height_ratios, hspace=0.4, figure=fig)

    # Plot angles (top row)
    for col, (leg, joints) in enumerate(leg_joints.items()):
        ax = fig.add_subplot(gs[0, col])
        plotted = False
        for joint in joints:
            if joint in joint_ang:
                colc = get_color_for_joint(joint)
                ax.plot(time, joint_ang[joint], '.', color=colc, label=joint)
                plotted = True
        ax.set_title(f"{leg} - Angle")
        ax.set_ylabel('Angle (rad)')
        if plotted:
            ax.legend(fontsize='small')
        ax.grid(True, alpha=0.3)

    # Plot lengths: three stacked subrows, one per joint in the leg (order matches leg_joints list)
    for col, (leg, joints) in enumerate(leg_joints.items()):
        for j_idx, joint in enumerate(joints):
            ax = fig.add_subplot(gs[1 + j_idx, col])
            plotted = False
            muscles = [m for m in muscle_len.keys() if joint.replace('_joint', '') in m]
            for m in muscles:
                base_col = get_color_for_joint(joint)
                plot_col = lighten_color(base_col, amount=0.5) if is_flexor(m) else base_col
                ax.plot(muscle_len[m], marker='.', linestyle='-', color=plot_col, label=m)
                plotted = True
            # Title each small length subplot by joint name for clarity
            jlabel = joint.replace('_joint', '').replace('L_', '').replace('R_', '').capitalize()
            ax.set_title(f"{leg} - {jlabel} Length")
            ax.set_ylabel('Length (m)')
            if plotted:
                ax.legend(fontsize='x-small')
            ax.grid(True, alpha=0.25)

    # Plot velocities (second-to-bottom row)
    for col, (leg, joints) in enumerate(leg_joints.items()):
        ax = fig.add_subplot(gs[4, col])
        plotted = False
        for joint in joints:
            muscles = [m for m in muscle_vel.keys() if joint.replace('_joint', '') in m]
            for m in muscles:
                base_col = get_color_for_joint(joint)
                plot_col = lighten_color(base_col, amount=0.5) if is_flexor(m) else base_col
                ax.plot(muscle_vel[m], marker='.', linestyle='-', color=plot_col, label=m)
                plotted = True
        ax.set_title(f"{leg} - Muscle Velocity")
        ax.set_ylabel('Velocity (m/s)')
        ax.set_xlabel('Time (samples)')
        if plotted:
            ax.legend(fontsize='small')
        ax.grid(True, alpha=0.3)

    # Plot tensions: three stacked subrows under each limb column matching the length subplots style
    for col, (leg, joints) in enumerate(leg_joints.items()):
        for j_idx, joint in enumerate(joints):
            ax = fig.add_subplot(gs[5 + j_idx, col])
            plotted = False
            # find muscles related to this joint
            muscles = [m for m in muscle_ten.keys() if joint.replace('_joint', '') in m]
            for m in muscles:
                base_col = get_color_for_joint(joint)
                plot_col = lighten_color(base_col, amount=0.5) if is_flexor(m) else base_col
                ax.plot(muscle_ten[m], marker='.', linestyle='-', color=plot_col, label=m)
                plotted = True
            jlabel = joint.replace('_joint', '').replace('L_', '').replace('R_', '').capitalize()
            ax.set_title(f"{leg} - {jlabel} Tension")
            ax.set_ylabel('Tension (N)')
            if plotted:
                ax.legend(fontsize='x-small')
            ax.grid(True, alpha=0.25)

    plt.tight_layout()
    fname = os.path.join(save_folder, 'legs_master_summary.png')
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("... Legs master summary created ->", fname)



def plot_times(times):
    """
    Prints the times it took to run each section of the code throughout the simulation.
    Makes a pie chart of these times. 

    Parameters:
    times (array-like): An array of time points. 
                        t_init, t_sns, t_mujoco, t_sns2mujoco, t_mujoco2sns, t_plot, t_video = times
                        t_init:       time to initialize and compile models
                        t_sns:        time in sns-toolbox running the nueral model. Does not include compiling the model
                        t_mujoco:     time running the phisics model. Does not include compiling the model
                        t_sns2mujoco: time calculating the muscle activations from motor neuron data
                        t_mujoco2sns: time computing the feedback from biomechanical to neural model
                        t_plot:       time devoted to plotting the joint and neural data
                        t_video:      time devoted to making the video of the biomechanical model

    Returns:
    None
    """
    time_print, time_sns, time_spk, time_spkqueue, time_mujo, time_feed, time_vid, time_loop = times
    labels = ['Print-to-Terminal', 'SNS-Toolox', 'SNS-Spike Creation' 'Add-to-Spike Queue', 'MuJoCo', 'Feedback Processing', 'Video Creation']
    print('\n','Print-to-Terminal Time:          ', round(time_print,4))
    print('SNS-Toolox Time:                 ', round(time_sns,4))
    print('SNS-Toolox Spk Time:             ', round(time_spk,4))
    print('Add-to-Spike Queue Time:         ', round(time_spkqueue,4))
    print('MuJoCo Time:                     ', round(time_mujo,4))
    print('Feedback Processing Time:        ', round(time_feed,4))
    print('Video Creation Time:             ', round(time_vid,4))
    print('Total Loop Time:                 ', round(time_print+time_sns+time_spk+time_spkqueue+time_mujo+time_feed+time_vid,4))
    print('Total Loop Time (check):         ', round(time_loop,4))
    
    plt.figure()  # Optional: adjust the figure size
    plt.pie(times[0:6], labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Sim Loop Time Distribution')
    plt.axis('equal')

    plt.savefig('python/fig_plots/plot_times.png')

# def save_data(muscle_len, muscle_vel, muscle_ten):
#     # sns_data outputs: should be 24
#     # Right Side
#     # 0 - hip mn ext
#     # 1 - hip mn flx
#     # 2 - knee mn ext
#     # 3 - knee mn flx
#     # 4 - ankle mn ext
#     # 5 - ankle mn flx
#     # 6 - RG ext
#     # 7 - RG flx
#     # 8 - hip PF ext
#     # 9 - hip PF flx
#     # 10- KA PF ext
#     # 11- KA PF flx

#     # Left Side
#     # 12 - hip mn ext
#     # 13 - hip mn flx
#     # 14 - knee mn ext
#     # 15 - knee mn flx
#     # 16 - ankle mn ext
#     # 17 - ankle mn flx
#     # 18 - RG ext
#     # 19 - RG flx
#     # 20 - hip PF ext
#     # 21 - hip PF flx
#     # 22 - KA PF ext
#     # 23 - KA PF flx

#     sns_headers = ['R_hip_MN_Ext', 'R_hip_MN_Flx', 'R_knee_MN_Ext', 'R_knee_MN_Flx', 'R_ankle_MN_Ext', 'R_ankle_MN_Flx', 'R_RG_Ext', 'R_RG_Flx', 'R_hip_PF_Ext', 'R_hip_PF_Flx', 'R_KA_PF_Ext', 'R_KA_PF_Flx',
#                'L_hip_MN_Ext', 'L_hip_MN_Flx', 'L_knee_MN_Ext', 'L_knee_MN_Flx', 'L_ankle_MN_Ext', 'L_ankle_MN_Flx', 'L_RG_Ext', 'L_RG_Flx', 'L_hip_PF_Ext', 'L_hip_PF_Flx', 'L_KA_PF_Ext', 'L_KA_PF_Flx']
    
#     # sns_df = pd.DataFrame(sns_data, columns=sns_headers)

#     # joint_df = pd.DataFrame(joint_ang)
#     muscle_len_df = pd.DataFrame(muscle_len)
#     muscle_vel_df = pd.DataFrame(muscle_vel)
#     muscle_ten_df = pd.DataFrame(muscle_ten)

#     base_folder = 'feedback_test/'

#     # sns_df.to_csv(base_folder+'sns_data.csv', index=False)
#     # joint_df.to_csv(base_folder+'joint_ang.csv', index=False)
#     muscle_len_df.to_csv(base_folder+'muscle_length.csv', index=False)
#     muscle_vel_df.to_csv(base_folder+'muscle_velocity.csv', index=False)
#     muscle_ten_df.to_csv(base_folder+'muscle_tension.csv', index=False)

#     print("... Data saved")
    
def vel2S(vel):
    return 4.3*np.sign(vel)*(np.abs(vel)**(0.6)) + 82

def hip_inputs(length_e, length_f, velocity_e, velocity_f, tension_e, tension_f, L0_e, L0_f):
    Ia_e = vel2S(velocity_e)*10 -820
    Ia_f = vel2S(velocity_f)*10 -820
    Ib_e = tension_e*(-2) -1
    Ib_f = tension_f*(-2) -1
    II_e = (length_e - L0_e) *1000 +1
    II_f = (length_f - L0_f) *1000

    return np.array([Ia_e, Ia_f, Ib_e, Ib_f, II_e, II_f])

def knee_inputs(length_e, length_f, velocity_e, velocity_f, tension_e, tension_f, L0_e, L0_f):
    Ia_e = vel2S(velocity_e)*10 -820
    Ia_f = vel2S(velocity_f)*10 -820
    Ib_e = tension_e*(-1)-1
    Ib_f = tension_f*(-5)-1
    # II_e = (length_e - L0_e) *2000 -2.75
    # II_f = (length_f - L0_f) *500  +3

    return np.array([Ia_e, Ia_f, Ib_e, Ib_f])

def ankle_inputs(length_e, length_f, velocity_e, velocity_f, tension_e, tension_f, L0_e, L0_f):
    Ia_e = vel2S(velocity_e)*10 -820
    Ia_f = vel2S(velocity_f)*10 -820
    Ib_e = tension_e*(-1)-1
    Ib_f = tension_f*(-3)-1
    # II_e = (length_e - L0_e) *10000 -5.5
    II_f = (length_f - L0_f) *7000  +7

    return np.array([Ia_e, Ia_f, Ib_e, Ib_f, II_f])

def scapula_inputs(length_e, length_f, velocity_e, velocity_f, tension_e, tension_f, L0_e, L0_f):
    Ia_e = vel2S(velocity_e)*10 -820
    Ia_f = vel2S(velocity_f)*10 -820
    Ib_e = tension_e*(-2) -1
    Ib_f = tension_f*(-2) -1
    II_e = (length_e - L0_e) *2000 +1
    II_f = (length_f - L0_f) *2000

    return np.array([Ia_e, Ia_f, Ib_e, Ib_f, II_e, II_f])

def shoulder_inputs(length_e, length_f, velocity_e, velocity_f, tension_e, tension_f, L0_e, L0_f):
    Ia_e = vel2S(velocity_e)*10 -820
    Ia_f = vel2S(velocity_f)*10 -820
    Ib_e = tension_e*(-1)-1
    Ib_f = tension_f*(-5)-1
    # II_e = (length_e - L0_e) *2000 -2.75
    # II_f = (length_f - L0_f) *500  +3

    return np.array([Ia_e, Ia_f, Ib_e, Ib_f])

def wrist_inputs(length_e, length_f, velocity_e, velocity_f, tension_e, tension_f, L0_e, L0_f):
    Ia_e = vel2S(velocity_e)*10 -820
    Ia_f = vel2S(velocity_f)*10 -820
    Ib_e = tension_e*(-1)-1
    Ib_f = tension_f*(-3)-1
    # II_e = (length_e - L0_e) *10000 -5.5
    II_f = (length_f - L0_f) *7000  +7

    return np.array([Ia_e, Ia_f, Ib_e, Ib_f, II_f])

def stim_to_act(stim):
    """
    Convert neural potential to muscle activation [0, 1].
    """
    # converted the stim2tenstion curve in animatlab
    steepness = 0.121465
    x_offset = -65
    y_offset = -0.002297
    amp = 1.0
    act = amp/(1 + np.exp(steepness*(x_offset-stim))) + y_offset
    return min(max(act, 0), 1)


def non_to_spk(x,half_point,bandwidth):
    """
    Convert neural potential to muscle activation [0, 1] (spiking version).
    """
    # converted the stim2tenstion curve in animatlab
    steepness = 10/bandwidth
    y_offset = 0.01
    x_offset = half_point
    amp = 2
    y = amp/(1 + np.exp(steepness*(x_offset-x))) + y_offset

    return min(max(y, 0), amp)


def muscle_data(
            pressure_sensor_data,
            potentiometer_data,
            muscle_length_static,
            muscle_length_dynamic,
            muscle_wrap,
            M,
            Slist,
            muscle_insertion_rest_polar,
            joint_ang,
            joint_radius,
            BPA_L0,
            muscle_len,
            muscle_vel,
            muscle_ten,
            comm_dt,
            comm_index):

    """
    Updates joint angle, muscle length, velocity, and tension dictionaries in place
    based on potentiometer and pressure sensor readings.
    """
    comm_index = int(comm_index)  # Ensure comm_index is an integer
    angle_conversion = - (3/2 * np.pi) / 255  # TODO: Measure this

    # Update joint angles
    for joint in joint_ang.keys():
        joint_ang[joint][comm_index] = (int(potentiometer_data[joint][comm_index]) - int(potentiometer_data[joint][0])) * angle_conversion

    # Update muscle lengths
    for muscle in muscle_len.keys():
        for joint in joint_ang.keys():
            if joint in muscle:
                if any(j in muscle for j in ('wrist', 'ankle', 'knee', 'shoulder')):

                        x_0 = muscle_wrap[muscle][0] #+ joint_offset[muscle][0]
                        y_0 = muscle_wrap[muscle][1] #+ joint_offset[muscle][1]

                        T= mr.FKinSpace(M[muscle], Slist[muscle], [joint_ang[joint][comm_index]])
                        x_1 = T[0,3]
                        y_1 = T[1,3]

                        muscle_length_dynamic[muscle] = np.sqrt((x_0 - x_1)**2 + (y_0 - y_1)**2) # * np.sign(y_0-y_1)  * np.sign(x_0-x_1)

                        muscle_len[muscle][comm_index] =  muscle_length_dynamic[muscle]+ muscle_length_dynamic[muscle]

                elif any(j in muscle for j in ('hip', 'scapula')):
                    r  = joint_radius[muscle] # measured directly

                    if 'ext' in muscle:
                        theta_0 = joint_ang[joint][comm_index]
                    else:
                        theta_0 = - joint_ang[joint][comm_index]
                        
                    muscle_length_dynamic[muscle] = r * theta_0
                    muscle_len[muscle][comm_index] = muscle_length_static[muscle] + muscle_length_dynamic[muscle]

                else: 
                    print('ERROR! with', muscle, 'muscle')

    # print("\n\n")

    # Update muscle velocities (m/s) (second order backwards difference approximation to remove noise. requires index > 1)
    if comm_index > 1:
        for muscle in muscle_vel.keys():
            muscle_vel[muscle][comm_index] = (3 * muscle_len[muscle][comm_index] - 4 * muscle_len[muscle][comm_index - 1] + muscle_len[muscle][comm_index - 2]) / (2 * comm_dt)
    else:
        for muscle in muscle_vel.keys():
            muscle_vel[muscle][comm_index] = 0.0

    # Tension equation by Ben Bolen
    c_0 = 0.5682
    c_1 = 4.254
    c_2 = 0.5597

    pressure_conversion = 700 / 215 # Eyeballed conversion to kPa
    
    # Update muscle tensions from pressure sensor
    for muscle in muscle_ten.keys():
        ep = ( muscle_len[muscle][comm_index] - muscle_len[muscle][0] ) + BPA_L0[muscle]
        P = ( pressure_sensor_data[muscle][comm_index] - pressure_sensor_data[muscle][0] ) * pressure_conversion

        muscle_ten[muscle][comm_index] = c_0 * (np.exp(float(-c_1 * ep)) - 1) + (P * np.exp(float(-c_2 * ep**2)))

    # Print joint status to terminal
    # sys.stdout.write(f"\033[{len(joint_ang.keys())}A")
    #  # Update muscle lengths
    # for muscle in muscle_len.keys():
    #     for joint in joint_ang.keys():
    #         if joint in muscle:
                # sys.stdout.write("\033[K")
                # sys.stdout.write(f"{muscle:<30} {round((joint_ang[joint][comm_index]+muscle_insertion_rest_polar[muscle][1]),2):<10}  {round(muscle_length_dynamic[muscle],4):<10} {round(muscle_len[muscle][comm_index],4):<10}\n")
                # sys.stdout.write(f"{muscle:<30} {round(muscle_len[muscle][comm_index],4):<10} {round(muscle_ten[muscle][comm_index],4):<10}\n")
 
    return





def run_sims(dt, 
             num_steps, 
             end_time, 
             comm_freq,
             num_comms,
             xml_path, 
             cpg_inputs, 
             cpg_gsyn=1.49167, 
             feed_forward=True,
             muscle_mutt=False,
             make_vid=True,
             spike_port_name='name_goes_here',
             sense_port_name='name_goes_here',
             data_location=False):
    """
    Runs a simulation integrating a neural network model (SNS toolbox) with a Mujoco physics engine model.

    Parameters:
    dt (float): Time step for the simulation in seconds.
    num_steps (int): Number of simulation steps to run.
    xml_path (str): Path to the Mujoco XML model file.
    L_cpg_inputs (ndarray): Left CPG inputs for each simulation step.
    R_cpg_inputs (ndarray): Right CPG inputs for each simulation step.
    save_name (str): Base name for saving simulation outputs (optional).

    Returns:
    None

    This function integrates the SNS toolbox neural network model with Mujoco physics simulations over a specified 
    number of time steps. It calculates and records joint positions, muscle lengths, forces, and velocities, and can 
    optionally generate a video and plot simulations.
    """

    '''
    We want the simulation to run fast, such that errors are not created. However, we only want to send spikes in batches.
    Spikes are "and"ed on to each other and send at 50 Hz.
    '''

    # ----------------------
    # Initialization Section
    # ----------------------

    # --- Timing and Communication ---
    comm_dt    = 1 / comm_freq       # Communication period (s)
    comm_index = 0               # Communication event counter

    # --- Simulation Time Vectors ---
    t = np.arange(0, num_steps)
    time = np.zeros([len(t)])

    # --- MuJoCo and SNS Model Initialization ---
    mujoco_dt = dt
    sns_dt = mujoco_dt * 1000
    mujoco_sim, mujoco_data = mujoco_model(xml_path)
    mujoco_sim.opt.timestep = mujoco_dt
    sns_model = build_net(dt=sns_dt, cpg_gsyn=cpg_gsyn, feed_forward=feed_forward)
    spk_model = spike_net(dt=sns_dt) # Nonspiking to spiking conversion network

    # --- SNS Data Structures ---
    num_outputs = sns_model.num_outputs
    sns_sim_data = np.zeros([len(t), num_outputs])
    sns_sim_data[0] = [-100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -60, -60, -60, -60, -60, -60, 
                       -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -60, -60, -60, -60, -60, -60,
                       -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -60, -60, -60, -60, -60, -60, 
                       -100.0, -100.0, -100.0, -100.0, -100.0, -100.0, -60, -60, -60, -60, -60, -60]
    num_spk_out = spk_model.num_outputs
    sns_spk_data = np.zeros([len(t), num_spk_out])
    sns_spk_data[0] = np.zeros([num_spk_out])
    num_inputs   = int(sns_model.num_inputs)
    sns_inputs   = np.concatenate([np.zeros(num_inputs-1), [0]])
    num_spk_in   = int(spk_model.num_inputs)
    spk_inputs   = np.concatenate([np.zeros(num_spk_in)])

    # --- Muscle and Joint Initialization ---
    muscles_list = [mujoco.mj_id2name(mujoco_sim, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(mujoco_sim.nu)]
    all_joint_names = [mujoco.mj_id2name(mujoco_sim, mujoco.mjtObj.mjOBJ_JOINT, i) for i in range(mujoco_sim.njnt)]
    joint_list = [name for name in all_joint_names if any(keyword in name for keyword in ['hip', 'knee', 'ankle', 'scapula', 'shoulder', 'wrist'])]

    # --- Indices corresponding to item name ~ Needed only for MuJoCo ---
    joint_indices  = {name: mujoco.mj_name2id(mujoco_sim, mujoco.mjtObj.mjOBJ_JOINT, name)    for name in  joint_list}
    muscle_indices = {name: mujoco.mj_name2id(mujoco_sim, mujoco.mjtObj.mjOBJ_ACTUATOR, name) for name in  muscles_list}

    # --- Raw Robot Data Structures ---
    potentiometer_data      = {key: np.zeros(num_comms) for key in joint_list}
    pressure_sensor_data    = {key: np.zeros(num_comms) for key in muscles_list}

    # --- Muscle Properties ---
    if muscle_mutt:
        joint_ang  = {key: np.zeros(num_comms) for key in joint_list}
        muscle_len = {key: np.zeros(num_comms) for key in muscles_list}
        muscle_vel = {key: np.zeros(num_comms) for key in muscles_list}
        muscle_ten = {key: np.zeros(num_comms) for key in muscles_list}

        muscle_origin           = {name: [0,0] for name in muscles_list}
        muscle_wrap             = {name: [0,0] for name in muscles_list}
        joint_offset            = {name: [0,0] for name in muscles_list}
        muscle_insertion   = {name: [0,0] for name in muscles_list}
        for muscle in muscles_list:
            if   'hip_joint_ext_muscle' in muscle:        
                muscle_origin[muscle]               = [-0.083,  0.037]
                muscle_wrap[muscle]                 = [-0.508, -0.00]
                joint_offset[muscle]                = [-0.508, -0.025]
                muscle_insertion[muscle]            = [-0.0201,  0.0001+joint_offset[muscle][1]]
            elif 'hip_joint_flx_muscle' in muscle:        
                muscle_origin[muscle]               = [-0.083,  0.015]
                muscle_wrap[muscle]                 = [-0.508, -0.0451]
                joint_offset[muscle]                = [-0.508, -0.025]
                muscle_insertion[muscle]            = [-0.0201, -0.0001+joint_offset[muscle][1]]
            elif 'knee_joint_ext_muscle' in muscle:       
                muscle_origin[muscle]               = [0.024,    0.0250]
                muscle_wrap[muscle]                 = [0.0225,   -0.2025]
                joint_offset[muscle]                = [0.000,   -0.2225]
                muscle_insertion[muscle]            = [0.016,     0.007+joint_offset[muscle][1]]
            elif 'knee_joint_flx_muscle' in muscle:       
                muscle_origin[muscle]               = [-0.024,   0.0250]
                muscle_wrap[muscle]                 = [-0.0225, -0.2025]
                joint_offset[muscle]                = [ 0.000,  -0.2225]
                muscle_insertion[muscle]            = [-0.015,  -0.013+joint_offset[muscle][1]]
            elif 'ankle_joint_ext_muscle' in muscle:      
                muscle_origin[muscle]               = [-0.025,  -0.034]
                muscle_wrap[muscle]                 = [-0.0225, -0.20]
                joint_offset[muscle]                = [0,       -0.22]
                muscle_insertion[muscle]            = [0.0,      0.0100+joint_offset[muscle][1]]
            elif 'ankle_joint_flx_muscle' in muscle:      
                muscle_origin[muscle]               = [0.020,   -0.006]
                muscle_wrap[muscle]                 = [0.0225,  -0.20]
                joint_offset[muscle]                = [0,       -0.22]
                muscle_insertion[muscle]            = [0.0075,  -0.015+joint_offset[muscle][1]]
            elif 'scapula_joint_ext_muscle' in muscle:    
                muscle_origin[muscle]               = [-0.405,  0.045]
                muscle_wrap[muscle]                 = [0,       0.1051]
                joint_offset[muscle]                = [0,       0.085]
                muscle_insertion[muscle]            = [0.0201,  0.0001+joint_offset[muscle][1]]
            elif 'scapula_joint_flx_muscle' in muscle:    
                muscle_origin[muscle]               = [-0.405,  0.023]
                muscle_wrap[muscle]                 = [0,      0.065]
                joint_offset[muscle]                = [0,      0.085]
                muscle_insertion[muscle]            = [0.0201,-0.0001+joint_offset[muscle][1]]
            elif 'shoulder_joint_ext_muscle' in muscle:   
                muscle_origin[muscle]               = [0.024 ,  0.025]
                muscle_wrap[muscle]                 = [0.0225, -0.15]
                joint_offset[muscle]                = [0,      -0.17]
                muscle_insertion[muscle]            = [0.022,   0.011+joint_offset[muscle][1]]
            elif 'shoulder_joint_flx_muscle' in muscle:   
                muscle_origin[muscle]               = [-0.024,  0.025]
                muscle_wrap[muscle]                 = [-0.0225,-0.15]
                joint_offset[muscle]                = [0,      -0.17]
                muscle_insertion[muscle]            = [-0.011, -0.015+joint_offset[muscle][1]]
            elif 'wrist_joint_ext_muscle' in muscle:      
                muscle_origin[muscle]               = [-0.023, 0.016]
                muscle_wrap[muscle]                 = [-0.023, 0.016] # TODO: Update this! Currently no wrapping point in MuJoCo model
                joint_offset[muscle]                = [0,     -0.2125]
                muscle_insertion[muscle]            = [-0.01,  0.02+joint_offset[muscle][1]]
            elif 'wrist_joint_flx_muscle' in muscle:      
                muscle_origin[muscle]               = [0.023,  -0.023]
                muscle_wrap[muscle]                 = [0.023,  -0.023] # TODO: Update this! Currently no wrapping point in MuJoCo model
                joint_offset[muscle]                = [0,      -0.2125]
                muscle_insertion[muscle]  = [0.0075, -0.015+joint_offset[muscle][1]]

        M     = {name: np.array([[0,0,0,0],
                                [0,0,0,0],
                                [0,0,0,0],
                                [0,0,0,0]]) for name in muscles_list}
        Slist = {name: np.array([[0],
                                 [0],
                                 [1],
                                 [0],
                                 [0],
                                 [0]]) for name in muscles_list}
        for muscle in muscles_list:
                M[muscle] = np.array([[1,0,0,muscle_insertion[muscle][0]],
                                      [0,1,0,muscle_insertion[muscle][1]],
                                      [0,0,1,0],
                                      [0,0,0,1]])
            # Revolute about z through q = (qx, qy, 0)
                # w = [0,0,1]; v = -w x q = [ qy, -qx, 0 ]
                qx = float(joint_offset[muscle][0])
                qy = float(joint_offset[muscle][1])
                Slist[muscle] = np.array([[0.0],
                                           [0.0],
                                           [1.0],
                                           [qy],
                                           [-qx],
                                           [0.0]])


        muscle_insertion_rest_polar = {name: [0,0] for name in muscles_list} # muscle insertion point in polar coordinates
        muscle_length_static        = {name: 0.0 for name in muscles_list} # length of the static portion
        muscle_length_dynamic       = {name: 0.0 for name in muscles_list} # length of the static portion

        for muscle in muscles_list:
            x_0 = muscle_origin[muscle][0]
            x_1 = muscle_wrap[muscle][0]
            x_2 = muscle_insertion[muscle][0]
            y_0 = muscle_origin[muscle][1]
            y_1 = muscle_wrap[muscle][1]
            y_2 = muscle_insertion[muscle][1]

            muscle_length_static[muscle] = np.sqrt((x_0 - x_1)**2 + (y_0 - y_1)**2) # + np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2) # length of static portion of muscle

        # BPA resting lengths for tension calculation.
        joint_radius = {name: 0.0 for name in muscles_list}
        for muscle in muscles_list:
            if   'hip_joint_flx_muscle' in muscle:        joint_radius[muscle] = 0.0365/2
            elif 'hip_joint_ext_muscle' in muscle:        joint_radius[muscle] = 0.0365/2
            elif 'knee_joint_flx_muscle' in muscle:       joint_radius[muscle] = 0.020
            elif 'knee_joint_ext_muscle' in muscle:       joint_radius[muscle] = 0.019
            elif 'ankle_joint_flx_muscle' in muscle:      joint_radius[muscle] = 0.018
            elif 'ankle_joint_ext_muscle' in muscle:      joint_radius[muscle] = 0.020
            elif 'scapula_joint_flx_muscle' in muscle:    joint_radius[muscle] = 0.0365/2
            elif 'scapula_joint_ext_muscle' in muscle:    joint_radius[muscle] = 0.0365/2
            elif 'shoulder_joint_flx_muscle' in muscle:   joint_radius[muscle] = 0.019
            elif 'shoulder_joint_ext_muscle' in muscle:   joint_radius[muscle] = 0.024
            elif 'wrist_joint_flx_muscle' in muscle:      joint_radius[muscle] = 0.017
            elif 'wrist_joint_ext_muscle' in muscle:      joint_radius[muscle] = 0.021
            
        # BPA resting lengths for tension calculation.
        BPA_L0 = {name: 0.0 for name in muscles_list}
        for muscle in muscles_list:
            if   'hip_joint_flx_muscle' in muscle:        BPA_L0[muscle] = 0.268
            elif 'hip_joint_ext_muscle' in muscle:        BPA_L0[muscle] = 0.268
            elif 'knee_joint_flx_muscle' in muscle:       BPA_L0[muscle] = 0.166
            elif 'knee_joint_ext_muscle' in muscle:       BPA_L0[muscle] = 0.162
            elif 'ankle_joint_flx_muscle' in muscle:      BPA_L0[muscle] = 0.135
            elif 'ankle_joint_ext_muscle' in muscle:      BPA_L0[muscle] = 0.117
            elif 'scapula_joint_flx_muscle' in muscle:    BPA_L0[muscle] = 0.268
            elif 'scapula_joint_ext_muscle' in muscle:    BPA_L0[muscle] = 0.268
            elif 'shoulder_joint_flx_muscle' in muscle:   BPA_L0[muscle] = 0.128
            elif 'shoulder_joint_ext_muscle' in muscle:   BPA_L0[muscle] = 0.13
            elif 'wrist_joint_flx_muscle' in muscle:      BPA_L0[muscle] = 0.15
            elif 'wrist_joint_ext_muscle' in muscle:      BPA_L0[muscle] = 0.128
        
        # --- Motoneuron Properties ---
        act_bandwidth = {name: 1.0 for name in muscles_list}
        for muscle in muscles_list:
            if   'hip_joint_ext_muscle' in muscle:        act_bandwidth[muscle] = 10
            elif 'hip_joint_flx_muscle' in muscle:        act_bandwidth[muscle] = 10
            elif 'knee_joint_ext_muscle' in muscle:       act_bandwidth[muscle] = 10
            elif 'knee_joint_flx_muscle' in muscle:       act_bandwidth[muscle] = 10
            elif 'ankle_joint_ext_muscle' in muscle:      act_bandwidth[muscle] = 10
            elif 'ankle_joint_flx_muscle' in muscle:      act_bandwidth[muscle] = 10
            elif 'scapula_joint_ext_muscle' in muscle:    act_bandwidth[muscle] = 10
            elif 'scapula_joint_flx_muscle' in muscle:    act_bandwidth[muscle] = 10
            elif 'shoulder_joint_ext_muscle' in muscle:   act_bandwidth[muscle] = 10
            elif 'shoulder_joint_flx_muscle' in muscle:   act_bandwidth[muscle] = 10
            elif 'wrist_joint_ext_muscle' in muscle:      act_bandwidth[muscle] = 10
            elif 'wrist_joint_flx_muscle' in muscle:      act_bandwidth[muscle] = 10

        act_mid = {name: -65 for name in muscles_list}
        for muscle in muscles_list:
            if   'hip_joint_ext_muscle' in muscle:        act_mid[muscle] = -95
            elif 'hip_joint_flx_muscle' in muscle:        act_mid[muscle] = -95
            elif 'knee_joint_ext_muscle' in muscle:       act_mid[muscle] = -95
            elif 'knee_joint_flx_muscle' in muscle:       act_mid[muscle] = -95
            elif 'ankle_joint_ext_muscle' in muscle:      act_mid[muscle] = -95
            elif 'ankle_joint_flx_muscle' in muscle:      act_mid[muscle] = -95
            elif 'scapula_joint_ext_muscle' in muscle:    act_mid[muscle] = -95
            elif 'scapula_joint_flx_muscle' in muscle:    act_mid[muscle] = -95
            elif 'shoulder_joint_ext_muscle' in muscle:   act_mid[muscle] = -95
            elif 'shoulder_joint_flx_muscle' in muscle:   act_mid[muscle] = -95
            elif 'wrist_joint_ext_muscle' in muscle:      act_mid[muscle] = -95
            elif 'wrist_joint_flx_muscle' in muscle:      act_mid[muscle] = -95

        # --- Teensy/Serial Initialization ---
        spike_port = serial.Serial(port=spike_port_name, baudrate=9600, timeout=0.1)
        sense_port = serial.Serial(port=sense_port_name, baudrate=9600, timeout=0.1)
        print("... Teensy Connection Established")

        spike_port.reset_input_buffer()  # Clear any existing data in the buffer
        spike_port.reset_output_buffer() # Clear any existing data in the buffers
        sense_port.reset_input_buffer()  # Clear any existing data in the buffer
        sense_port.reset_output_buffer() # Clear any existing data in the buffer    

        # Potentiometer and pressure sensor calibration
        sense_port.write(bytearray([255]))
        for joint in potentiometer_data.keys():
            potentiometer_data[joint][0] = np.frombuffer(sense_port.read(1), dtype=np.uint8)
        for muscle in pressure_sensor_data.keys():
            pressure_sensor_data[muscle][0] = np.frombuffer(sense_port.read(1), dtype=np.uint8)
        
    
    else:
        pulse_data = np.zeros([len(t), num_spk_out])   # Simulated Teensy pulse data
        pulse_data[0] = np.zeros([num_spk_out])        # For comparison with physical platform

        joint_ang  = {key: np.zeros(num_steps) for key in joint_list}
        muscle_len = {key: np.zeros(num_steps) for key in muscles_list}
        muscle_vel = {key: np.zeros(num_steps) for key in muscles_list}
        muscle_ten = {key: np.zeros(num_steps) for key in muscles_list}

        for joint in joint_ang.keys():
            joint_ang[joint][0] = mujoco_data.qpos[joint_indices[joint]]
        for muscle in muscle_len.keys():
            muscle_len[muscle][0] = mujoco_data.actuator_length[muscle_indices[muscle]]

        # --- Video Rendering ---
        frames = []
        framerate = 60
        renderer = mujoco.Renderer(mujoco_sim, 920,1280)
        plt.figure()
        plt.imshow(sns_model.g_max_non)



    mn_indices = {}
    for ind, name in enumerate(muscles_list):
        if ind < 6:
            mn_indices[name] = ind
        elif 6 <= ind < 12:
            mn_indices[name] = ind + 6
        elif 12 <= ind < 18:
            mn_indices[name] = ind + 6*2
        else:
            mn_indices[name] = ind + 6*3

    # --- Loop Timing Variables ---
    time_print    = 0
    time_sns      = 0
    time_spk      = 0
    time_mujo     = 0
    time_spkqueue = 0
    time_feed     = 0
    time_vid      = 0
    time_mark     = clock.perf_counter()

    # --- Spike and Sensory Data Buffers ---
    spk_packet  = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=bool)

    # --- Time Initialization ---
    t_mark          = clock.perf_counter()
    time_start      = clock.perf_counter()
    sys.stdout.write(f"\n\n\n\n")

    # =============================
    # Main Simulation Loop
    # =============================
    for i in range(1, num_steps):
        # --- Timing: Track time spent in each section ---
        time_print += clock.perf_counter() - time_mark
        time_mark  = clock.perf_counter()

        # --- Step SNS Models ---
        sns_sim_data[i, :] = sns_model(x=sns_inputs)
        time_sns += clock.perf_counter() - time_mark
        time_mark = clock.perf_counter()

        # --- Convert SNS output to spiking inputs ---
        for muscle in muscle_indices.keys():
            spk_inputs[muscle_indices[muscle]] = non_to_spk(x=sns_sim_data[i-1, mn_indices[muscle]], half_point=act_mid[muscle], bandwidth=act_bandwidth[muscle])
        sns_spk_data[i, :] = spk_model(x=spk_inputs)
        spikes_raw = np.array(sns_spk_data[i, :], dtype=bool)
        time_spk += clock.perf_counter() - time_mark
        time_mark = clock.perf_counter()

        # --- Hardware Communication: Muscle Mutt ---
        if muscle_mutt:
            # Accumulate spikes for next comm event
            if np.any(spikes_raw): 
                spk_packet = spk_packet | spikes_raw

            # At comm interval, send spikes and receive sensory data
            if i * dt >= comm_index * comm_dt:               
                # limbs  = np.array([1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0], dtype=bool) #hindlimbs
                # limbs  = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1], dtype=bool) #forelimbs
                limbs  = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=bool) #forelimbs
                spk_packet = spk_packet & limbs
                spk_msg_in_bytes = np.concatenate(([255], np.packbits(spk_packet)))
                # Wait for real time to match simulation
                time_now = clock.perf_counter()
                while time_now < dt * i + time_start:
                    time_sleep = ((dt * i + time_start) - time_now) * 0.9
                    clock.sleep(max(0.0001, time_sleep))
                    time_now = clock.perf_counter()
                # Send spikes
                for byte in spk_msg_in_bytes:
                    spike_port.write(bytes([byte]))
                clock.sleep(0.000001)
                spk_confirmation = np.frombuffer(spike_port.read(4), dtype=np.uint8)
                spk_packet = np.zeros_like(spk_packet, dtype=bool)
                # Get sensory data
                sense_port.write(bytearray([255]))
                for joint in potentiometer_data.keys():
                    if 'L_' in joint:
                        potentiometer_data[joint][comm_index] = - np.frombuffer(sense_port.read(1), dtype=np.uint8)
                    elif 'R_' in joint:
                        potentiometer_data[joint][comm_index] = np.frombuffer(sense_port.read(1), dtype=np.uint8)
                for muscle in pressure_sensor_data.keys():
                    pressure_sensor_data[muscle][comm_index] = np.frombuffer(sense_port.read(1), dtype=np.uint8)

                #  joint/muscle value calculation
                muscle_data(
                    pressure_sensor_data=pressure_sensor_data,
                    potentiometer_data=potentiometer_data,
                    muscle_length_static=muscle_length_static,
                    muscle_length_dynamic=muscle_length_dynamic,
                    muscle_wrap=muscle_wrap,
                    muscle_insertion_rest_polar=muscle_insertion_rest_polar,
                    M=M,
                    Slist=Slist,
                    joint_ang=joint_ang,
                    joint_radius=joint_radius,
                    BPA_L0=BPA_L0,
                    muscle_len=muscle_len,
                    muscle_vel=muscle_vel,
                    muscle_ten=muscle_ten,
                    comm_dt=comm_dt,
                    comm_index=comm_index)
                
                comm_index += 1
                
                # Sync MuJoCo viewer (Verify that the simulation reads is reading sensor data correctly.)

                # viewer.sync()

        time_spkqueue += clock.perf_counter() - time_mark
        time_mark = clock.perf_counter()

        # --- Simulation Communication: MuJoCo ---
        if not muscle_mutt:
            for muscle in muscle_indices.keys():
                mujoco_data.act[muscle_indices[muscle]] = stim_to_act(sns_sim_data[i-1, mn_indices[muscle]])
            for muscle in muscle_indices.keys():
                if sns_spk_data[i, muscle_indices[muscle]] == 1:
                    pulse_data[i:i+int(10 - 1), muscle_indices[muscle]] = 1
                mujoco_data.act[muscle_indices[muscle]] = pulse_data[i, muscle_indices[muscle]]
            mujoco.mj_step(mujoco_sim, mujoco_data)
            time[i] = mujoco_data.time
            for joint in joint_ang.keys():
                joint_ang[joint][i] = mujoco_data.qpos[joint_indices[joint]]
            for muscle in muscle_len.keys():
                muscle_len[muscle][i] = mujoco_data.actuator_length[muscle_indices[muscle]]
                muscle_vel[muscle][i] = mujoco_data.actuator_velocity[muscle_indices[muscle]]
                muscle_ten[muscle][i] = mujoco_data.actuator_force[muscle_indices[muscle]]
            
        # --- Choose Index Based on Control Loop Type ---
        feedback_index = comm_index - 1 if muscle_mutt else i

        # --- Convert Muscle Data to SNS Inputs ---
        L_hip_feedback = hip_inputs(muscle_len['L_hip_joint_ext_muscle'][feedback_index], muscle_len['L_hip_joint_flx_muscle'][feedback_index], muscle_vel['L_hip_joint_ext_muscle'][feedback_index], muscle_vel['L_hip_joint_flx_muscle'][feedback_index], muscle_ten['L_hip_joint_ext_muscle'][feedback_index], muscle_ten['L_hip_joint_flx_muscle'][feedback_index], muscle_len['L_hip_joint_ext_muscle'][0], muscle_len['L_hip_joint_flx_muscle'][0])
        R_hip_feedback = hip_inputs(muscle_len['R_hip_joint_ext_muscle'][feedback_index], muscle_len['R_hip_joint_flx_muscle'][feedback_index], muscle_vel['R_hip_joint_ext_muscle'][feedback_index], muscle_vel['R_hip_joint_flx_muscle'][feedback_index], muscle_ten['R_hip_joint_ext_muscle'][feedback_index], muscle_ten['R_hip_joint_flx_muscle'][feedback_index], muscle_len['R_hip_joint_ext_muscle'][0], muscle_len['R_hip_joint_flx_muscle'][0])
        L_knee_feedback = knee_inputs(muscle_len['L_knee_joint_ext_muscle'][feedback_index], muscle_len['L_knee_joint_flx_muscle'][feedback_index], muscle_vel['L_knee_joint_ext_muscle'][feedback_index], muscle_vel['L_knee_joint_flx_muscle'][feedback_index], muscle_ten['L_knee_joint_ext_muscle'][feedback_index], muscle_ten['L_knee_joint_flx_muscle'][feedback_index], muscle_len['L_knee_joint_ext_muscle'][0], muscle_len['L_knee_joint_flx_muscle'][0])
        R_knee_feedback = knee_inputs(muscle_len['R_knee_joint_ext_muscle'][feedback_index], muscle_len['R_knee_joint_flx_muscle'][feedback_index], muscle_vel['R_knee_joint_ext_muscle'][feedback_index], muscle_vel['R_knee_joint_flx_muscle'][feedback_index], muscle_ten['R_knee_joint_ext_muscle'][feedback_index], muscle_ten['R_knee_joint_flx_muscle'][feedback_index], muscle_len['R_knee_joint_ext_muscle'][0], muscle_len['R_knee_joint_flx_muscle'][0])
        L_ankle_feedback = ankle_inputs(muscle_len['L_ankle_joint_ext_muscle'][feedback_index], muscle_len['L_ankle_joint_flx_muscle'][feedback_index], muscle_vel['L_ankle_joint_ext_muscle'][feedback_index], muscle_vel['L_ankle_joint_flx_muscle'][feedback_index], muscle_ten['L_ankle_joint_ext_muscle'][feedback_index], muscle_ten['L_ankle_joint_flx_muscle'][feedback_index], muscle_len['L_ankle_joint_ext_muscle'][0], muscle_len['L_ankle_joint_flx_muscle'][0])
        R_ankle_feedback = ankle_inputs(muscle_len['R_ankle_joint_ext_muscle'][feedback_index], muscle_len['R_ankle_joint_flx_muscle'][feedback_index], muscle_vel['R_ankle_joint_ext_muscle'][feedback_index], muscle_vel['R_ankle_joint_flx_muscle'][feedback_index], muscle_ten['R_ankle_joint_ext_muscle'][feedback_index], muscle_ten['R_ankle_joint_flx_muscle'][feedback_index], muscle_len['R_ankle_joint_ext_muscle'][0], muscle_len['R_ankle_joint_flx_muscle'][0])
        L_scapula_feedback = scapula_inputs(muscle_len['L_scapula_joint_ext_muscle'][feedback_index], muscle_len['L_scapula_joint_flx_muscle'][feedback_index], muscle_vel['L_scapula_joint_ext_muscle'][feedback_index], muscle_vel['L_scapula_joint_flx_muscle'][feedback_index], muscle_ten['L_scapula_joint_ext_muscle'][feedback_index], muscle_ten['L_scapula_joint_flx_muscle'][feedback_index], muscle_len['L_scapula_joint_ext_muscle'][0], muscle_len['L_scapula_joint_flx_muscle'][0])
        R_scapula_feedback = scapula_inputs(muscle_len['R_scapula_joint_ext_muscle'][feedback_index], muscle_len['R_scapula_joint_flx_muscle'][feedback_index], muscle_vel['R_scapula_joint_ext_muscle'][feedback_index], muscle_vel['R_scapula_joint_flx_muscle'][feedback_index], muscle_ten['R_scapula_joint_ext_muscle'][feedback_index], muscle_ten['R_scapula_joint_flx_muscle'][feedback_index], muscle_len['R_scapula_joint_ext_muscle'][0], muscle_len['R_scapula_joint_flx_muscle'][0])
        L_shoulder_feedback = shoulder_inputs(muscle_len['L_shoulder_joint_ext_muscle'][feedback_index], muscle_len['L_shoulder_joint_flx_muscle'][feedback_index], muscle_vel['L_shoulder_joint_ext_muscle'][feedback_index], muscle_vel['L_shoulder_joint_flx_muscle'][feedback_index], muscle_ten['L_shoulder_joint_ext_muscle'][feedback_index], muscle_ten['L_shoulder_joint_flx_muscle'][feedback_index], muscle_len['L_shoulder_joint_ext_muscle'][0], muscle_len['L_shoulder_joint_flx_muscle'][0])
        R_shoulder_feedback = shoulder_inputs(muscle_len['R_shoulder_joint_ext_muscle'][feedback_index], muscle_len['R_shoulder_joint_flx_muscle'][feedback_index], muscle_vel['R_shoulder_joint_ext_muscle'][feedback_index], muscle_vel['R_shoulder_joint_flx_muscle'][feedback_index], muscle_ten['R_shoulder_joint_ext_muscle'][feedback_index], muscle_ten['R_shoulder_joint_flx_muscle'][feedback_index], muscle_len['R_shoulder_joint_ext_muscle'][0], muscle_len['R_shoulder_joint_flx_muscle'][0])
        L_wrist_feedback = wrist_inputs(muscle_len['L_wrist_joint_ext_muscle'][feedback_index], muscle_len['L_wrist_joint_flx_muscle'][feedback_index], muscle_vel['L_wrist_joint_ext_muscle'][feedback_index], muscle_vel['L_wrist_joint_flx_muscle'][feedback_index], muscle_ten['L_wrist_joint_ext_muscle'][feedback_index], muscle_ten['L_wrist_joint_flx_muscle'][feedback_index], muscle_len['L_wrist_joint_ext_muscle'][0], muscle_len['L_wrist_joint_flx_muscle'][0])
        R_wrist_feedback = wrist_inputs(muscle_len['R_wrist_joint_ext_muscle'][feedback_index], muscle_len['R_wrist_joint_flx_muscle'][feedback_index], muscle_vel['R_wrist_joint_ext_muscle'][feedback_index], muscle_vel['R_wrist_joint_flx_muscle'][feedback_index], muscle_ten['R_wrist_joint_ext_muscle'][feedback_index], muscle_ten['R_wrist_joint_flx_muscle'][feedback_index], muscle_len['R_wrist_joint_ext_muscle'][0], muscle_len['R_wrist_joint_flx_muscle'][0])
        time_mujo += clock.perf_counter() - time_mark
        time_mark = clock.perf_counter()
        # --- Concatenate all feedback for SNS input ---
        L_sns_inputs_hind = np.concatenate((L_hip_feedback, L_knee_feedback, L_ankle_feedback, cpg_inputs[i,:]))
        R_sns_inputs_hind = np.concatenate((R_hip_feedback, R_knee_feedback, R_ankle_feedback, cpg_inputs[i,:]))
        L_sns_inputs_fore = np.concatenate((L_scapula_feedback, L_shoulder_feedback, L_wrist_feedback, cpg_inputs[i,:]))
        R_sns_inputs_fore = np.concatenate((R_scapula_feedback, R_shoulder_feedback, R_wrist_feedback, cpg_inputs[i,:]))
        sns_inputs = np.concatenate((R_sns_inputs_hind, L_sns_inputs_hind, R_sns_inputs_fore, L_sns_inputs_fore))
        time_feed += clock.perf_counter() - time_mark
        time_mark = clock.perf_counter()

        # --- Video Frame Rendering ---
        if make_vid:
            if len(frames) < mujoco_data.time * framerate:
                renderer.update_scene(mujoco_data, camera='close')
                pixels = renderer.render().copy()
                frames.append(pixels)
        time_vid += clock.perf_counter() - time_mark
        time_mark = clock.perf_counter()

    ###################################################################################
    ############################ Misc. Post-loop Actions ##############################
    ###################################################################################
    time_loop = clock.perf_counter() - time_start   # Calculate the actual simulation time

    if make_vid == True:
        media.write_video('full_hindlimb_sim.mp4', frames, fps=framerate)

    data = 'data'

    np.save(f'Python/{data}/comm_times.npy', np.arange(comm_index*comm_dt*1000))
    np.save(f'Python/{data}/time.npy', time)
    np.save(f'Python/{data}/sns_sim_data.npy', sns_sim_data)
    np.save(f'Python/{data}/sns_spk_data.npy', sns_spk_data)
    np.save(f'Python/{data}/joint_ang.npy', joint_ang)
    np.save(f'Python/{data}/muscle_len.npy', muscle_len)
    np.save(f'Python/{data}/muscle_vel.npy', muscle_vel)
    np.save(f'Python/{data}/muscle_ten.npy', muscle_ten)

    # cost = plot_gaits(time, joint_ang)
    # plot_length(time, muscle_len)
    # plot_velocity(time, muscle_vel)
    # plot_joint(time, joint_ang)
    plot_sns(t, sns_sim_data.T)
    plot_spk(t, sns_spk_data.T)
    # Use combined per-leg master plot (angle, length, velocity)
    plot_legs_master_summary(np.arange(comm_index)*comm_dt*1000, joint_ang, muscle_len, muscle_vel, muscle_ten)
    
    times = [time_print, time_sns, time_spk, time_spkqueue, time_mujo, time_feed, time_vid, time_loop]
    plot_times(times)

    # teensy_queue.put(None)
    # teensy_thread.join()
    
    sns_sim_data = sns_sim_data.T
    plt.figure()
    plt.plot(t, sns_sim_data[:][0], color='red')
    plt.plot(t, sns_sim_data[:][1], color='green')
    plt.plot(t, sns_sim_data[:][12], color='red', ls='--')
    plt.plot(t, sns_sim_data[:][13], color='green', ls='--')

    if muscle_mutt:
        spike_port.flush()
        sense_port.flush()

    return # cost

def main():
    """
    Runs a simulation of rat hindlimbs movement using a Two-layer CPG SNS integrated with a Mujoco physics engine.

    This function sets up parameters such as simulation duration (`end_time`), time step (`dt`), Mujoco XML model path (`xml_path`), 
    and neural network inputs (`cpg_inputs`). It then calls the `run_sims()` function to perform the simulation and save the results.

    Parameters:
    None

    Returns:
    None

    Sets up threads which run synthetic nervous system.

    Functions:
    sim_thread: runs the simulation containing the SNS
    dat_thread: handles data receiving and sending between the simulation and Teensy
    """

    feed_fwd    = False
    muscle_mutt = True
    make_vid    = False

    spike_port_name = "COM5" # port to send spikes to the Teensy
    sense_port_name = "COM4" # port from Teensy which obtains sense data
    xml_path = 'python/quadruped_model.xml' # quadruped robot mujoco model path
    data_location = 'data' # location to save data

    cpg_gsyn = 1.3  # defines RG oscillation speed (small adjustments make a big difference!)
    end_time = 5    # simulation end seconds
    dt = 1/1000     # simulation step size (1 ms is pretty large)
    num_steps = int(end_time/dt)    # Do not edit
    comm_freq = 50 # on the Windows, 50Hz communication frequency is ther max, real-time frequency. 
    num_comms = int(comm_freq * end_time)
    Iapp =  np.zeros([num_steps,1]) # Do not edit
    Ipert = np.zeros([num_steps,1]) # Do not edit
    Ipert[1] = 1 # kick start the rhythm generators
    cpg_inputs = Iapp + Ipert       # Do not edit

    cost = run_sims(dt=dt, 
                    num_steps=num_steps, 
                    end_time=end_time, 
                    comm_freq=comm_freq,
                    num_comms=num_comms,
                    xml_path=xml_path, 
                    cpg_inputs=cpg_inputs, 
                    cpg_gsyn=cpg_gsyn, 
                    feed_forward=feed_fwd,
                    muscle_mutt=muscle_mutt,
                    make_vid=make_vid,
                    spike_port_name=spike_port_name,
                    sense_port_name=sense_port_name,
                    data_location=data_location)
    return cost


if __name__ == '__main__':
    print("\n")
    print("... Program Started")
    main()
    print("\n", "... Simulation and Storage Complete")
    print("\n")
    # print(muscle_indeces)
    # plt.show()