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
        Ia_flx_Ia_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)
        Ia_ext_Ia_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)
        Ia_flx_mn_ext = NonSpikingSynapse(max_conductance=2.0, reversal_potential=-100,e_hi=-40, e_lo=-60)
        Ia_ext_mn_flx = NonSpikingSynapse(max_conductance=2.0, reversal_potential=-100,e_hi=-40, e_lo=-60)
        mn_flx_rc_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40,e_hi=-10, e_lo=-100)
        mn_ext_rc_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40,e_hi=-10, e_lo=-100)
        rc_ext_Ia_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)
        rc_flx_Ia_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)
        rc_ext_mn_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-100,e_hi=-40, e_lo=-60)
        rc_flx_mn_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-100,e_hi=-40, e_lo=-60)
        rc_flx_rc_ext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)
        rc_ext_rc_flx = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-70,e_hi=-40, e_lo=-60)

        self.add_connection(Ia_flx_Ia_ext, 'Ia_flx', 'Ia_ext')
        self.add_connection(Ia_ext_Ia_flx, 'Ia_ext', 'Ia_flx')
        self.add_connection(Ia_flx_mn_ext, 'Ia_flx', 'MN_ext')
        self.add_connection(Ia_ext_mn_flx, 'Ia_ext', 'MN_flx')
        self.add_connection(mn_flx_rc_flx, 'MN_flx', 'RC_flx')
        self.add_connection(mn_ext_rc_ext, 'MN_ext', 'RC_ext')
        self.add_connection(rc_ext_Ia_ext, 'RC_ext', 'Ia_ext')
        self.add_connection(rc_flx_Ia_flx, 'RC_flx', 'Ia_flx')
        self.add_connection(rc_ext_mn_ext, 'RC_ext', 'MN_ext')
        self.add_connection(rc_flx_mn_flx, 'RC_flx', 'MN_flx')
        self.add_connection(rc_flx_rc_ext, 'RC_flx', 'RC_ext')
        self.add_connection(rc_ext_rc_flx, 'RC_ext', 'RC_flx')

        Ib2MN_flx = NonSpikingSynapse(max_conductance=1.0, reversal_potential=-10, e_hi=-40, e_lo=-60)
        Ib2MN_ext = NonSpikingSynapse(max_conductance=0.59, reversal_potential=-10, e_hi=-40, e_lo=-60)
        IaIn2Iaflx = NonSpikingSynapse(max_conductance=0.695, reversal_potential=-40, e_hi=-40, e_lo=-60)
        IaIn2Iaext = NonSpikingSynapse(max_conductance=0.5, reversal_potential=-40, e_hi=-40, e_lo=-60)
        IaIN2MNflx = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)
        IaIN2MNext = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)

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

