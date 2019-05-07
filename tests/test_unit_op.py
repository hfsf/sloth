#test_mass_conservation.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.model import Model
from src.sloth.problem import Problem
from src.sloth.simulation import Simulation
from src.sloth.core.property_package import PropertyPackage
from src.sloth.analysis import Analysis

from src.sloth.unit_op_library import *

from src.sloth.core.equation_operators import *
from src.sloth.core.template_units import *
from src.sloth.core.domain import *


@pytest.fixture
def pp_water_toluene():
    """
    Create a property package
    """

    class pp_(PropertyPackage):

        def __init__(self, phases, phase_names):

            super().__init__(phases, phase_names)

    return pp_(phases=2, phase_names=['water', 'toluene'])

@pytest.fixture
def pp_water():
    """
    Create a property package
    """

    class pp_(PropertyPackage):

        def __init__(self, phases, phase_names):

            super().__init__(phases, phase_names)

    return pp_(phases=1, phase_names=['water'])

'''
def homogeneous_material_stream(pp_water, name):

    """
    Create a homogeneous material_stream model
    """
    class h_material_stream(MaterialStream):

        def __init__(self, name, description="Homogeneous material stream", property_package=pp_water):

            super().__init__(name, description, property_package)
'''

@pytest.fixture
def simple_heater():

    class heater_model(Heater):

        def __init__(self, name, description, property_package):

            super().__init__(name, description, property_package)

    return heater_model

@pytest.fixture
def simple_mixer():

    class mix_model(Mixer):

        def __init__(self, name, description, property_package):

            super().__init__(name, description, property_package)

    return mix_model

@pytest.fixture
def valve_class():

    class valve_class(Valve):

        def __init__(self, name, description, property_package):

            super().__init__(name, description, property_package)

    return valve_class

@pytest.fixture
def biphasic_mixer_class(pp_water_toluene):

    class mix_model(Mixer):

        def __init__(self, name, description, property_package):

            super().__init__(name, description, property_package)

            '''
            for phase_i in self.property_package.phase_names:

                exec("self.x_{}=createVariable('x_{}_out',dimless,'Molar fraction for {} phase in the output',is_exposed=True, type='output')".format(phase_i))
                exec("self.w_{}=createVariable('w_{}_out',dimless,'Mass fraction for {} phase in the output',is_exposed=True, type='output')".format(phase_i))
            '''

    #m_mod = mix_model("BFM0","Model for biphasic mixer", pp_water_toluene)

    #m_mod()

    return mix_model #m_mod

@pytest.fixture
def prob():
    """
    Create a generic problem
    """

    return Problem("prob", "generic problem")

@pytest.fixture
def sim():
    """
    Create a generic simulation
    """

    class simul(Simulation):

        def __init__(self, name, description):

            super().__init__(name, description)

    return simul("simul", "generic simulation")

def test_mixer_and_homogeneous_material_stream(simple_mixer, prob, sim, pp_water):

    """
    Test for simulation of the mixer problem using models for material streams
    """

    simple_mixer = simple_mixer("M0", "Simple mixer", pp_water)
    simple_mixer()

    #---------------------------------------------
    #Create a homogeneous material_stream model

    class homogeneous_material_stream(MaterialStream):

        def __init__(self, name, mdot, description="Homogeneous material stream", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.mdot.setValue(mdot)

            self.T.setValue(298.15)

            self.H.setValue(0.)

            self.P.setValue(101325.)
    #----------------------------------------------

    hms1 = homogeneous_material_stream("HMS1", 100.)
    hms1.P.setValue(120e3)
    hms1()
    hms2 = homogeneous_material_stream("HMS2", 200.)
    hms2()

    prob.addModels([simple_mixer, hms1, hms2])

    prob.createConnection("", simple_mixer, Min(hms1.T(), hms2.T()), simple_mixer.T_in())

    prob.createConnection("", simple_mixer, hms1.mdot()+hms2.mdot(), simple_mixer.mdot_in())

    prob.createConnection("", simple_mixer, hms1.ndot()+hms2.ndot(), simple_mixer.ndot_in())

    prob.createConnection("", simple_mixer, Min(hms1.P(), hms2.P()), simple_mixer.P_in())

    prob.createConnection("", simple_mixer, hms1.ndot()*hms1.H() + hms2.ndot()*hms1.H(), simple_mixer.ndot_in()*simple_mixer.H_in())

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print(results)

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )


