#test_model_inheritance.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.model import Model
from src.sloth.problem import Problem
from src.sloth.simulation import Simulation
from src.sloth.optimization import Optimization, OptimizationProblem

from src.sloth.core.equation_operators import *
from src.sloth.core.template_units import *
from src.sloth.core.domain import *

"""
Create a simple Model for incorporation tests
"""

class mod1(Model):

    def __init__(self, name, description=""):

        super().__init__(name, description)

        self.d = self.createVariable("d",dimless,"e")
        self.f = self.createParameter("f",dimless,"f")
        self.f.setValue(3.)

        self.createEquation("eq1", "Generic equation 1", self.d() + self.f())

@pytest.fixture
def mod2():

    """
    Create a simple model for incorporation tests
    """

    class mod2(mod1):

        def __init__(self, name, description):

            super().__init__(name, "Model 1")

            self.a = self.createVariable("a",dimless,"a")
            self.b = self.createVariable("b",dimless,"b")
            self.c = self.createParameter("c",dimless,"c")
            self.c.setValue(2.)

            eq21 = self.a() + self.b() + self.c()
            eq22 = self.b() - self.f()

            self.createEquation("eq21", "Generic equation 2.1", eq21)

            self.createEquation("eq22", "Generic equation 2.2", eq22)

    mod = mod2("M2", "Model 2")

    mod()

    return mod

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

def test_model_incorporation(mod2):

    """
    Test model incorporation
    """

    mod1_ = mod1("M1", "Model 1")

    mod1_()

    print("\n\n===>",mod2.parameters)
    print("\n\n--->",mod1_.parameters)

    assert mod2.parameters['f_M2'].value == mod1_.parameters['f_M1'].value

def test_incorporated_model_solution(prob, mod2, sim):

    prob.addModels(mod2)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    results = sim.getResults('dict')

    expected = {'a_M2':-5., 'b_M2':3., 'd_M2':-3.}

    assert results == pytest.approx(expected)