def build_hindlimbs(cpg_gsyn=1.49167, dt = 0.01, feed_forward=True):

    net = Network('Kaiyu_2layehi_Rndlimb')

    if feed_forward == True:
        MN_mag = 2
    else:
        MN_mag = 1

    Cm = 5
    Gm = 1
    Ena = 50
    Er = -60
    Sm = 0.2
    Sh = -0.6
    delEna = Ena
    Km = 1
    Kh = 0.5
    Em = -40
    Eh = -60
    delEm = Em
    delEh = Eh
    tauHmax = 350
    Gna = 1.5
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
    IaIN2MNflx = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)
    IaIN2MNext = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)
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

    PF2HipMN_ext = NonSpikingSynapse(max_conductance=2.565*0.15*MN_mag*4, reversal_potential=-10, e_hi=-50, e_lo=-60)
    PF2HipMN_flx = NonSpikingSynapse(max_conductance=3.632*0.07*MN_mag*4, reversal_potential=-10, e_hi=-50, e_lo=-60)

    PF2KneeMN_ext = NonSpikingSynapse(max_conductance=2.1*MN_mag, reversal_potential=-40, e_hi=-50, e_lo=-60)
    PF2KneeMN_flx = NonSpikingSynapse(max_conductance=1.6*MN_mag, reversal_potential=-40, e_hi=-50, e_lo=-60)

    PF2AnkleMN_ext = NonSpikingSynapse(max_conductance=2.7*MN_mag, reversal_potential=-10, e_hi=-50, e_lo=-60)
    PF2AnkleMN_flx = NonSpikingSynapse(max_conductance=4.4*MN_mag, reversal_potential=-40, e_hi=-50, e_lo=-60)
    
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

    net.add_connection(HipII_flx2RG_IN_ext, 'II_IN_flx_Hip','RG_IN_ext')
    net.add_connection(HipII_ext2RG_IN_flx, 'II_IN_ext_Hip','RG_IN_flx')
    net.add_connection(HipII_flx2Hip_PF_IN_ext, 'II_IN_flx_Hip', 'PF_IN_ext_Hip')
    net.add_connection(HipII_ext2Hip_PF_IN_flx, 'II_IN_ext_Hip', 'PF_IN_flx_Hip')
    net.add_connection(HipII_flx2KA_PF_IN_ext, 'II_IN_flx_Hip', 'KA_PF_IN_ext')
    net.add_connection(HipII_ext2KA_PF_IN_flx, 'II_IN_ext_Hip', 'KA_PF_IN_flx')
    net.add_connection(AnkleIb_ext2KA_PF_IN_ext, 'IbIN_ext_Ankle', 'KA_PF_IN_ext')

    net.add_output('RG_HC_ext')
    net.add_output('RG_HC_flx')

    net.add_output('PF_HC_ext_Hip')
    net.add_output('PF_HC_flx_Hip')
    net.add_output('KA_PF_HC_ext')
    net.add_output('KA_PF_HC_flx')

    return net

def build_forelimbs(cpg_gsyn=1.49167, dt=0.01, feed_forward=True):

    net = Network('Kaiyu_2layehi_Rndlimb')

    if feed_forward == True:
        MN_mag = 2
    else:
        MN_mag = 1

    Cm = 5
    Gm = 1
    Ena = 50
    Er = -60
    Sm = 0.2
    Sh = -0.6
    delEna = Ena
    Km = 1
    Kh = 0.5
    Em = -40
    Eh = -60
    delEm = Em
    delEh = Eh
    tauHmax = 350
    Gna = 1.5
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
    IaIN2MNflx = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)
    IaIN2MNext = NonSpikingSynapse(max_conductance=0.0, reversal_potential=0, e_hi=-40, e_lo=-60)
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

    PF2HipMN_ext = NonSpikingSynapse(max_conductance=2.565*0.3*MN_mag, reversal_potential=-10, e_hi=-50, e_lo=-60)
    PF2HipMN_flx = NonSpikingSynapse(max_conductance=3.632*0.3*MN_mag, reversal_potential=-10, e_hi=-50, e_lo=-60)

    PF2KneeMN_ext = NonSpikingSynapse(max_conductance=2.1*MN_mag, reversal_potential=-40, e_hi=-50, e_lo=-60)
    PF2KneeMN_flx = NonSpikingSynapse(max_conductance=1.6*MN_mag, reversal_potential=-40, e_hi=-50, e_lo=-60)

    PF2AnkleMN_ext = NonSpikingSynapse(max_conductance=2.7*MN_mag, reversal_potential=-10, e_hi=-50, e_lo=-60)
    PF2AnkleMN_flx = NonSpikingSynapse(max_conductance=4.4*MN_mag, reversal_potential=-40, e_hi=-50, e_lo=-60)
    
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

    net.add_connection(HipII_flx2RG_IN_ext, 'II_IN_flx_Hip','RG_IN_ext')
    net.add_connection(HipII_ext2RG_IN_flx, 'II_IN_ext_Hip','RG_IN_flx')
    net.add_connection(HipII_flx2Hip_PF_IN_ext, 'II_IN_flx_Hip', 'PF_IN_ext_Hip')
    net.add_connection(HipII_ext2Hip_PF_IN_flx, 'II_IN_ext_Hip', 'PF_IN_flx_Hip')
    net.add_connection(HipII_flx2KA_PF_IN_ext, 'II_IN_flx_Hip', 'KA_PF_IN_ext')
    net.add_connection(HipII_ext2KA_PF_IN_flx, 'II_IN_ext_Hip', 'KA_PF_IN_flx')
    net.add_connection(AnkleIb_ext2KA_PF_IN_ext, 'IbIN_ext_Ankle', 'KA_PF_IN_ext')

    net.add_output('RG_HC_ext')
    net.add_output('RG_HC_flx')

    net.add_output('PF_HC_ext_Hip')
    net.add_output('PF_HC_flx_Hip')
    net.add_output('KA_PF_HC_ext')
    net.add_output('KA_PF_HC_flx')

    return net