def test_biphasic_mixer_biphasic_material_stream(biphasic_mixer_class, prob, sim, pp_water_toluene):

    """
    Test for simulation of the mixer problem using models for material streams
    """

    biphasic_mixer = biphasic_mixer_class("BFM0", "Model for biphasic mixer", pp_water_toluene)
    biphasic_mixer()

    #---------------------------------------------
    #Create biphasic material_stream model

    class biphasic_material_stream(MaterialStream):

        def __init__(self, name, ndot, z1, description="Biphasic material stream", property_package=pp_water_toluene):

            super().__init__(name, description, property_package)

            self.ndot.setValue(ndot)

            self.z_water.setValue(z1)

            self.z_toluene.setValue(1. - z1)

            n_mols_water = self.z_water.value*self.ndot.value

            n_mols_toluene = self.z_toluene.value*self.ndot.value

            MW_water = self.property_package["water"].MW

            MW_toluene = self.property_package["toluene"].MW

            self.w_water.setValue((n_mols_water*MW_water*1e-3)/((n_mols_water*MW_water*1e-3)+(n_mols_toluene*MW_toluene*1e-3)))

            self.w_toluene.setValue(1. - self.w_water.value)

            self.T.setValue(298.15)

            self.H.setValue(0.)

            self.P.setValue(101325.)
    #----------------------------------------------

    bfms1 = biphasic_material_stream("BFMS1", 100., .6)
    bfms1()
    bfms2 = biphasic_material_stream("BFMS2", 200., .4)
    bfms2()
    bfms3 = biphasic_material_stream("BFMS3", 500., .8)
    bfms3()

    prob.addModels([biphasic_mixer, bfms1, bfms2, bfms3])

    prob.createConnection("", biphasic_mixer, Min(bfms1.T(), bfms2.T()), biphasic_mixer.T_in())

    prob.createConnection("", biphasic_mixer, bfms1.mdot()+bfms2.mdot()+bfms3.mdot(), biphasic_mixer.mdot_in())

    prob.createConnection("", biphasic_mixer, bfms1.ndot()+bfms2.ndot()+bfms3.ndot(), biphasic_mixer.ndot_in())

    prob.createConnection("", biphasic_mixer, Min(bfms1.P(),bfms2.P(),bfms3.P()), biphasic_mixer.P_in())

    prob.createConnection("", biphasic_mixer, bfms1.H()*bfms1.ndot() + bfms2.H()*bfms2.ndot() + bfms3.H()*bfms3.ndot(), biphasic_mixer.ndot_in()*biphasic_mixer.H_in())

    prob.createConnection("", biphasic_mixer, bfms1.z_water()*bfms1.ndot() + bfms2.z_water()*bfms2.ndot() + bfms3.z_water()*bfms3.ndot(), biphasic_mixer.z_water_in()*biphasic_mixer.ndot_in())

    prob.createConnection("", biphasic_mixer, bfms1.w_water()*bfms1.mdot() + bfms2.w_water()*bfms2.mdot() + bfms3.w_water()*bfms3.mdot(), biphasic_mixer.w_water_in()*biphasic_mixer.mdot_in())

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print("Results = ",results)

    assert results["mdot_out_BFM0"] == pytest.approx( bfms1.mdot.value + bfms2.mdot.value + bfms3.mdot.value )

    assert results["mdot_out_BFM0"] == pytest.approx(results["mdot_in_BFM0"])

    assert results["ndot_out_BFM0"] == pytest.approx(results["ndot_in_BFM0"])

    assert results["ndot_out_BFM0"] == pytest.approx( bfms1.ndot.value + bfms2.ndot.value + bfms3.ndot.value )


