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

        self.d = self.createVariable("d",dimless,"d")
        self.f = self.createParameter("f",dimless,"f")
        self.f.setValue(3.)

        self.createEquation("eq1a", "Generic equation 1", self.d() + self.f())

class mod1b(Model):

    def __init__(self, name, description=""):

        super().__init__(name, description)

        self.g = self.createVariable("g",dimless,"g")
        self.h = self.createParameter("h",dimless,"h")
        self.h.setValue(7.)

        self.createEquation("eq1b", "Generic equation 1", self.g() + self.h())

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
def mod3():

    """
    Create a simple model for multiple incorporation tests
    """

    class mod3(mod1, mod1b, Model):

        def __init__(self, name, description):

            super().__init__(name, "Model 3")

            self.a = self.createVariable("a",dimless,"a")
            self.b = self.createVariable("b",dimless,"b")
            self.k = self.createVariable("k",dimless,"k")
            self.c = self.createParameter("c",dimless,"c")
            self.c.setValue(2.)

            eq21 = self.a() + self.b() + self.c()
            eq22 = self.b() - self.f()
            eq23 = self.k() - self.g() - self.h()

            self.createEquation("eq31", "Generic equation 3.1", eq21)
            self.createEquation("eq32", "Generic equation 3.2", eq22)
            self.createEquation("eq33", "Generic equation 3.3", eq23)

    mod = mod3("M3", "Model 3")

    mod()

    return mod

@pytest.fixture
def mod_():

    """
    Create a simple model for multiple incorporation tests
    """

    class mod_(Model):

        def __init__(self, name, description):

            super().__init__(name, "Model 3")

            m1 = mod1("M1","Model 1")
            m1()
            m1b =mod1b("M1b", "Model 1b")
            m1b()

            self._incorporateFromModel(m1)
            self._incorporateFromModel(m1b)

        def DeclareVariables(self):

            self.a = self.createVariable("a",dimless,"a")
            self.b = self.createVariable("b",dimless,"b")
            self.k = self.createVariable("k",dimless,"k")

        def DeclareParameters(self):

            self.c = self.createParameter("c",dimless,"c")
            self.c.setValue(2.)

        def DeclareEquations(self):

            eq21 = self.a() + self.b() + self.c()
            eq22 = self.b() - self.f()
            eq23 = self.k() - self.g() - self.h()

            self.createEquation("eq31", "Generic equation 3.1", eq21)
            self.createEquation("eq32", "Generic equation 3.2", eq22)
            self.createEquation("eq33", "Generic equation 3.3", eq23)

    mod = mod_("M3", "Model 3")

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

def test_single_model_incorporation(mod2):

    """
    Test model incorporation
    """

    mod1_ = mod1("M1", "Model 1")

    mod1_()

    print("\n\n===>",mod2.parameters)
    print("\n\n--->",mod1_.parameters)

    assert mod2.parameters['f_M2'].value == mod1_.parameters['f_M1'].value


def test_multiple_model_incorporation(mod3):

    """
    Test model incorporation
    """

    mod1a_ = mod1("M1a", "Model 1a")
    mod1b_ = mod1b("M1b", "Model 1b")

    mod1a_()
    mod1b_()

    print("\n\n===> Parameters(mod3): ",mod3.parameters)
    print("\n\n===> Constants(mod3): ",mod3.constants)
    print("\n\n===> Variables(mod3): ",mod3.variables)
    print("\n\n===> Equations(mod3): ",mod3.equations)

    print("\n\n===> Parameters(mod1a): ",mod1a_.parameters)
    print("\n\n===> Constants(mod1a): ",mod1a_.constants)
    print("\n\n===> Variables(mod1a): ",mod1a_.variables)
    print("\n\n===> Equations(mod1a): ",mod1a_.equations)


    print("\n\n===> Parameters(mod1b): ",mod1b_.parameters)
    print("\n\n===> Constants(mod1b): ",mod1b_.constants)
    print("\n\n===> Variables(mod1b): ",mod1b_.variables)
    print("\n\n===> Equations(mod1b): ",mod1b_.equations)

    assert mod3.parameters['f_M3'].value == mod1a_.parameters['f_M1a'].value
    assert mod3.parameters['h_M3'].value == mod1b_.parameters['h_M1b'].value

def test_single_incorporated_model_solution(prob, mod2, sim):

    prob.addModels(mod2)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    results = sim.getResults('dict')

    expected = {'a_M2':-5., 'b_M2':3., 'd_M2':-3.}

    assert results == pytest.approx(expected)


def test_multiple_incorporated_model_solution(prob, mod3, sim):

    prob.addModels(mod3)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    results = sim.getResults('dict')

    print("\n\n==>Results = ",results)

    expected = {'a_M3':-5., 'b_M3':3., 'd_M3':-3., 'g_M3':-7., 'k_M3':0.}

    assert results == pytest.approx(expected)

def donot_test_incorporateFromModel_feature(prob, mod_, sim):

    mod_._infoModelReport_()

    prob.addModels(mod_)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations()

    sim.runSimulation()

    results = sim.getResults('dict')

    print("\n\n==>Results = ",results)

    expected = {'a_M3':-5., 'b_M3':3., 'd_M3':-3., 'g_M3':-7., 'k_M3':0.}

    assert results == pytest.approx(expected)