def build_net(cpg_gsyn=1.49167, dt = 0.01, return_net = False, feed_forward=True): 

    if feed_forward == True:
        RG_mag = 2
    else:
        RG_mag = 1

    Cm = 5
    Gm = 1
    Ena = 50
    Er = -60
    Sm = 0.2
    Sh = -0.6
    delEna = Ena
    Km = 1
    Kh = 0.5
    Em = -40
    Eh = -60
    delEm = Em
    delEh = Eh
    tauHmax = 350
    Gna = 1.5
    # reformat for sns-toolbox
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

    whole_net = Network('hindlimbs')

    hindlimb_net = build_hindlimbs(cpg_gsyn=cpg_gsyn,feed_forward=feed_forward)
    forelimb_net = build_forelimbs(cpg_gsyn=cpg_gsyn,feed_forward=feed_forward)
    hindlimb_false = build_hindlimbs(cpg_gsyn = 0)

    whole_net.add_network(hindlimb_net, suffix='_hi_R')
    whole_net.add_input('RG_HC_ext_hi_R')
    whole_net.add_network(hindlimb_net, suffix='_hi_L')
    whole_net.add_input('RG_HC_flx_hi_L')

    # add forelimb hindlimb networks
    whole_net.add_network(forelimb_net, suffix='_fo_R')
    whole_net.add_input('RG_HC_ext_fo_R')
    whole_net.add_network(forelimb_net, suffix='_fo_L')
    whole_net.add_input('RG_HC_flx_fo_L')


    # Based on Rybak
    base_neuron = NonSpikingNeuron(color='yellow', membrane_capacitance=5.0, membrane_conductance=1, resting_potential=-60)

    exc_2_5     = NonSpikingSynapse(max_conductance=1.00*0.15*RG_mag, reversal_potential=0, e_hi=-40, e_lo=-60) # directly proportional to the period
    exc_1_0     = NonSpikingSynapse(max_conductance=0.25*0.15*RG_mag, reversal_potential=0, e_hi=-40, e_lo=-60) # no impact, other synapse in link is too weak
    exc_0_3     = NonSpikingSynapse(max_conductance=0.0638*0.15*RG_mag, reversal_potential=0, e_hi=-40, e_lo=-60) # inversely proportional to the period. small change has big impact
    inh_6_0     = NonSpikingSynapse(max_conductance=2.0*0.075*RG_mag, reversal_potential=-100, e_hi=-40, e_lo=-60) # inversely proportional to the period
    exc_0_1_flx = NonSpikingSynapse(max_conductance=0.0204*0.15*RG_mag, reversal_potential=0, e_hi=-40, e_lo=-60) # increased period. larger impact on ext period. later coupling effect. 
    exc_0_1_ext = NonSpikingSynapse(max_conductance=0.0204*0.15*RG_mag, reversal_potential=0, e_hi=-40, e_lo=-60) # Proportional to the period
    exc_1_5     = NonSpikingSynapse(max_conductance=0.4286*0.75*RG_mag, reversal_potential=0, e_hi=-40, e_lo=-60)  # inversely proportional to the period

    # TODO: We are getting close! Edits to the conductances values in the forelimb 
    # construction yeld better MN activity compared to the PF networks (no changes
    # from the RG to PF conductances). However, now the RGs seems to want to move 
    # in unison, regardless of whether they are mutually inhibited or not. Thus we
    # need to find out the reason for this, and fast!!! 

    # whole_net.add_neuron(base_neuron, 'inh_L')
    # whole_net.add_neuron(base_neuron, 'V2a_L')
    # whole_net.add_neuron(base_neuron, 'V0v_L')
    whole_net.add_neuron(base_neuron, 'V0d_hi_L')
    whole_net.add_neuron(base_neuron, 'V3f_hi_L')
    whole_net.add_neuron(base_neuron, 'V3e_hi_L')

    # whole_net.add_neuron(base_neuron, 'inh_R')
    # whole_net.add_neuron(base_neuron, 'V2a_R')
    # whole_net.add_neuron(base_neuron, 'V0v_R')
    whole_net.add_neuron(base_neuron, 'V0d_hi_R')
    whole_net.add_neuron(base_neuron, 'V3f_hi_R')
    whole_net.add_neuron(base_neuron, 'V3e_hi_R')

    whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_hi_L')
    whole_net.add_connection(inh_6_0, 'V0d_hi_L', 'RG_HC_flx_hi_R')

    whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_L', 'V3f_hi_L')
    whole_net.add_connection(exc_0_1_flx, 'V3f_hi_L', 'RG_HC_flx_hi_R')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_hi_L')
    whole_net.add_connection(exc_0_1_ext, 'V3e_hi_L', 'RG_HC_ext_hi_R')
    # whole_net.add_connection(exc_1_5, 'V3e_hi_L', 'RG_IN_ext_hi_R')

    whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_hi_R')
    whole_net.add_connection(inh_6_0, 'V0d_hi_R', 'RG_HC_flx_hi_L')

    whole_net.add_connection(exc_1_0, 'RG_HC_flx_hi_R', 'V3f_hi_R')
    whole_net.add_connection(exc_0_1_flx, 'V3f_hi_R', 'RG_HC_flx_hi_L')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_hi_R')
    whole_net.add_connection(exc_0_1_ext, 'V3e_hi_R', 'RG_HC_ext_hi_L')
    # whole_net.add_connection(exc_1_5, 'V3e_hi_R', 'RG_IN_ext_hi_L')


    # create forelimb neurons in the same method as for the hind hindlimbs
    whole_net.add_neuron(base_neuron, 'V0d_fo_L')
    whole_net.add_neuron(base_neuron, 'V3f_fo_L')
    whole_net.add_neuron(base_neuron, 'V3e_fo_L')

    whole_net.add_neuron(base_neuron, 'V0d_fo_R')
    whole_net.add_neuron(base_neuron, 'V3f_fo_R')
    whole_net.add_neuron(base_neuron, 'V3e_fo_R')

    # connect forelimbs with the same interneurons as for the hind hindlimbs
    whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_fo_L')
    whole_net.add_connection(inh_6_0, 'V0d_fo_L', 'RG_HC_flx_fo_R')

    whole_net.add_connection(exc_1_0, 'RG_HC_flx_fo_L', 'V3f_fo_L')
    whole_net.add_connection(exc_0_1_flx, 'V3f_fo_L', 'RG_HC_flx_fo_R')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_fo_L')
    whole_net.add_connection(exc_0_1_ext, 'V3e_fo_L', 'RG_HC_ext_fo_R')

    whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_fo_R')
    whole_net.add_connection(inh_6_0, 'V0d_fo_R', 'RG_HC_flx_fo_L')

    whole_net.add_connection(exc_1_0, 'RG_HC_flx_fo_R', 'V3f_fo_R')
    whole_net.add_connection(exc_0_1_flx, 'V3f_fo_R', 'RG_HC_flx_fo_L')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_fo_R')
    whole_net.add_connection(exc_0_1_ext, 'V3e_fo_R', 'RG_HC_ext_fo_L')

    """
    The connection of RG networks above produces inverse correlations between extensor and flexor RG neurons.
    For example, when the RG_HC_flx_R neuron is excited, the RG_HC_flx_L neuron is inhibited through stimulation
    of the V0d_R internueron. 

    The V3e interneurons between the left and right extensor RGs have additional connections to the extensor HC
    interneuron which provides an inhibitory connection from the extensor HC to the flexor HC. To the best of 
    my knowledge this causes, for example, the left flexor RG to become excited when the right extensor RG is
    excited.

    Thus, the only additions needed to connect the fore and hind limb RGs will be, for now, inhibitory connections


    Rhythm Generator Connections

        Fore and Hind limb Interneurons:

            V0d_L_hi2fo:       Left hind to fore limb extensor RG interneuron                                    
            V0d_L_fo2hi:       Left fore to hind limb extensor RG interneuron
            V3e_L_hi2fo:       Left hind to fore limb extensor RG interneuron
            V3e_L_fo2hi:       Left fore to hind limb extensor RG interneuron
            V0d_R_hi2fo:       Right hind to fore limb extensor RG interneuron                                    
            V0d_R_fo2hi:       Right fore to hind limb extensor RG interneuron
            V3e_R_hi2fo:       Right hind to fore limb extensor RG interneuron
            V3e_R_fo2hi:       Right fore to hind limb extensor RG interneuron

        Fore and hind limb RG interneuron synapses:

            exc_2_5:           Pre-V0d synapse      # Proportional to the period
            exc_0_3:           Pre-V3e synapse      # Inversely proportional to the period. Small change has big impact
            inh_6_0:           Post-V0d synapse     # Inversely proportional to the period
            exc_0_1_ext:       Post-V3e synapse     # Proportional to the period
    """

    whole_net.add_neuron(base_neuron, 'V0d_L_hi2fo')
    whole_net.add_neuron(base_neuron, 'V0d_L_fo2hi')
    whole_net.add_neuron(base_neuron, 'V3e_L_hi2fo')
    whole_net.add_neuron(base_neuron, 'V3e_L_fo2hi')
    whole_net.add_neuron(base_neuron, 'V0d_R_hi2fo')
    whole_net.add_neuron(base_neuron, 'V0d_R_fo2hi')
    whole_net.add_neuron(base_neuron, 'V3e_R_hi2fo')
    whole_net.add_neuron(base_neuron, 'V3e_R_fo2hi')

    # Left RG internueron connections
    whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_L', 'V0d_L_hi2fo')
    whole_net.add_connection(inh_6_0, 'V0d_L_hi2fo', 'RG_HC_flx_fo_L')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_L', 'V3e_L_hi2fo')
    whole_net.add_connection(exc_0_1_ext, 'V3e_L_hi2fo', 'RG_HC_ext_fo_L')

    whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_L', 'V0d_L_fo2hi')
    whole_net.add_connection(inh_6_0, 'V0d_L_fo2hi', 'RG_HC_flx_hi_L')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_L', 'V3e_L_fo2hi')
    whole_net.add_connection(exc_0_1_ext, 'V3e_L_fo2hi', 'RG_HC_ext_hi_L')

    # Right RG internueron connections
    whole_net.add_connection(exc_2_5, 'RG_HC_flx_hi_R', 'V0d_R_hi2fo')
    whole_net.add_connection(inh_6_0, 'V0d_R_hi2fo', 'RG_HC_flx_fo_R')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_hi_R', 'V3e_R_hi2fo')
    whole_net.add_connection(exc_0_1_ext, 'V3e_R_hi2fo', 'RG_HC_ext_fo_R')

    whole_net.add_connection(exc_2_5, 'RG_HC_flx_fo_R', 'V0d_R_fo2hi')
    whole_net.add_connection(inh_6_0, 'V0d_R_fo2hi', 'RG_HC_flx_hi_R')

    whole_net.add_connection(exc_0_3, 'RG_HC_ext_fo_R', 'V3e_R_fo2hi')
    whole_net.add_connection(exc_0_1_ext, 'V3e_R_fo2hi', 'RG_HC_ext_hi_R')


    # render(whole_net, view=False, save=True, filename='jack_sns', img_format='png')

    # mn_labels = whole_net.outputs # TODO: Determine method by which to ehindlimbantly search for output names.

    if return_net:
        return whole_net.compile(backend='numpy', dt=dt), whole_net
    else:
        return whole_net.compile(backend='numpy', dt=dt)