def test_simple_mixer_valve_homogeneous_material_stream(simple_mixer, valve_class, prob, sim, pp_water):

    """
    Test for simulation of the mixer problem using models for material streams and valve class
    """

    simple_mixer = simple_mixer("M0", "Simple mixer", pp_water)
    simple_mixer()

    simple_valve = valve_class("V0", "Simple valve", pp_water)
    simple_valve.Delta_P.setValue(20e3)
    simple_valve.perc_open.setValue(.5)
    simple_valve()

    #---------------------------------------------
    #Create a homogeneous material_stream model

    class homogeneous_material_stream(MaterialStream):

        def __init__(self, name, mdot, description="Homogeneous material stream", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.mdot.setValue(mdot)

            self.T.setValue(298.15)

            self.H.setValue(0.)

            self.P.setValue(101325.)
    #----------------------------------------------

    hms1 = homogeneous_material_stream("HMS1", 100.)
    hms1.P.setValue(120e3)
    hms1()
    hms2 = homogeneous_material_stream("HMS2", 200.)
    hms2()

    prob.addModels([simple_mixer, hms1, hms2, simple_valve])

    prob.createConnection("", simple_mixer, Min(hms1.T(), hms2.T()), simple_mixer.T_in())

    prob.createConnection("", simple_mixer, hms1.mdot()+hms2.mdot(), simple_mixer.mdot_in())

    prob.createConnection("", simple_mixer, hms1.ndot()+hms2.ndot(), simple_mixer.ndot_in())

    prob.createConnection("", simple_mixer, Min(hms1.P(), hms2.P()), simple_mixer.P_in())

    prob.createConnection("", simple_mixer, hms1.ndot()*hms1.H() + hms2.ndot()*hms1.H(), simple_mixer.ndot_in()*simple_mixer.H_in())

    prob.createConnection(simple_mixer, simple_valve, simple_mixer.mdot_out, simple_valve.mdot_in)

    prob.createConnection(simple_mixer, simple_valve, simple_mixer.ndot_out, simple_valve.ndot_in)

    prob.createConnection(simple_mixer, simple_valve, simple_mixer.P_out, simple_valve.P_in)

    prob.createConnection(simple_mixer, simple_valve, simple_mixer.T_out, simple_valve.T_in)

    prob.createConnection(simple_mixer, simple_valve, simple_mixer.H_out, simple_valve.H_in)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print(results)

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )

    assert results["mdot_out_V0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["mdot_out_V0"] == pytest.approx(results["mdot_in_V0"])

    assert results["ndot_out_V0"] == pytest.approx(results["ndot_out_M0"])

    assert results["P_out_V0"] == pytest.approx(results["P_out_M0"]-20e3)

    assert results["Qdot_out_V0"] == pytest.approx(.5 * results["mdot_out_M0"]/pp_water["*"].rho)


def test_mixer_homogeneous_material_stream_heater(simple_mixer, simple_heater, prob, sim, pp_water):

    """
    Test for simulation of the mixer problem using models for material streams and heater
    """

    simple_mixer = simple_mixer("M0", "Simple mixer", pp_water)
    simple_mixer()

    simple_heater = simple_heater("H0", "Simple heater", pp_water)
    simple_heater.Q.setValue(1e8) #100 GW
    simple_heater.Delta_P.setValue(0.)
    simple_heater()

    #---------------------------------------------
    #Create a homogeneous material_stream model

    class homogeneous_material_stream(MaterialStream):

        def __init__(self, name, mdot, description="Homogeneous material stream", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.mdot.setValue(mdot)

            self.T.setValue(298.15)

            self.H.setValue(0.)

            self.P.setValue(101325.)
    #----------------------------------------------

    hms1 = homogeneous_material_stream("HMS1", 100.)
    hms1.P.setValue(120e3)
    hms1()
    hms2 = homogeneous_material_stream("HMS2", 200.)
    hms2()

    prob.addModels([simple_mixer, simple_heater, hms1, hms2])

    prob.createConnection("", simple_mixer, Min(hms1.T(), hms2.T()), simple_mixer.T_in())

    prob.createConnection("", simple_mixer, hms1.mdot()+hms2.mdot(), simple_mixer.mdot_in())

    prob.createConnection("", simple_mixer, hms1.ndot()+hms2.ndot(), simple_mixer.ndot_in())

    prob.createConnection("", simple_mixer, Min(hms1.P(), hms2.P()), simple_mixer.P_in())

    prob.createConnection("", simple_mixer, hms1.ndot()*hms1.H() + hms2.ndot()*hms1.H(), simple_mixer.ndot_in()*simple_mixer.H_in())

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.T_out, simple_heater.T_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.P_out, simple_heater.P_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.mdot_out, simple_heater.mdot_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.ndot_out, simple_heater.ndot_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.H_out, simple_heater.H_in)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    #print(Analysis().problemReport(prob))

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print("\nResults = ",results)

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )

    assert results["T_out_H0"] > results["T_in_H0"]


