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
def mod1():
    """
    Create a generic linear model
    """

    class linear_model(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.a =  self.createVariable("a", kg_s, "A")
            self.b =  self.createVariable("b", kg_s, "B")
            self.c =  self.createVariable("c", kg, "C", is_exposed=True, type='output')            
            self.d =  self.createVariable("d", kg, "D", is_exposed=True, type='output')
            self.e =  self.createConstant("e", s**-1, "D")
            self.e.setValue(0.7)

        def DeclareEquations(self):

            expr1 = self.a() + self.b() - 1.

            expr2 = self.a() + self.c()*self.e() - 2

            expr3 = self.e()*self.c() - self.a() - self.b()

            expr4 = self.c()*self.e() - self.d()*self.e()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
            self.eq3 = self.createEquation("eq3", "Equation 3", expr3)
            self.eq4 = self.createEquation("eq4", "Equation 4", expr4)

    lin_mod = linear_model("L0","Linear model")

    lin_mod()

    return lin_mod

@pytest.fixture
def mod2():
    """
    Create a generic linear model
    """

    class linear_model(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.a =  self.createVariable("a", kg_s, "A")
            self.b =  self.createVariable("b", kg_s, "B")
            self.c =  self.createVariable("c", kg, "C", is_exposed=True, type='input')
            self.d =  self.createConstant("d", s**-1, "D")
            self.d.setValue(0.7)

        def DeclareEquations(self):

            expr1 = self.a() - self.b() + 7.6

            expr2 = self.a() - 0.8*self.c()*self.d() + 1

            #expr3 = self.d()*self.c() - .6*self.a() + self.b()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
            #self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

    lin_mod = linear_model("L1","Linear model")

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

def test_model_properties(mod1):

    mod=mod1

    assert mod.name == "L0"
    
    assert mod.description == "Linear model"
    
    assert list(mod.variables.keys()) == ["a_L0","b_L0","c_L0", "d_L0"]

    assert list(mod.equations.keys()) == ["eq1_L0","eq2_L0","eq3_L0", "eq4_L0"]

def test_model_enodes(mod1):

    mod=mod1

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.a

    assert mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.b

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.eq2.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]]


def test_problem_properties(mod1, prob):

    mod=mod1

    prob.addModels(mod)

    prob.resolve()

    assert prob.name == "prob"

    assert prob.description == "generic problem"
    
    assert prob._getProblemType() == "linear"


def test_simulation_properties(mod1, mod2, prob, sim):

    mod=mod1

    prob.addModels(mod)

    prob.resolve()

    sim.setProblem(prob)

    assert sim.name == "simul"

    assert sim.description == "generic simulation"
    
    assert sim.problem == prob


def test_simulation_result(mod1, prob, sim):

    prob.addModels(mod1)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    assert sim.getResults(return_type='dict') == pytest.approx({'a_L0':1.0, 'b_L0':0.0, 'c_L0':1.4285714, 'd_L0':1.4285714})

    
def test_model_connection(mod1, mod2, prob, sim):

    prob.addModels([mod1, mod2])

    #Connection between two models

    prob.createConnection(mod1, mod2, mod1.c, mod2.c)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    print("==>%s"%sim.getResults(return_type='dict'))

    results = sim.getResults(return_type='dict')

    expected = {'a_L0':1.0, 'b_L0':0.0, 'c_L0':1.4285714285714286, 'd_L0':1.4285714285714286, 'a_L1':-0.2, 'b_L1':7.4, 'c_L1':1.4285714285714286}

    assert results == pytest.approx(expected)

    
def test_model_multi_connection(mod1, mod2, prob, sim):

    prob.addModels([mod1, mod2])

    #Connection between two models

    prob.createConnection(mod1, mod2, mod1.c, mod2.c)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    print("==>%s"%sim.getResults(return_type='dict'))

    results = sim.getResults(return_type='dict')

    expected = {'a_L0':1.0, 'b_L0':0.0, 'c_L0':1.4285714285714286, 'd_L0':1.4285714285714286, 'a_L1':-0.2, 'b_L1':7.4, 'c_L1':1.4285714285714286}

    assert results == pytest.approx(expected)

def test_model_multi_connection_2(mod1, mod2, prob, sim):

    prob.addModels([mod1, mod2])

    #Connection between two models

    prob.createConnection(mod1, mod2, [mod1.c, mod1.d], [mod2.c])

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    print("==>%s"%sim.getResults(return_type='dict'))

    results = sim.getResults(return_type='dict')

    expected = {'a_L0': 1.0, 'a_L1': 0.6, 'b_L0': 0.0, 'b_L1': 8.2, 'c_L0': 1.4285714285714286, 'c_L1': 2.857142857142857, 'd_L0': 1.4285714285714286}

    assert results == pytest.approx(expected)