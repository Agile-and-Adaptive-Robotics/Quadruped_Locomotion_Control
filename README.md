 # Quadruped_Locomotion_Control
A comprehensive repository for controlling locomotion in the AARL's "Muscle Mutt", detailed in the "Quadruped_Robot" repository. The SNS is based on work by Clayton Jackson, and the communication protocol is grounded in work by Stu McNeal.

# System Overview


It is fairly complicated to generate stable locomotion in a quadrupedal robot, and doing so with spike activations to BPAs is a novel method.
In addition, neural systems are notoriously difficult to tune; though, when done so properly, they can be a robust control method.

This work bridges the gap between a synthetic nervous system, tuned to generate stable walking in the hind limbs of a rat model, and a quadruped robot.
The quadruped robot in question is Muscle Mutt, the BPA-actuated platform used in the Agile and Adaptive Robotics lab as a means of testing biologically-plausible neural controllers.
Thus, this works attempts to provide a structure for "controller interfaces" which bridge the gaps in the many-input/many-output control scheme to create locomotion in the quadruped robot. 

I will breifly describe the physical platform, Muscle Mutt, and its set of BPA valves, BPAs, BPA pressure sensors, and joint angle sensors (potentiometers).
However, an in depth description of Muscle Mutt's development can be found in Cody Scharzenberger's masters thesis.
Additionally, I will also discuss the modifications to Clayton Jackson's rat model (which recreates the results of Kaiyu Deng's research). 
However, I will, once again, leave the in depth discussion of dual-layered CPG structure to the research of dual-layered CPGs.
I will also discuss the developmemt of controller interfaces, which run on Teensy 4.1 microcontrollers and convert between high and low-level signals throughout the control loop.

<img width="1499" height="755" alt="Screenshot 2025-08-10 at 7 07 29 PM" src="https://github.com/user-attachments/assets/7fd20f22-52f9-47d0-adee-f25aa41b55e1" />

## Teensy 4.1

There are two components to the Teensy code.

### Spike Activation Pipeline

The first recieves spike data from dog_sitter.py, and activates the muscles on Muscle Mutt using Stu McNeal's [Robot Control](https://github.com/Agile-and-Adaptive-Robotics/Robot-Control) repo.

### Sensory Data Pipeline

The second piece of code is uploaded to the Sensory Feedback Teensy, which currently handles potentiometer and pressure sensor data.
As Python, via the PC, handles all control process timing, the Teensy is waiting until a specific byte is recieved and validated over serial.
When a data request byte is recieved, the data from 12 potentiometers (one at each joint) and 24 pressure sensors (within each BPA) is read by sampling pins from multiplexers.
Data from each pin is limited to a single byte, for speed of transmission.
The data is packed into a 36-byte array, and written over serial. 
Python recieves 



## Python

Open the file dog_sitter.py (contained within the Python directory) in your editor of choice.
I prefer to use [VSCode](https://code.visualstudio.com), as it is very versatile and has a built-in terminal.

### Modes of Operation

One can select modes of operation in main() of dog_sitter.py.

```
feed_fwd    = True
muscle_mutt = True
make_vid    = False
```

#### Feed Forward

If the boolean feed_fwd is selected, the connection between the pattern formation and motoneuron layers are strengthened in sns_network_model.py. 
In addition, all calculated feedback is overwritten by small, but constant values. 
This general configuration allows one to test the SNS on the MuJoCo or Muscle Mutt as a more simplistic model.


Note that I did not validate the reasonability of the strengths of the connections in this SNS model.
This setting was to test the effectiveness of the spike communication protocol without sensory feedback, which we did not have at the time.

#### Muscle Mutt

If this is selected as false, the MuJoCo simulation is initialized.
Feedback is taken from MuJoCo data and processed using equations adapted by Clayton Jackson.

Otherwise, if this option is set to true, the controls scheme is configured for controlling Muscle Mutt.
This includes the initialization of the serial ports for the spike and sensory data, as well as the functions which convert potentiometer and pressure sensor data to muscle length, velocity, and tension.
 
##### Muscle Data in Simulation

In the setup by Clayton Jackson, all muscle data (i.e. length, velocity, and tension) is collected directly from MuJoCo using the handy fields "actuator_length", "actuator_velocity", etc.
While joint angle was collected, it was only used for plotting and analysis post-simulation.
We do not have the luxury of reading sensor outputs directly with Muscle Mutt.
Thus, it is necessary that we interpolate muscle data to be fed into the SNS using the available data.
We have joint data in the form of potentiometer readings (0-255), as well as pressure data from pressure sensors within the muscles (also processed as a digital value.



#### Make Video

Originally built by Clayton Jackson, this option builds a video from the MuJoCo simulation frames, if the MuJoCo option was selected.

Note: Video creation eats a huge amount of loop time, so only use this method if you don't expect the simulation to run in real time. 

### Serial Pipeline

Sendospiko sends and recieves spikes, using a queue to buffer the spikes being sent.
It is run as a separate thread called inside of the loop. This is so that the serial handling does not dominate simulation loop use.
    
teensy_queue: Defined outside of function, stores a queue of spikes accessable from inside and outside of thread.

### A Troubleshooting Note: Path Names

It is very likely that you will need to update the path and port names within the dog_sitter.py code.
For example, "anim_data" is pulled from 'python/JA.csv'.
However, this reference depends on my configuration of the project within the VSCode ("Quadruped" is my workspace folder.)


Likewise, the actual Teensy port names depend exclusively on the device to which they are attached.
These can be found by connecting the Teensy microcontrollers in their ultimate configuration and reading the port names from the Arduino IDE.
 