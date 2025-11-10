
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
import modern_robotics as mr  # MJL: I HAVE TO COMMENT THIS OUT ON MY LAPTOP
import mujoco
import mujoco.viewer
import mediapy as media
import matplotlib.pyplot as plt
import scipy.signal
from scipy.signal import find_peaks
import serial
from queue import Queue
from sns_network_model import build_net, spike_net


# =============================
# Path Setup
# =============================
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

# Plotter Function entirely vibe-coded with ChatGPT 
# Sorry, Leo, if this doesn't make sense, code-wise. *I* wouldn't be able to tell you what all the little variables are.
# I bet I could give a good guess though!
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

def muscle_data(
            pressure_sensor_data,
            potentiometer_data,
            muscle_length_static,
            muscle_length_dynamic,
            muscle_wrap,
            M,
            Slist,
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
    angle_conversion = -np.deg2rad(299.1) / 255.0

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

    # Inidialize communication timesteps and time vectors!
    comm_dt    = 1 / comm_freq       # Communication period (s)
    comm_index = 0               # Communication event counter

    t = np.arange(0, num_steps)
    time = np.zeros([len(t)])

    # MuJoCo and SNS model initialization
    mujoco_dt = dt
    sns_dt = mujoco_dt * 1000
    mujoco_sim, mujoco_data = mujoco_model(xml_path)
    mujoco_sim.opt.timestep = mujoco_dt
    sns_model = build_net(dt=sns_dt, cpg_gsyn=cpg_gsyn, feed_forward=feed_forward)
    spk_model = spike_net(dt=sns_dt) # Nonspiking to spiking conversion network

    # ----------- DATA STRUCTURES ----------- 

    # DATA STRUCTURES for SNS
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

    # This is a convenient way to determine the indices of ALL MuJoCo objects 
    muscles_list = [mujoco.mj_id2name(mujoco_sim, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(mujoco_sim.nu)]
    all_joint_names = [mujoco.mj_id2name(mujoco_sim, mujoco.mjtObj.mjOBJ_JOINT, i) for i in range(mujoco_sim.njnt)]
    joint_list = [name for name in all_joint_names if any(keyword in name for keyword in ['hip', 'knee', 'ankle', 'scapula', 'shoulder', 'wrist'])]
    
    # Link indices to their keys in a dictionary, so that we can reference them directly by name later
    muscle_indices = {name: mujoco.mj_name2id(mujoco_sim, mujoco.mjtObj.mjOBJ_ACTUATOR, name) for name in  muscles_list}
    time_start      = clock.perf_counter()

    spike_port = serial.Serial(port=spike_port_name, baudrate=9600, timeout=0.1)

    print(muscle_indices)

    # =============================
    # Main Simulation Loop
    # =============================
    for muscle in muscles_list[0:12]:
        # --- Timing: Track time spent in each section ---

        input()

        spk_packet  = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=bool)
        spk_packet[muscle_indices[muscle]] = 1
        spk_packet[muscle_indices[muscle]+12] = 1

        print(muscle, muscles_list[muscle_indices[muscle]+12])

        spk_msg_in_bytes = np.concatenate(([255], np.packbits(spk_packet)))

        for byte in spk_msg_in_bytes:
            spike_port.write(bytes([byte]))
        clock.sleep(0.000001)
        spk_confirmation = np.frombuffer(spike_port.read(4), dtype=np.uint8)
        spk_packet = np.zeros_like(spk_packet, dtype=bool)

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

    feed_fwd    = False  # If true : runs in feedforward mode (no feedback to SNS)
                         # If false: operates with feedback to SNS
    muscle_mutt = True  # If true : configured for communication to Muscle Mutt robot
                         # If false: configured for communication to MuJoCo Model
    
    if not muscle_mutt:  # If true: generate video of MuJoCo simulation
        make_vid = True
    else:
        make_vid = False

    spike_port_name = "COM5" # port to send spikes to the Teensy
    sense_port_name = "COM4" # port from Teensy which obtains sense data
    xml_path = 'python/quadruped_model.xml' # quadruped robot mujoco model path
    # if muscle_mutt:
    data_location = 'data' # location to save data
    # else:
    #     data_location = '/Users/jacklutz/Desktop/1_Academic/1_MJL_Research/2_Writing/MJL_Thesis/1_chapter/figures/results/data_MuJoCo'

    cpg_gsyn = 1.49167  # defines RG oscillation speed (small adjustments make a big difference!)
    end_time = 15    # simulation end seconds
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
