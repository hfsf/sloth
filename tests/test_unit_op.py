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

from src.sloth.unit_op import *

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
def mod_1():
    """
    Create a mass conversation model for a case of two streams being mixed
    -1--> |M| <--2-
           |
           v
           out
    """

    class mix_model(Mixer):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.P_1 =  self.createParameter("P_1", Pa, "Pressure from stream 1")
            self.P_2 =  self.createParameter("P_2", Pa, "Pressure from from stream 2")

            self.mdot_1 =  self.createParameter("mdot_1", kg/s, "mass flux from stream 1")
            self.mdot_2 =  self.createParameter("mdot_2", kg/s, "mass flux from stream 2")

            self.molar_mass = self.createConstant("molar_mass", kg/mol, "molar mass")

            self.mdot_out =  self.createVariable("mdot_out", kg/s, "mass flux from output stream", is_exposed=True, type='output')

            self.H_out =  self.createVariable("H_out", J/mol, "molar enthalpy for output stream", latex_text="H_{out}", is_exposed=True, type='output')

            self.mdot_1.setValue(100.)
            self.mdot_2.setValue(200.)
            self.molar_mass.setValue(0.018)

            self.P_1.setValue(1.)
            self.P_2.setValue(.8)

        def DeclareEquations(self):

            self.eq1 = self.createEquation("eq1", "Input mass flow", self.mdot_in() - self.mdot_1() - self.mdot_2() )
            self.eq2 = self.createEquation("eq2", "Input molar flow", self.ndot_in() - self.mdot_in()/self.molar_mass() )
            self.eq3 = self.createEquation("eq3", "Pressure input", self.P_in() - min(self.P_1.value, self.P_2.value))
            self.eq4 = self.createEquation("eq4", "Enthalpy output", self.H_out() )

    m_mod = mix_model("M0","Model for simple stream mixer")

    m_mod()

    return m_mod

@pytest.fixture
def simple_mixer():

    class mix_model(Mixer):

        def __init__(self, name, description):

            super().__init__(name, description)

    m_mod = mix_model("M0","Model for simple stream mixer")

    m_mod()

    return m_mod

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
def valve_mod():
    """
    Create a model for a valve using predefined unit operation from the library of current software
    """

    class valve_model(Valve):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.Delta_P.setValue(0.)

    valve_model = valve_model("V0","Model for valve")

    valve_model()

    return valve_model

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

def donot_test_mixer_and_homogeneous_material_stream(simple_mixer, prob, sim, pp_water):

    """
    Test for simulation of the mixer problem using models for material streams
    """

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

    prob.createConnection("", simple_mixer, hms1.mdot_out()+hms2.mdot_out(), simple_mixer.mdot_in())

    prob.createConnection("", simple_mixer, hms1.ndot_out()+hms2.ndot_out(), simple_mixer.ndot_in())

    prob.createConnection("", simple_mixer, Min(hms1.P_out(), hms2.P_out()), simple_mixer.P_in())

    prob.createConnection("", simple_mixer, hms1.H_out(), simple_mixer.H_in())

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    print(results)

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["ndot_out_M0"] == pytest.approx( results["ndot_out_HMS1"]+results["ndot_out_HMS2"]  )


def test_biphasic_mixer_and_biphasic_material_stream(biphasic_mixer_class, prob, sim, pp_water_toluene):

    """
    Test for simulation of the mixer problem using models for material streams
    """

    biphasic_mixer = biphasic_mixer_class("BFM0", "Model for biphasic mixer", pp_water_toluene)
    biphasic_mixer()

    #---------------------------------------------
    #Create a homogeneous material_stream model

    class biphasic_material_stream(MultiphasicMaterialStream):

        def __init__(self, name, ndot, x1, description="Biphasic material stream", property_package=pp_water_toluene):

            super().__init__(name, description, property_package)

            self.ndot.setValue(ndot)

            self.x_water.setValue(x1)

            self.x_toluene.setValue(1. - x1)

            n_mols_water = self.x_water.value*self.ndot.value

            n_mols_toluene = self.x_toluene.value*self.ndot.value

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

    prob.addModels([biphasic_mixer, bfms1, bfms2])

    prob.createConnection("", biphasic_mixer, bfms1.mdot_out()+bfms2.mdot_out(), biphasic_mixer.mdot_in())

    prob.createConnection("", biphasic_mixer, bfms1.ndot_out()+bfms2.ndot_out(), biphasic_mixer.ndot_in())

    prob.createConnection("", biphasic_mixer, Min(bfms1.P_out(),bfms2.P_out()), biphasic_mixer.P_in())

    prob.createConnection("", biphasic_mixer, bfms1.H_out(), biphasic_mixer.H_in())

    prob.createConnection("", biphasic_mixer, bfms1.x_water_out()*bfms1.ndot_out() + bfms2.x_water_out()*bfms2.ndot_out(), biphasic_mixer.x_water_in()*biphasic_mixer.ndot_in())

    prob.createConnection("", biphasic_mixer, bfms1.w_water_out()*bfms1.mdot_out() + bfms2.w_water_out()*bfms2.mdot_out(), biphasic_mixer.w_water_in()*biphasic_mixer.mdot_in())

    prob.resolve()

    print(Analysis().problemReport(prob))

    #tty = input("...")

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    assert results["mdot_out_M0"] == pytest.approx(hms1.mdot.value+hms2.mdot.value)

    assert results["mdot_out_M0"] == pytest.approx(results["mdot_in_M0"])

    assert results["ndot_out_M0"] == pytest.approx( results["ndot_out_HMS1"]+results["ndot_out_HMS2"]  )
