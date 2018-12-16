#test_model.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.model import Model
from src.sloth.problem import Problem
from src.sloth.simulation import Simulation

from src.sloth.core.equation_operators import *
from src.sloth.core.template_units import *
import copy

@pytest.fixture
def mod():
    """
    Create a generic linear model
    """

    class linear_model(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.a =  self.createVariable("a", kg_s, "A", is_exposed=True, type='output')
            self.b =  self.createVariable("b", kg_s, "B")
            self.c =  self.createVariable("c", kg, "C")
            self.d =  self.createConstant("d", s**-1, "D")
            self.d.setValue(0.7)

        def DeclareEquations(self):

            print("=>d().dict: %s"%self.d().__dict__)

            expr1 = self.a() + self.b() - 1.

            expr2 = self.a() + self.c()*self.d() - 2

            expr3 = self.d()*self.c() - self.a() - self.b()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
            self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

    lin_mod = linear_model("L0","Linear model")

    lin_mod()

    return lin_mod

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

def test_model_properties(mod):

    assert mod.name == "L0"
    
    assert mod.description == "Linear model"
    
    assert list(mod.variables.keys()) == ["a_L0","b_L0","c_L0"]

    assert list(mod.equations.keys()) == ["eq1_L0","eq2_L0","eq3_L0"]

def test_model_enodes(mod):

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.a

    assert mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.b

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.eq2.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]]


def test_problem_properties(mod,prob):

    prob.addModels(mod)

    prob.resolve()

    assert prob.name == "prob"

    assert prob.description == "generic problem"
    
    assert prob._getProblemType() == "linear"


def test_simulation_properties(mod, prob, sim):

    prob.addModels(mod)

    prob.resolve()

    sim.setProblem(prob)

    assert sim.name == "simul"

    assert sim.description == "generic simulation"
    
    assert sim.problem == prob


def test_simulation_result(mod, prob, sim):

    prob.addModels(mod)

    prob.resolve()

    sim.setProblem(prob)

    sim.runSimulation()

    assert sim.getResults(return_type='list') == pytest.approx([1.0, 0.0, 1.4285714])


