#test_mass_conservation.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.model import Model
from src.sloth.problem import Problem
from src.sloth.simulation import Simulation

from src.sloth.unit_op import *

from src.sloth.core.equation_operators import *
from src.sloth.core.template_units import *
from src.sloth.core.domain import *


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

            self.h_out =  self.createVariable("h_out", J, "enthalpy for output stream", is_exposed=True, type='output')

            self.mdot_1.setValue(100.)
            self.mdot_2.setValue(200.)
            self.molar_mass.setValue(0.018)

            self.P_1.setValue(1.)
            self.P_2.setValue(.8)

        def DeclareEquations(self):

            self.eq1 = self.createEquation("eq1", "Input mass flow", self.mdot_in() - self.mdot_1() - self.mdot_2() )
            self.eq2 = self.createEquation("eq2", "Input molar flow", self.ndot_in() - self.mdot_in()/self.molar_mass() )
            self.eq3 = self.createEquation("eq3", "Pressure input", self.P_in() - min(self.P_1.value, self.P_2.value))
            self.eq4 = self.createEquation("eq4", "Enthalpy output", self.h_out() )

    m_mod = mix_model("M0","Model for simple stream mixer")

    m_mod()

    return m_mod


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


def test_simulation_only_mixer(mod_1, prob, sim):

    """
    Test for simulation of the mixer problem
    """

    prob.addModels(mod_1)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    assert results["mdot_out_M0"] == pytest.approx(300.)


def test_simulation_mixer_and_valves(mod_1, valve_mod, prob, sim):

    """
    Test for simulation of the mixer problem, with one valve in the output stream
    -1---> |M| <---2-
            |
           |V|
            |
            v
           out
    """

    prob.addModels([mod_1, valve_mod])

    prob.createConnection(mod_1, valve_mod, mod_1.mdot_out, valve_mod.mdot_in)

    prob.createConnection(mod_1, valve_mod, mod_1.ndot_out, valve_mod.ndot_in)

    prob.createConnection(mod_1, valve_mod, mod_1.P_out, valve_mod.P_in) # P

    prob.createConnection(mod_1, valve_mod, mod_1.h_out, valve_mod.h_in) # h

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation(show_output_msg=True)

    results = sim.getResults( return_type='dict')

    assert results["mdot_out_V0"] == pytest.approx(300.)
    assert results["ndot_out_V0"] == pytest.approx(300/0.018)