def spike_net(dt = 0.01, return_net = False):
    spike_network = Network('python/fig_networks/Jack_Non2Spk')

    motor_neuron_non2spk = SpikingNeuron(name='MN_spk', color='yellow', threshold_initial_value = 1, threshold_time_constant = 50, membrane_capacitance = 50)

    spike_network.add_neuron(motor_neuron_non2spk, name='R_hip_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_hip_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_knee_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_knee_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_ankle_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_ankle_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_hip_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_hip_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_knee_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_knee_flx_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_ankle_ext_muscle', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_ankle_flx_muscle', color='blue')

    spike_network.add_input('R_hip_ext_muscle')
    spike_network.add_input('R_hip_flx_muscle')
    spike_network.add_input('R_knee_ext_muscle')
    spike_network.add_input('R_knee_flx_muscle')
    spike_network.add_input('R_ankle_ext_muscle')
    spike_network.add_input('R_ankle_flx_muscle')
    spike_network.add_input('L_hip_ext_muscle')
    spike_network.add_input('L_hip_flx_muscle')
    spike_network.add_input('L_knee_ext_muscle')
    spike_network.add_input('L_knee_flx_muscle')
    spike_network.add_input('L_ankle_ext_muscle')
    spike_network.add_input('L_ankle_flx_muscle')

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

    ### forelimb hindlimb spiking network
    spike_network.add_neuron(motor_neuron_non2spk, name='R_scapula_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_scapula_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_shoulder_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_shoulder_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_wrist_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='R_wrist_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_scapula_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_scapula_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_shoulder_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_shoulder_flx_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_wrist_ext_muscle_forelimb', color='blue')
    spike_network.add_neuron(motor_neuron_non2spk, name='L_wrist_flx_muscle_forelimb', color='blue')

    spike_network.add_input('R_scapula_ext_muscle_forelimb')
    spike_network.add_input('R_scapula_flx_muscle_forelimb')
    spike_network.add_input('R_shoulder_ext_muscle_forelimb')
    spike_network.add_input('R_shoulder_flx_muscle_forelimb')
    spike_network.add_input('R_wrist_ext_muscle_forelimb')
    spike_network.add_input('R_wrist_flx_muscle_forelimb')
    spike_network.add_input('L_scapula_ext_muscle_forelimb')
    spike_network.add_input('L_scapula_flx_muscle_forelimb')
    spike_network.add_input('L_shoulder_ext_muscle_forelimb')
    spike_network.add_input('L_shoulder_flx_muscle_forelimb')
    spike_network.add_input('L_wrist_ext_muscle_forelimb')
    spike_network.add_input('L_wrist_flx_muscle_forelimb')

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

    render(spike_network, view=False, save=True, filename='python/fig_networks/jack_non2spk', img_format='png')

    if return_net:
        return spike_network.compile(backend='numpy', dt=dt), spike_net
    else:
        return spike_network.compile(backend='numpy', dt=dt)


    # # based on Alex Puppy Robot
    # base_neuron = NonSpikingNeuron(color='yellow', membrane_capacitance=5.0, membrane_conductance=1, resting_potential=-60)

    # whole_net.add_neuron(base_neuron, 'L_Cort_IN_exc')
    # whole_net.add_neuron(base_neuron,'L_Cort_IN_inh')
    # whole_net.add_neuron(base_neuron,'R_Cort_IN_exc')
    # whole_net.add_neuron(base_neuron,'R_Cort_IN_inh')

    # unit_add = NonSpikingSynapse(max_conductance=0.08, reversal_potential=0,e_hi=-40, e_lo=-60)
    # whole_net.add_connection(unit_add, 'L_RG_IN_flx', 'L_Cort_IN_exc')
    # whole_net.add_connection(unit_add, 'R_RG_IN_flx', 'R_Cort_IN_exc')

    # unit_add = NonSpikingSynapse(max_conductance=0.3, reversal_potential=0,e_hi=-40, e_lo=-60)
    # whole_net.add_connection(unit_add, 'L_RG_IN_flx', 'L_Cort_IN_inh')    
    # whole_net.add_connection(unit_add, 'R_RG_IN_flx', 'R_Cort_IN_inh')

    # mutual_inhibit = NonSpikingSynapse(max_conductance=0.04, reversal_potential=-100,e_hi=-40, e_lo=-60)
    # whole_net.add_connection(mutual_inhibit, 'L_Cort_IN_inh', 'R_Cort_IN_inh')
    # whole_net.add_connection(mutual_inhibit, 'R_Cort_IN_inh', 'L_Cort_IN_inh')

    # unit_add = NonSpikingSynapse(max_conductance=0.014, reversal_potential=0,e_hi=-40, e_lo=-60)
    # whole_net.add_connection(unit_add, 'L_Cort_IN_exc', 'R_RG_IN_flx')
    # whole_net.add_connection(unit_add, 'R_Cort_IN_exc', 'L_RG_IN_flx')
    
    # unit_sub = NonSpikingSynapse(max_conductance=0.04, reversal_potential=-100,e_hi=-40, e_lo=-60)
    # whole_net.add_connection(unit_sub, 'L_Cort_IN_inh', 'R_RG_IN_flx')
    # whole_net.add_connection(unit_sub, 'R_Cort_IN_inh', 'L_RG_IN_flx')




    # if return_net:
    #     return whole_net.compile(backend='numoy', dt=dt), whole_net
    # else:
    #     return whole_net.compile(backend='numoy', dt=dt)
    

def main():
    sns_model = build_net()
    # print(sns_model.num_inputs)


if __name__ == '__main__':
    main()

    #Inputs: should be 32

    #Right
    # 0  Hip_IaIN_ext
    # 1  Hip_IaIN_flx
    # 2  Hip_IbIN_ext
    # 3  Hip_IbIN_flx
    # 4  Hip_II_IN_ext
    # 5  Hip_II_IN_flx
    # 6  Knee_IaIN_ext
    # 7  Knee_IaIN_flx
    # 8  Knee_IbIN_ext
    # 9  Knee_IbIN_flx
    # 10 Ankle_IaIN_ext
    # 11 Ankle_IaIN_flx
    # 12 Ankle_IbIN_ext
    # 13 Ankle_IbIN_flx
    # 14 Ankle_II_IN_flx
    # 15 RG_HC_ext

    #Left
    # 16 Hip_IaIN_ext
    # 17 Hip_IaIN_flx
    # 18 Hip_IbIN_ext
    # 19 Hip_IbIN_flx
    # 20 Hip_II_IN_ext
    # 21 Hip_II_IN_flx
    # 22 Knee_IaIN_ext
    # 23 Knee_IaIN_flx
    # 24 Knee_IbIN_ext
    # 25 Knee_IbIN_flx
    # 26 Ankle_IaIN_ext
    # 27 Ankle_IaIN_flx
    # 28 Ankle_IbIN_ext
    # 29 Ankle_IbIN_flx
    # 30 Ankle_II_IN_flx
    # 31 RG_HC_flx



    #outputs should be 24
    # right Side
    # 0 - hip mn ext
    # 1 - hip mn flx
    # 2 - knee mn ext
    # 3 - knee mn flx
    # 4 - ankle mn ext
    # 5 - ankle mn flx
    # 6 - RG ext
    # 7 - RG flx
    # 8 - hip PF ext
    # 9 - hip PF flx
    # 10- KA PF ext
    # 11- KA PF flx

    # left Side
    # 12 - hip mn ext
    # 13 - hip mn flx
    # 14 - knee mn ext
    # 15 - knee mn flx
    # 16 - ankle mn ext
    # 17 - ankle mn flx
    # 18 - RG ext
    # 19 - RG flx
    # 20 - hip PF ext
    # 21 - hip PF flx
    # 22 - KA PF ext
    # 23 - KA PF flx