def test_pump_mixer_heater_homogeneous_material_stream_heater(simple_mixer, simple_heater, prob, sim, pp_water):

    """
    Test for simulation of the mixer problem using models for material streams, a pump and a heater
    """

    simple_mixer = simple_mixer("M0", "Simple mixer", pp_water)
    simple_mixer()

    simple_heater = simple_heater("H0", "Simple heater", pp_water)
    simple_heater.Q.setValue(1e8) #100 GW
    simple_heater.Delta_P.setValue(0.)
    simple_heater()

    #---------------------------------------------
    #Create a homogeneous material_stream model

    class homogeneous_material_stream(MaterialStream):

        def __init__(self, name, mdot, description="Homogeneous material stream", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.mdot.setValue(mdot)

            self.T.setValue(298.15)

            self.H.setValue(0.)

            self.P.setValue(101325.)
    #----------------------------------------------

    hms1 = homogeneous_material_stream("HMS1", 100.)
    hms1.P.setValue(120e3)
    hms1()
    hms2 = homogeneous_material_stream("HMS2", 200.)
    hms2()

    #-----------------------------------------------
    #Create a damn simple pump
    class simple_pump(SimplePump):

        def __init__(self, name, Delta_P, description="A simple pump", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.Delta_P.setValue(Delta_P)
    #-----------------------------------------------

    spmp = simple_pump("SP0",2*101325.)
    spmp()

    prob.addModels([spmp, simple_mixer, simple_heater, hms1, hms2])

    prob.createConnection("", simple_mixer, Min(spmp.T_out(), hms2.T()), simple_mixer.T_in())

    prob.createConnection("", simple_mixer, spmp.mdot_out()+hms2.mdot(), simple_mixer.mdot_in())

    prob.createConnection("", simple_mixer, spmp.ndot_out()+hms2.ndot(), simple_mixer.ndot_in())

    prob.createConnection("", simple_mixer, Min(spmp.P_out(), hms2.P()), simple_mixer.P_in())

    prob.createConnection("", simple_mixer, spmp.ndot_out()*spmp.H_out() + hms2.ndot()*hms1.H(), simple_mixer.ndot_in()*simple_mixer.H_in())

    prob.createConnection("", spmp, hms1.T(), spmp.T_in())

    prob.createConnection("", spmp, hms1.P(), spmp.P_in())

    prob.createConnection("", spmp, hms1.H(), spmp.H_in())

    prob.createConnection("", spmp, hms1.mdot(), spmp.mdot_in())

    prob.createConnection("", spmp, hms1.ndot(), spmp.ndot_in())

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.T_out, simple_heater.T_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.P_out, simple_heater.P_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.mdot_out, simple_heater.mdot_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.ndot_out, simple_heater.ndot_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.H_out, simple_heater.H_in)

    prob.resolve()

    '''
    prob.createGraphModelConnection(hms1, spmp)

    prob.createGraphModelConnection(hms2, simple_mixer)

    prob.createGraphModelConnection(spmp, simple_mixer)

    prob.drawConnectionGraph('/home/hfsf/out.png', show_model_headings=False)
    '''

    sim.setProblem(prob)

    sim.setConfigurations()

    #print(Analysis().problemReport(prob))

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print("\nResults = ",results)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )

    assert results["P_out_SP0"] == pytest.approx(hms1.P.value+2*101325.)

    assert results["mdot_out_SP0"] == pytest.approx(hms1.mdot.value)

    assert results["ndot_out_SP0"] == pytest.approx(hms1.ndot.value)

    assert results["P_out_SP0"] > results["P_in_SP0"]

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )

    assert results["T_out_H0"] > results["T_in_H0"]


