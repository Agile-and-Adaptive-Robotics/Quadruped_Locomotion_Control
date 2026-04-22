import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from sns_toolbox.networks import Network #, AdditionNetwork (This would import the code that we remake here
from sns_toolbox.neurons import NonSpikingNeuron, SpikingNeuron
from sns_toolbox.connections import NonSpikingSynapse
from sns_toolbox.neurons import  NonSpikingNeuronWithPersistentSodiumChannel
from sns_toolbox.renderer import render
import matplotlib.pyplot as plt


class MotorCircuit(Network): # Note that this network is also a preset available from sns_toolbox.networks
    '''
    Motor Unit netwok
    :param name:        Name of this network and all neurons prefix. Should be Hip/knee/ankle. Default is 'Hip'.
    :type name:         str, optional
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        base_neuron =  NonSpikingNeuron(name='Ia', color='red', membrane_capacitance=5.0, membrane_conductance=1, resting_potential=-60)
        motor_neuron = NonSpikingNeuron(name='MN', color='green', membrane_capacitance=5.0, membrane_conductance=1, resting_potential=-100.0)

        #CMM
        self.add_neuron(motor_neuron, name='MN_ext', color='lightcoral') 
        self.add_neuron(motor_neuron, name='MN_flx', color='mediumseagreen')    
        self.add_neuron(base_neuron, name='Ia_ext', color='lightcoral')
        self.add_neuron(base_neuron, name='Ia_flx', color='mediumseagreen')    
        self.add_neuron(base_neuron, name='RC_ext', color='lightcoral')
        self.add_neuron(base_neuron, name='RC_flx', color='mediumseagreen')   
        #Feedback neurons
        self.add_neuron(base_neuron, name='IaIN_ext', color='lightcoral') 
        self.add_neuron(base_neuron, name='IaIN_flx', color='mediumseagreen') 
        self.add_neuron(base_neuron, name='IbIN_ext', color='lightcoral') 
        self.add_neuron(base_neuron, name='IbIN_flx', color='mediumseagreen') 
        
        #define CMM synapses
        Ia_flx_Ia_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)   # inhibit
        Ia_ext_Ia_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)   # inhibit
        Ia_flx_mn_ext = NonSpikingSynapse(max_conductance=2.0, reversal_potential=-100,e_hi=-40, e_lo=-60)  # inhibit
        Ia_ext_mn_flx = NonSpikingSynapse(max_conductance=2.0, reversal_potential=-100,e_hi=-40, e_lo=-60)  # inhibit
        mn_flx_rc_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40,e_hi=-10, e_lo=-100)  # excite
        mn_ext_rc_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40,e_hi=-10, e_lo=-100)  # excite
        rc_ext_Ia_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)   # inhibit
        rc_flx_Ia_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)   # inhibit
        rc_ext_mn_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-100,e_hi=-40, e_lo=-60)  # inhibit
        rc_flx_mn_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-100,e_hi=-40, e_lo=-60)  # inhibit
        rc_flx_rc_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)   # inhibit
        rc_ext_rc_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)   # inhibit

        self.add_connection(Ia_flx_Ia_ext, 'Ia_flx', 'Ia_ext')
        self.add_connection(Ia_ext_Ia_flx, 'Ia_ext', 'Ia_flx')
        self.add_connection(Ia_flx_mn_ext, 'Ia_flx', 'MN_ext')
        self.add_connection(Ia_ext_mn_flx, 'Ia_ext', 'MN_flx')
        self.add_connection(mn_flx_rc_flx, 'MN_flx', 'RC_flx') # excite
        self.add_connection(mn_ext_rc_ext, 'MN_ext', 'RC_ext') # excite
        self.add_connection(rc_ext_Ia_ext, 'RC_ext', 'Ia_ext')
        self.add_connection(rc_flx_Ia_flx, 'RC_flx', 'Ia_flx')
        self.add_connection(rc_ext_mn_ext, 'RC_ext', 'MN_ext')
        self.add_connection(rc_flx_mn_flx, 'RC_flx', 'MN_flx')
        self.add_connection(rc_flx_rc_ext, 'RC_flx', 'RC_ext')
        self.add_connection(rc_ext_rc_flx, 'RC_ext', 'RC_flx')

        Ib2MN_flx = NonSpikingSynapse(max_conductance=1.0, reversal_potential=-10, e_hi=-40, e_lo=-60)      # excite
        Ib2MN_ext = NonSpikingSynapse(max_conductance=0.59, reversal_potential=-10, e_hi=-40, e_lo=-60)     # excite
        IaIn2Iaflx = NonSpikingSynapse(max_conductance=0.695, reversal_potential=-40, e_hi=-40, e_lo=-60)   # excite    
        IaIn2Iaext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40, e_hi=-40, e_lo=-60)     # excite
        IaIN2MNflx = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)       # excite
        IaIN2MNext = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)       # excite

        self.add_connection(Ib2MN_ext, 'IbIN_ext', 'MN_ext')
        self.add_connection(Ib2MN_flx, 'IbIN_flx', 'MN_flx')
        self.add_connection(IaIn2Iaflx, 'IaIN_flx', 'Ia_flx')
        self.add_connection(IaIn2Iaext, 'IaIN_ext', 'Ia_ext')

        self.add_input('IaIN_ext')
        self.add_input('IaIN_flx')
        self.add_input('IbIN_ext')
        self.add_input('IbIN_flx')

        self.add_output('MN_ext')
        self.add_output('MN_flx')

def build_limbs(neuron_params):

    net = Network('limb')

    Cm =         neuron_params["Cm"]
    Gm =         neuron_params["Gm"]
    Ena =        neuron_params["Ena"]
    Er =         neuron_params["Er"]
    Sm =         neuron_params["Sm"]
    Sh =         neuron_params["Sh"]
    Km =         neuron_params["Km"]
    Kh =         neuron_params["Kh"]
    Em =         neuron_params["Em"]
    Eh =         neuron_params["Eh"]
    tauHmax =    neuron_params["tauHmax"]
    Gna =        neuron_params["Gna"]
    cpg_gsyn =   neuron_params["cpg_gsyn"] #Synaptic Conductance

    delEna = Ena
    delEm = Em
    delEh = Eh

    # reformat for sns-toolbox
    g_ion = [Gna]
    e_ion = [delEna]
    k_m = [Km]
    slope_m = [Sm]
    e_m = [delEm]
    k_h = [Kh]
    slope_h = [Sh]
    e_h = [delEh]
    tau_max_h = [tauHmax]

    # defining cpg neurons    
    HC_neuron = NonSpikingNeuronWithPersistentSodiumChannel(membrane_capacitance=Cm, membrane_conductance=Gm,
                                                                g_ion=g_ion,e_ion=e_ion,
                                                                k_m=k_m,slope_m=slope_m,e_m=e_m,
                                                                k_h=k_h,slope_h=slope_h,e_h=e_h,tau_max_h=tau_max_h,
                                                                name='HC',color='orange', resting_potential=Er , bias = 0.0)
    
    # # # defining cpg neurons    
    # # Cm = 20
    # # tau_max_h = [500] # Slow DOOOOOWN RG 
    # RG_HC_neuron = NonSpikingNeuronWithPersistentSodiumChannel(membrane_capacitance=Cm, membrane_conductance=Gm,
    #                                                             g_ion=g_ion,e_ion=e_ion,
    #                                                             k_m=k_m,slope_m=slope_m,e_m=e_m,
    #                                                             k_h=k_h,slope_h=slope_h,e_h=e_h,tau_max_h=tau_max_h,
    #                                                             name='HC',color='orange', resting_potential=Er , bias = 0.0)
    
    interneuron = NonSpikingNeuron(membrane_capacitance=Cm, membrane_conductance=Gm, resting_potential=Er, name='IN', color='blue')

    #define cpg synapses
    HC2IN = NonSpikingSynapse(max_conductance=cpg_gsyn, reversal_potential= -40, e_hi = -40, e_lo = -60)
    IN2HC = NonSpikingSynapse(max_conductance=cpg_gsyn, reversal_potential= -70, e_hi = -40, e_lo = -60)
    
    #add the RG neurons
    net.add_neuron(HC_neuron, 'RG_HC_ext')
    net.add_neuron(HC_neuron, 'RG_HC_flx')
    net.add_neuron(interneuron, 'RG_IN_ext')
    net.add_neuron(interneuron, 'RG_IN_flx')

    #connect the RG
    net.add_connection(HC2IN, 'RG_HC_ext', 'RG_IN_ext')
    net.add_connection(HC2IN, 'RG_HC_flx', 'RG_IN_flx')
    net.add_connection(IN2HC, 'RG_IN_ext', 'RG_HC_flx')
    net.add_connection(IN2HC, 'RG_IN_flx', 'RG_HC_ext')
    # net.add_connection(Gw, 'RG_HC_ext', 'RG_HC_flx')
    # net.add_connection(Gw, 'RG_HC_flx', 'RG_HC_ext')
    
    #add the hip PF layer
    net.add_neuron(HC_neuron, 'PF_HC_ext_Hip')
    net.add_neuron(HC_neuron, 'PF_HC_flx_Hip')
    net.add_neuron(interneuron, 'PF_IN_ext_Hip')
    net.add_neuron(interneuron, 'PF_IN_flx_Hip')

    #connect the Hip_PF
    net.add_connection(HC2IN, 'PF_HC_ext_Hip', 'PF_IN_ext_Hip')
    net.add_connection(HC2IN, 'PF_HC_flx_Hip', 'PF_IN_flx_Hip')
    net.add_connection(IN2HC, 'PF_IN_ext_Hip', 'PF_HC_flx_Hip')
    net.add_connection(IN2HC, 'PF_IN_flx_Hip', 'PF_HC_ext_Hip')

    #add the knee&ankle PF layer
    net.add_neuron(HC_neuron, 'KA_PF_HC_ext')
    net.add_neuron(HC_neuron, 'KA_PF_HC_flx')
    net.add_neuron(interneuron, 'KA_PF_IN_ext')
    net.add_neuron(interneuron, 'KA_PF_IN_flx')

    #connect the KA_PF
    net.add_connection(HC2IN, 'KA_PF_HC_ext', 'KA_PF_IN_ext')
    net.add_connection(HC2IN, 'KA_PF_HC_flx', 'KA_PF_IN_flx')
    net.add_connection(IN2HC, 'KA_PF_IN_ext', 'KA_PF_HC_flx')
    net.add_connection(IN2HC, 'KA_PF_IN_flx', 'KA_PF_HC_ext')

    # RG -> PF
    RG2PF_hip = NonSpikingSynapse(max_conductance=1.0,  reversal_potential=-40, e_hi=-40, e_lo=-59)
    RG2PF_KA = NonSpikingSynapse(max_conductance=0.8, reversal_potential=-40, e_hi=-40, e_lo=-59)
    
    net.add_connection(RG2PF_hip, 'RG_HC_ext', 'PF_HC_ext_Hip')
    net.add_connection(RG2PF_hip, 'RG_HC_flx', 'PF_HC_flx_Hip')
    net.add_connection(RG2PF_KA, 'RG_HC_ext', 'KA_PF_HC_ext')
    net.add_connection(RG2PF_KA, 'RG_HC_flx', 'KA_PF_HC_flx')

    #add the motor circuits
    motor_circuit = MotorCircuit()

    net.add_network(motor_circuit, suffix='_Hip') 
    IaIN2MNflx = NonSpikingSynapse(max_conductance=0.1, reversal_potential=0, e_hi=-40, e_lo=-60)
    IaIN2MNext = NonSpikingSynapse(max_conductance=0.1, reversal_potential=0, e_hi=-40, e_lo=-60)
    net.add_neuron(interneuron, name='II_IN_ext_Hip', color='lightcoral') 
    net.add_neuron(interneuron, name='II_IN_flx_Hip', color='mediumseagreen') 
    net.add_input('II_IN_ext_Hip')
    net.add_input('II_IN_flx_Hip')
    net.add_connection(IaIN2MNflx, 'IaIN_flx_Hip', 'MN_flx_Hip')
    net.add_connection(IaIN2MNext, 'IaIN_ext_Hip', 'MN_ext_Hip')

    net.add_network(motor_circuit, suffix='_Knee') 
    
    net.add_network(motor_circuit, suffix='_Ankle') 
    ankle_II_flx2ankleMNflx = NonSpikingSynapse(max_conductance=0.47, reversal_potential=-10, e_hi=-40, e_lo=-60)
    net.add_neuron(interneuron, 'II_IN_flx_Ankle')
    net.add_connection(ankle_II_flx2ankleMNflx ,'II_IN_flx_Ankle','MN_flx_Ankle')
    net.add_input('II_IN_flx_Ankle')


    # PF -> Ib IN inhibit
    pf2Ib = NonSpikingSynapse(max_conductance=2, reversal_potential=-60, e_hi=-59, e_lo=-60)

    net.add_connection(pf2Ib, 'PF_HC_flx_Hip','IbIN_ext_Hip')
    net.add_connection(pf2Ib, 'PF_HC_ext_Hip','IbIN_flx_Hip')
    net.add_connection(pf2Ib, 'KA_PF_HC_flx','IbIN_ext_Knee')
    net.add_connection(pf2Ib, 'KA_PF_HC_ext','IbIN_flx_Knee')
    net.add_connection(pf2Ib, 'KA_PF_HC_flx','IbIN_ext_Ankle')
    net.add_connection(pf2Ib, 'KA_PF_HC_ext','IbIN_flx_Ankle')

    # PF -> Motor Circuits
    PF2Ia = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40, e_hi=-55, e_lo=-60)

    PF2HipMN_ext = NonSpikingSynapse(max_conductance=2.565*0.15*4, reversal_potential=-10, e_hi=-50, e_lo=-60)
    PF2HipMN_flx = NonSpikingSynapse(max_conductance=3.632*0.07*4, reversal_potential=-10, e_hi=-50, e_lo=-60)

    PF2KneeMN_ext = NonSpikingSynapse(max_conductance=2.1, reversal_potential=-40, e_hi=-50, e_lo=-60)
    PF2KneeMN_flx = NonSpikingSynapse(max_conductance=1.6, reversal_potential=-40, e_hi=-50, e_lo=-60)

    PF2AnkleMN_ext = NonSpikingSynapse(max_conductance=2.7, reversal_potential=-10, e_hi=-50, e_lo=-60)
    PF2AnkleMN_flx = NonSpikingSynapse(max_conductance=4.4, reversal_potential=-40, e_hi=-50, e_lo=-60)
    
    net.add_connection(PF2Ia, 'PF_HC_ext_Hip','Ia_ext_Hip')
    net.add_connection(PF2Ia, 'PF_HC_flx_Hip','Ia_flx_Hip')
    net.add_connection(PF2Ia, 'KA_PF_HC_ext','Ia_ext_Knee')
    net.add_connection(PF2Ia, 'KA_PF_HC_flx','Ia_flx_Knee')
    net.add_connection(PF2Ia, 'KA_PF_HC_ext','Ia_ext_Ankle')
    net.add_connection(PF2Ia, 'KA_PF_HC_flx','Ia_flx_Ankle')

    net.add_connection(PF2HipMN_ext, 'PF_HC_ext_Hip','MN_ext_Hip')
    net.add_connection(PF2HipMN_flx, 'PF_HC_flx_Hip','MN_flx_Hip')
    net.add_connection(PF2KneeMN_ext, 'KA_PF_HC_ext','MN_ext_Knee')
    net.add_connection(PF2KneeMN_flx, 'KA_PF_HC_flx','MN_flx_Knee')
    net.add_connection(PF2AnkleMN_ext, 'KA_PF_HC_ext','MN_ext_Ankle')
    net.add_connection(PF2AnkleMN_flx, 'KA_PF_HC_flx','MN_flx_Ankle')

    # # feedback to PF and RG layers
    HipII_flx2RG_IN_ext = NonSpikingSynapse(max_conductance=0.1, reversal_potential=-70, e_hi=-45, e_lo=-60)
    HipII_ext2RG_IN_flx = NonSpikingSynapse(max_conductance=0.1, reversal_potential=-70, e_hi=-40, e_lo=-55)
    HipII_flx2Hip_PF_IN_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70, e_hi=-30, e_lo=-50)
    HipII_ext2Hip_PF_IN_flx = NonSpikingSynapse(max_conductance=0.2, reversal_potential=-70, e_hi=-30, e_lo=-50)
    HipII_flx2KA_PF_IN_ext = NonSpikingSynapse(max_conductance=0.2, reversal_potential=-70, e_hi=-35, e_lo=-55)
    HipII_ext2KA_PF_IN_flx = NonSpikingSynapse(max_conductance=0.8, reversal_potential=-70, e_hi=-40, e_lo=-50)
    AnkleIb_ext2KA_PF_IN_ext = NonSpikingSynapse(max_conductance=0.1, reversal_potential=-70, e_hi=-45, e_lo=-60)
    AnkleIb_ext2RG_IN_ext = NonSpikingSynapse(max_conductance=0.01, reversal_potential=-30, e_hi=-55, e_lo=-80) ##excite
    HipIa_flx2RG_IN_ext = NonSpikingSynapse(max_conductance=0, reversal_potential=-60, e_hi=-45, e_lo=-60) ##inhibit

    net.add_connection(HipII_flx2RG_IN_ext, 'II_IN_flx_Hip','RG_IN_ext')
    net.add_connection(HipII_ext2RG_IN_flx, 'II_IN_ext_Hip','RG_IN_flx')
    net.add_connection(HipII_flx2Hip_PF_IN_ext, 'II_IN_flx_Hip', 'PF_IN_ext_Hip')
    net.add_connection(HipII_ext2Hip_PF_IN_flx, 'II_IN_ext_Hip', 'PF_IN_flx_Hip')
    net.add_connection(HipII_flx2KA_PF_IN_ext, 'II_IN_flx_Hip', 'KA_PF_IN_ext')
    net.add_connection(HipII_ext2KA_PF_IN_flx, 'II_IN_ext_Hip', 'KA_PF_IN_flx')
    net.add_connection(AnkleIb_ext2KA_PF_IN_ext, 'IbIN_ext_Ankle', 'KA_PF_IN_ext')
    net.add_connection(AnkleIb_ext2RG_IN_ext, 'IbIN_ext_Ankle', 'RG_IN_ext')
    net.add_connection(HipIa_flx2RG_IN_ext, 'IaIN_flx_Hip', 'RG_IN_ext')

    net.add_output('RG_HC_ext')
    net.add_output('RG_HC_flx')

    net.add_output('PF_HC_ext_Hip')
    net.add_output('PF_HC_flx_Hip')
    net.add_output('KA_PF_HC_ext')
    net.add_output('KA_PF_HC_flx')

    render(net, view=False, save=True, filename='python/fig_networks/leo_motor', img_format='png')

    return net


def spike_net(dt = 0.01, fore_limbs = False):
    spike_network = Network('SpikeNet')

    motor_neuron_spk = SpikingNeuron(name='MN_spk', color='yellow', threshold_initial_value = 1, threshold_time_constant = 50, membrane_capacitance = 50)

    spike_network.add_neuron(motor_neuron_spk, name='R_hip_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_hip_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_knee_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_knee_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_ankle_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_ankle_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_hip_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_hip_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_knee_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_knee_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_ankle_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_ankle_flx_muscle', color='blue')

        ### forelimb hindlimb spiking network
    spike_network.add_neuron(motor_neuron_spk, name='R_scapula_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_scapula_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_shoulder_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_shoulder_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_wrist_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='R_wrist_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_scapula_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_scapula_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_shoulder_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_shoulder_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_wrist_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_spk, name='L_wrist_flx_muscle_forelimb', color='blue')

    spike_network.add_output('R_hip_ext_muscle'  ,spiking=True)
    spike_network.add_output('R_hip_flx_muscle'  ,spiking=True)
    spike_network.add_output('R_knee_ext_muscle' ,spiking=True)
    spike_network.add_output('R_knee_flx_muscle' ,spiking=True)
    spike_network.add_output('R_ankle_ext_muscle',spiking=True)
    spike_network.add_output('R_ankle_flx_muscle',spiking=True)
    spike_network.add_output('L_hip_ext_muscle'  ,spiking=True)
    spike_network.add_output('L_hip_flx_muscle'  ,spiking=True)
    spike_network.add_output('L_knee_ext_muscle' ,spiking=True)
    spike_network.add_output('L_knee_flx_muscle' ,spiking=True)
    spike_network.add_output('L_ankle_ext_muscle',spiking=True)
    spike_network.add_output('L_ankle_flx_muscle',spiking=True)

    if fore_limbs:
        spike_network.add_output('R_scapula_ext_muscle_forelimb',spiking=True)
        spike_network.add_output('R_scapula_flx_muscle_forelimb',spiking=True)
        spike_network.add_output('R_shoulder_ext_muscle_forelimb',spiking=True)
        spike_network.add_output('R_shoulder_flx_muscle_forelimb',spiking=True)
        spike_network.add_output('R_wrist_ext_muscle_forelimb',spiking=True)
        spike_network.add_output('R_wrist_flx_muscle_forelimb',spiking=True)
        spike_network.add_output('L_scapula_ext_muscle_forelimb',spiking=True)
        spike_network.add_output('L_scapula_flx_muscle_forelimb',spiking=True)
        spike_network.add_output('L_shoulder_ext_muscle_forelimb',spiking=True)
        spike_network.add_output('L_shoulder_flx_muscle_forelimb',spiking=True)
        spike_network.add_output('L_wrist_ext_muscle_forelimb',spiking=True)
        spike_network.add_output('L_wrist_flx_muscle_forelimb',spiking=True)
    
    else:
        # Create a dummy set of dummy outputs so that data collection remains the same in dog_sitter.py
        # but the forelimbs have zero output
        spike_network.add_neuron(motor_neuron_spk, name='dummy_neuron', color='green')
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)
        spike_network.add_output('dummy_neuron',spiking=True)



    render(spike_network, view=False, save=True, filename='python/fig_networks/jack_spk', img_format='png')

    return spike_network

def build_net(neuron_params, dt, fore_limbs, hop_step, lateral_step):

    # Create the space for the entire network to live
    whole_net = Network('all_legs')

    # Create the model of a limb network
    limb_net = build_limbs(neuron_params)

    whole_net.add_network(limb_net, suffix='_hi_R')
    whole_net.add_input('RG_HC_ext_hi_R')
    whole_net.add_network(limb_net, suffix='_hi_L')
    whole_net.add_input('RG_HC_flx_hi_L')

    # add forelimb hindlimb networks
    whole_net.add_network(limb_net, suffix='_fo_R')
    whole_net.add_input('RG_HC_ext_fo_R')
    whole_net.add_network(limb_net, suffix='_fo_L')
    whole_net.add_input('RG_HC_flx_fo_L')

    RG_adjust = 1

    # Based on Rybak
    base_neuron = NonSpikingNeuron(color='yellow', membrane_capacitance=5.0, membrane_conductance=1, resting_potential=-60)

    exc_2_5     = NonSpikingSynapse(max_conductance=1.00*0.15*RG_adjust, reversal_potential=0, e_hi=-40, e_lo=-60) # directly proportional to the period
    exc_1_0     = NonSpikingSynapse(max_conductance=0.25*0.15*RG_adjust, reversal_potential=0, e_hi=-40, e_lo=-60) # no impact, other synapse in link is too weak
    exc_0_3     = NonSpikingSynapse(max_conductance=0.0638*0.15*RG_adjust, reversal_potential=0, e_hi=-40, e_lo=-60) # inversely proportional to the period. small change has big impact
    inh_6_0     = NonSpikingSynapse(max_conductance=2.0*0.075*RG_adjust, reversal_potential=-100, e_hi=-40, e_lo=-60) # inversely proportional to the period
    exc_0_1_flx = NonSpikingSynapse(max_conductance=0.0204*0.15*RG_adjust, reversal_potential=0, e_hi=-40, e_lo=-60) # increased period. larger impact on ext period. later coupling effect. 
    exc_0_1_ext = NonSpikingSynapse(max_conductance=0.0204*0.15*RG_adjust, reversal_potential=0, e_hi=-40, e_lo=-60) # Proportional to the period
    exc_1_5     = NonSpikingSynapse(max_conductance=0.4286*0.75*RG_adjust, reversal_potential=0, e_hi=-40, e_lo=-60)  # inversely proportional to the period

    """
    LEFT AND RIGHT LIMB RHYTHM GENERATOR NETWORK CONNECTIONS

        Fore and hind limb RG interneuron synapses:

            exc_2_5:           Pre-V0d synapse      # Proportional to the period
            exc_0_3:           Pre-V3e synapse      # Inversely proportional to the period. Small change has big impact
            inh_6_0:           Post-V0d synapse     # Inversely proportional to the period
            exc_0_1_ext:       Post-V3e synapse     # Proportional to the period
    """
    if hop_step:
        #############################
        ############# HIND LIMBS ####################
        #############################################
        whole_net.add_neuron(base_neuron, 'V0d_hi_L')
        whole_net.add_neuron(base_neuron, 'V3f_hi_L')
        whole_net.add_neuron(base_neuron, 'V3e_hi_L')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_hi_L')
        whole_net.add_connection(inh_6_0, 'V0d_hi_L', 'RG_HC_ext_hi_R')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_L', 'V3f_hi_L')
        whole_net.add_connection(exc_0_1_flx, 'V3f_hi_L', 'RG_HC_ext_hi_R')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_hi_L')
        whole_net.add_connection(exc_0_1_ext, 'V3e_hi_L', 'RG_HC_flx_hi_R')

        whole_net.add_neuron(base_neuron, 'V0d_hi_R')
        whole_net.add_neuron(base_neuron, 'V3f_hi_R')
        whole_net.add_neuron(base_neuron, 'V3e_hi_R')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_hi_R')
        whole_net.add_connection(inh_6_0, 'V0d_hi_R', 'RG_HC_ext_hi_L')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_R', 'V3f_hi_R')
        whole_net.add_connection(exc_0_1_flx, 'V3f_hi_R', 'RG_HC_ext_hi_L')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_hi_R')
        whole_net.add_connection(exc_0_1_ext, 'V3e_hi_R', 'RG_HC_flx_hi_L')


        #############################################
        ############# FORE LIMBS ####################
        #############################################
        whole_net.add_neuron(base_neuron, 'V0d_fo_L')
        whole_net.add_neuron(base_neuron, 'V3f_fo_L')
        whole_net.add_neuron(base_neuron, 'V3e_fo_L')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_fo_L')
        whole_net.add_connection(inh_6_0, 'V0d_fo_L', 'RG_HC_ext_fo_R')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_fo_L', 'V3f_fo_L')
        whole_net.add_connection(exc_0_1_flx, 'V3f_fo_L', 'RG_HC_ext_fo_R')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_fo_L')
        whole_net.add_connection(exc_0_1_ext, 'V3e_fo_L', 'RG_HC_flx_fo_R')

        whole_net.add_neuron(base_neuron, 'V0d_fo_R')
        whole_net.add_neuron(base_neuron, 'V3f_fo_R')
        whole_net.add_neuron(base_neuron, 'V3e_fo_R')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_fo_R')
        whole_net.add_connection(inh_6_0, 'V0d_fo_R', 'RG_HC_ext_fo_L')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_fo_R', 'V3f_fo_R')
        whole_net.add_connection(exc_0_1_flx, 'V3f_fo_R', 'RG_HC_ext_fo_L')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_fo_R')
        whole_net.add_connection(exc_0_1_ext, 'V3e_fo_R', 'RG_HC_flx_fo_L')

        if fore_limbs: # Connect the fore and hind limbs if forelimbs are being used.

            #############################################
            ############# LEFT LIMBS ####################
            #############################################
            whole_net.add_neuron(base_neuron, 'V0d_L_hi2fo')
            whole_net.add_neuron(base_neuron, 'V3f_L_hi2fo')
            whole_net.add_neuron(base_neuron, 'V3e_L_hi2fo')

            whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_L_hi2fo')
            whole_net.add_connection(inh_6_0, 'V0d_L_hi2fo', 'RG_HC_flx_fo_R')

            whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_L', 'V3f_L_hi2fo')
            whole_net.add_connection(exc_0_1_flx, 'V3f_L_hi2fo', 'RG_HC_flx_fo_R')

            whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_L_hi2fo')
            whole_net.add_connection(exc_0_1_ext, 'V3e_L_hi2fo', 'RG_HC_ext_fo_R')
            
            whole_net.add_neuron(base_neuron, 'V0d_L_fo2hi') 
            whole_net.add_neuron(base_neuron, 'V3f_L_fo2hi')
            whole_net.add_neuron(base_neuron, 'V3e_L_fo2hi')
            
            whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_L_fo2hi')
            whole_net.add_connection(inh_6_0, 'V0d_L_fo2hi', 'RG_HC_flx_hi_R')

            whole_net.add_connection(exc_0_3, 'RG_HC_flx_fo_L', 'V3f_L_fo2hi')
            whole_net.add_connection(exc_0_1_flx, 'V3f_L_fo2hi', 'RG_HC_flx_hi_R')

            whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_L_fo2hi')
            whole_net.add_connection(exc_0_1_ext, 'V3e_L_fo2hi', 'RG_HC_ext_hi_R')


            #############################################
            ############# RIGHT LIMBS ###################
            #############################################
            whole_net.add_neuron(base_neuron, 'V0d_R_hi2fo')
            whole_net.add_neuron(base_neuron, 'V3f_R_hi2fo')
            whole_net.add_neuron(base_neuron, 'V3e_R_hi2fo')

            whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_R_hi2fo')
            whole_net.add_connection(inh_6_0, 'V0d_R_hi2fo', 'RG_HC_flx_fo_L')

            whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_R', 'V3e_R_hi2fo')
            whole_net.add_connection(exc_0_1_flx, 'V3f_R_hi2fo', 'RG_HC_flx_fo_L')

            whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_R_hi2fo')
            whole_net.add_connection(exc_0_1_ext, 'V3e_R_hi2fo', 'RG_HC_ext_fo_L')

            whole_net.add_neuron(base_neuron, 'V0d_R_fo2hi')
            whole_net.add_neuron(base_neuron, 'V3f_R_fo2hi')
            whole_net.add_neuron(base_neuron, 'V3e_R_fo2hi')

            whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_R_fo2hi')
            whole_net.add_connection(inh_6_0, 'V0d_R_fo2hi', 'RG_HC_flx_hi_L')

            whole_net.add_connection(exc_0_3, 'RG_HC_flx_fo_R', 'V3f_R_fo2hi')
            whole_net.add_connection(exc_0_1_flx, 'V3f_R_fo2hi', 'RG_HC_flx_hi_L')

            whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_R_fo2hi')
            whole_net.add_connection(exc_0_1_ext, 'V3e_R_fo2hi', 'RG_HC_ext_hi_L')

    if not hop_step:
        #############################################
        ############# HIND LIMBS ####################
        #############################################
        whole_net.add_neuron(base_neuron, 'V0d_hi_L')
        whole_net.add_neuron(base_neuron, 'V3f_hi_L')
        whole_net.add_neuron(base_neuron, 'V3e_hi_L')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_hi_L')
        whole_net.add_connection(inh_6_0, 'V0d_hi_L', 'RG_HC_flx_hi_R')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_L', 'V3f_hi_L')
        whole_net.add_connection(exc_0_1_flx, 'V3f_hi_L', 'RG_HC_flx_hi_R')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_hi_L')
        whole_net.add_connection(exc_0_1_ext, 'V3e_hi_L', 'RG_HC_ext_hi_R')

        whole_net.add_neuron(base_neuron, 'V0d_hi_R')
        whole_net.add_neuron(base_neuron, 'V3f_hi_R')
        whole_net.add_neuron(base_neuron, 'V3e_hi_R')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_hi_R')
        whole_net.add_connection(inh_6_0, 'V0d_hi_R', 'RG_HC_flx_hi_L')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_R', 'V3f_hi_R')
        whole_net.add_connection(exc_0_1_flx, 'V3f_hi_R', 'RG_HC_flx_hi_L')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_hi_R')
        whole_net.add_connection(exc_0_1_ext, 'V3e_hi_R', 'RG_HC_ext_hi_L')


        #############################################
        ############# FORE LIMBS ####################
        #############################################
        whole_net.add_neuron(base_neuron, 'V0d_fo_L')
        whole_net.add_neuron(base_neuron, 'V3f_fo_L')
        whole_net.add_neuron(base_neuron, 'V3e_fo_L')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_fo_L')
        whole_net.add_connection(inh_6_0, 'V0d_fo_L', 'RG_HC_flx_fo_R')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_fo_L', 'V3f_fo_L')
        whole_net.add_connection(exc_0_1_flx, 'V3f_fo_L', 'RG_HC_flx_fo_R')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_fo_L')
        whole_net.add_connection(exc_0_1_ext, 'V3e_fo_L', 'RG_HC_ext_fo_R')

        whole_net.add_neuron(base_neuron, 'V0d_fo_R')
        whole_net.add_neuron(base_neuron, 'V3f_fo_R')
        whole_net.add_neuron(base_neuron, 'V3e_fo_R')

        whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_fo_R')
        whole_net.add_connection(inh_6_0, 'V0d_fo_R', 'RG_HC_flx_fo_L')

        whole_net.add_connection(exc_1_0, 'RG_HC_flx_fo_R', 'V3f_fo_R')
        whole_net.add_connection(exc_0_1_flx, 'V3f_fo_R', 'RG_HC_flx_fo_L')

        whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_fo_R')
        whole_net.add_connection(exc_0_1_ext, 'V3e_fo_R', 'RG_HC_ext_fo_L')

        if fore_limbs: # Connect the fore and hind limbs if forelimbs are being used.

            if lateral_step:

                #############################################
                ############# LEFT LIMBS ####################
                #############################################
                whole_net.add_neuron(base_neuron, 'V0d_L_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3f_L_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3e_L_hi2fo')

                whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_L_hi2fo')
                whole_net.add_connection(inh_6_0, 'V0d_L_hi2fo', 'RG_HC_flx_fo_R')

                whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_L', 'V3f_L_hi2fo')
                whole_net.add_connection(exc_0_1_flx, 'V3f_L_hi2fo', 'RG_HC_flx_fo_R')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_L_hi2fo')
                whole_net.add_connection(exc_0_1_ext, 'V3e_L_hi2fo', 'RG_HC_ext_fo_R')
                
                whole_net.add_neuron(base_neuron, 'V0d_L_fo2hi') 
                whole_net.add_neuron(base_neuron, 'V3f_L_fo2hi')
                whole_net.add_neuron(base_neuron, 'V3e_L_fo2hi')
                
                whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_L_fo2hi')
                whole_net.add_connection(inh_6_0, 'V0d_L_fo2hi', 'RG_HC_flx_hi_R')

                whole_net.add_connection(exc_0_3, 'RG_HC_flx_fo_L', 'V3f_L_fo2hi')
                whole_net.add_connection(exc_0_1_flx, 'V3f_L_fo2hi', 'RG_HC_flx_hi_R')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_L_fo2hi')
                whole_net.add_connection(exc_0_1_ext, 'V3e_L_fo2hi', 'RG_HC_ext_hi_R')


                #############################################
                ############# RIGHT LIMBS ###################
                #############################################
                whole_net.add_neuron(base_neuron, 'V0d_R_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3f_R_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3e_R_hi2fo')

                whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_R_hi2fo')
                whole_net.add_connection(inh_6_0, 'V0d_R_hi2fo', 'RG_HC_flx_fo_L')

                whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_R', 'V3e_R_hi2fo')
                whole_net.add_connection(exc_0_1_flx, 'V3f_R_hi2fo', 'RG_HC_flx_fo_L')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_R_hi2fo')
                whole_net.add_connection(exc_0_1_ext, 'V3e_R_hi2fo', 'RG_HC_ext_fo_L')

                whole_net.add_neuron(base_neuron, 'V0d_R_fo2hi')
                whole_net.add_neuron(base_neuron, 'V3f_R_fo2hi')
                whole_net.add_neuron(base_neuron, 'V3e_R_fo2hi')

                whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_R_fo2hi')
                whole_net.add_connection(inh_6_0, 'V0d_R_fo2hi', 'RG_HC_flx_hi_L')

                whole_net.add_connection(exc_0_3, 'RG_HC_flx_fo_R', 'V3f_R_fo2hi')
                whole_net.add_connection(exc_0_1_flx, 'V3f_R_fo2hi', 'RG_HC_flx_hi_L')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_R_fo2hi')
                whole_net.add_connection(exc_0_1_ext, 'V3e_R_fo2hi', 'RG_HC_ext_hi_L')

            else:

                #############################################
                ############# LEFT LIMBS ####################
                #############################################
                whole_net.add_neuron(base_neuron, 'V0d_L_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3f_L_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3e_L_hi2fo')

                whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_L_hi2fo')
                whole_net.add_connection(inh_6_0, 'V0d_L_hi2fo', 'RG_HC_flx_fo_L')

                whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_L', 'V3f_L_hi2fo')
                whole_net.add_connection(exc_0_1_flx, 'V3f_L_hi2fo', 'RG_HC_flx_fo_L')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_L_hi2fo')
                whole_net.add_connection(exc_0_1_ext, 'V3e_L_hi2fo', 'RG_HC_ext_fo_L')
                
                whole_net.add_neuron(base_neuron, 'V0d_L_fo2hi') 
                whole_net.add_neuron(base_neuron, 'V3f_L_fo2hi')
                whole_net.add_neuron(base_neuron, 'V3e_L_fo2hi')
                
                whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_L_fo2hi')
                whole_net.add_connection(inh_6_0, 'V0d_L_fo2hi', 'RG_HC_flx_hi_L')

                whole_net.add_connection(exc_0_3, 'RG_HC_flx_fo_L', 'V3f_L_fo2hi')
                whole_net.add_connection(exc_0_1_flx, 'V3f_L_fo2hi', 'RG_HC_flx_hi_L')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_L_fo2hi')
                whole_net.add_connection(exc_0_1_ext, 'V3e_L_fo2hi', 'RG_HC_ext_hi_L')


                #############################################
                ############# RIGHT LIMBS ###################
                #############################################
                whole_net.add_neuron(base_neuron, 'V0d_R_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3f_R_hi2fo')
                whole_net.add_neuron(base_neuron, 'V3e_R_hi2fo')

                whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_R_hi2fo')
                whole_net.add_connection(inh_6_0, 'V0d_R_hi2fo', 'RG_HC_flx_fo_R')

                whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_R', 'V3e_R_hi2fo')
                whole_net.add_connection(exc_0_1_flx, 'V3f_R_hi2fo', 'RG_HC_flx_fo_R')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_R_hi2fo')
                whole_net.add_connection(exc_0_1_ext, 'V3e_R_hi2fo', 'RG_HC_ext_fo_R')

                whole_net.add_neuron(base_neuron, 'V0d_R_fo2hi')
                whole_net.add_neuron(base_neuron, 'V3f_R_fo2hi')
                whole_net.add_neuron(base_neuron, 'V3e_R_fo2hi')

                whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_R_fo2hi')
                whole_net.add_connection(inh_6_0, 'V0d_R_fo2hi', 'RG_HC_flx_hi_R')

                whole_net.add_connection(exc_0_3, 'RG_HC_flx_fo_R', 'V3f_R_fo2hi')
                whole_net.add_connection(exc_0_1_flx, 'V3f_R_fo2hi', 'RG_HC_flx_hi_R')

                whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_R_fo2hi')
                whole_net.add_connection(exc_0_1_ext, 'V3e_R_fo2hi', 'RG_HC_ext_hi_R')
        

    '''
    Add spiking network.

    Connect non-spiking neurons to spiking outputs via a synapse, instead of a transfer function
    '''

    spk_net = spike_net(dt = 0.01, fore_limbs=fore_limbs)
    whole_net.add_network(spk_net, suffix="_spk")

    non2spk = NonSpikingSynapse(max_conductance=.16, reversal_potential=20, e_hi=-60, e_lo=-100) # directly proportional to the period
    
    whole_net.add_connection(non2spk,'MN_ext_Hip_hi_R','R_hip_ext_muscle_spk')
    whole_net.add_connection(non2spk,'MN_flx_Hip_hi_R','R_hip_flx_muscle_spk')
    whole_net.add_connection(non2spk,'MN_ext_Knee_hi_R','R_knee_ext_muscle_spk')
    whole_net.add_connection(non2spk,'MN_flx_Knee_hi_R','R_knee_flx_muscle_spk')
    whole_net.add_connection(non2spk,'MN_ext_Ankle_hi_R','R_ankle_ext_muscle_spk')
    whole_net.add_connection(non2spk,'MN_flx_Ankle_hi_R','R_ankle_flx_muscle_spk')
    whole_net.add_connection(non2spk,'MN_ext_Hip_hi_L','L_hip_ext_muscle_spk')
    whole_net.add_connection(non2spk,'MN_flx_Hip_hi_L','L_hip_flx_muscle_spk')
    whole_net.add_connection(non2spk,'MN_ext_Knee_hi_L','L_knee_ext_muscle_spk')
    whole_net.add_connection(non2spk,'MN_flx_Knee_hi_L','L_knee_flx_muscle_spk')
    whole_net.add_connection(non2spk,'MN_ext_Ankle_hi_L','L_ankle_ext_muscle_spk')
    whole_net.add_connection(non2spk,'MN_flx_Ankle_hi_L','L_ankle_flx_muscle_spk')
    whole_net.add_connection(non2spk,'MN_ext_Hip_fo_R','R_scapula_ext_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_flx_Hip_fo_R','R_scapula_flx_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_ext_Knee_fo_R','R_shoulder_ext_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_flx_Knee_fo_R','R_shoulder_flx_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_ext_Ankle_fo_R','R_wrist_ext_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_flx_Ankle_fo_R','R_wrist_flx_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_ext_Hip_fo_L','L_scapula_ext_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_flx_Hip_fo_L','L_scapula_flx_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_ext_Knee_fo_L','L_shoulder_ext_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_flx_Knee_fo_L','L_shoulder_flx_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_ext_Ankle_fo_L','L_wrist_ext_muscle_forelimb_spk')
    whole_net.add_connection(non2spk,'MN_flx_Ankle_fo_L','L_wrist_flx_muscle_forelimb_spk')
    
    render(whole_net, view=False, save=True, filename='Python/fig_networks/leo_sns.png', img_format='png')

    mn_labels = whole_net.outputs # TODO: Determine method by which to ehindlimbantly search for output names.

    return whole_net.compile(backend='numpy', dt=dt)



def main():
    sns_model = build_net(neuron_params, dt, fore_limbs, hop_step, lateral_step)
    # print(sns_model.num_inputs)
    # print(sns_model.num_outputs)

if __name__ == '__main__':
    main()