def test_pump_mixer_heater_hms(simple_mixer, simple_heater, prob, sim, pp_water):

    """
    Test for simulation of the mixer problem using models for material streams, a pump and a heater
    """

    simple_mixer = simple_mixer("M0", "Simple mixer", pp_water)
    simple_mixer()

    simple_heater = simple_heater("H0", "Simple heater", pp_water)
    simple_heater.Q.setValue(1e8) #100 GW
    simple_heater.Delta_P.setValue(0.)
    simple_heater()

    #---------------------------------------------
    #Create a homogeneous material_stream model

    class homogeneous_material_stream(MaterialStream):

        def __init__(self, name, mdot, description="Homogeneous material stream", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.mdot.setValue(mdot)

            self.T.setValue(298.15)

            self.H.setValue(0.)

            self.P.setValue(101325.)
    #----------------------------------------------

    hms1 = homogeneous_material_stream("HMS1", 100.)
    hms1.P.setValue(120e3)
    hms1()
    hms2 = homogeneous_material_stream("HMS2", 200.)
    hms2()

    #-----------------------------------------------
    #Create a damn simple pump
    class simple_pump(SimplePump):

        def __init__(self, name, Delta_P, description="A simple pump", property_package=pp_water):

            super().__init__(name, description, property_package)

            self.Delta_P.setValue(Delta_P)
    #-----------------------------------------------

    spmp = simple_pump("SP0",2*101325.)
    spmp()

    prob.addModels([spmp, simple_mixer, simple_heater, hms1, hms2])

    prob.createConnection("", simple_mixer, Min(spmp.T_out(), hms2.T()), simple_mixer.T_in())

    prob.createConnection("", simple_mixer, spmp.mdot_out()+hms2.mdot(), simple_mixer.mdot_in())

    prob.createConnection("", simple_mixer, spmp.ndot_out()+hms2.ndot(), simple_mixer.ndot_in())

    prob.createConnection("", simple_mixer, Min(spmp.P_out(), hms2.P()), simple_mixer.P_in())

    prob.createConnection("", simple_mixer, spmp.ndot_out()*spmp.H_out() + hms2.ndot()*hms1.H(), simple_mixer.ndot_in()*simple_mixer.H_in())

    prob.createConnection("", spmp, hms1.T(), spmp.T_in())

    prob.createConnection("", spmp, hms1.P(), spmp.P_in())

    prob.createConnection("", spmp, hms1.H(), spmp.H_in())

    prob.createConnection("", spmp, hms1.mdot(), spmp.mdot_in())

    prob.createConnection("", spmp, hms1.ndot(), spmp.ndot_in())

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.T_out, simple_heater.T_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.P_out, simple_heater.P_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.mdot_out, simple_heater.mdot_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.ndot_out, simple_heater.ndot_in)

    prob.createConnection(simple_mixer, simple_heater, simple_mixer.H_out, simple_heater.H_in)

    prob.resolve()

    '''
    prob.createGraphModelConnection(hms1, spmp)

    prob.createGraphModelConnection(hms2, simple_mixer)

    prob.createGraphModelConnection(spmp, simple_mixer)

    prob.drawConnectionGraph('/home/hfsf/out.png', show_model_headings=False)
    '''

    sim.setProblem(prob)

    sim.setConfigurations()

    #print(Analysis().problemReport(prob))

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print("\nResults = ",results)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )

    assert results["P_out_SP0"] == pytest.approx(hms1.P.value+2*101325.)

    assert results["mdot_out_SP0"] == pytest.approx(hms1.mdot.value)

    assert results["ndot_out_SP0"] == pytest.approx(hms1.ndot.value)

    assert results["P_out_SP0"] > results["P_in_SP0"]

    assert results["ndot_out_M0"] == pytest.approx( hms1.ndot.value + hms2.ndot.value  )

    assert results["T_out_H0"] > results["T_in_H0"]

