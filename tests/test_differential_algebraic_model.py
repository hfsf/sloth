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
from src.sloth.core.domain import *

import copy

@pytest.fixture
def mod():
    """
    Create a generic linear model
    """

    class differential_model(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.y1 =  self.createVariable("y1", dimless, "y1")
            self.y2 =  self.createVariable("y2", dimless, "y2")
            self.y3 =  self.createVariable("y3", dimless, "y3")
            self.y4 =  self.createVariable("y4", dimless, "y4")
            self.y5 =  self.createVariable("y5", dimless, "y5")
            self.t =  self.createVariable("t", dimless, "t")

            self.dom = Domain("domain",dimless,self.t,"generic domain")

            self.y1.distributeOnDomain(self.dom)
            self.y2.distributeOnDomain(self.dom)
            self.y3.distributeOnDomain(self.dom)
            self.y4.distributeOnDomain(self.dom)
            self.y5.distributeOnDomain(self.dom)


        def DeclareEquations(self):

            expr1 = self.y1.Diff(self.t) - self.y3()

            expr2 = self.y2.Diff(self.t) - self.y4()

            expr3 = self.y3.Diff(self.t) + self.y5()*self.y1()

            expr4 = self.y4.Diff(self.t) + self.y5()*self.y2() + 9.82

            expr5 = self.y3()**2 + self.y4()**2 - self.y5()*(self.y1()**2+self.y2()**2)-9.82*self.y2()

            self.eq1 = self.createEquation("eq1", "Eq.1", expr1)
            self.eq2 = self.createEquation("eq2", "Eq.2", expr2)
            self.eq3 = self.createEquation("eq3", "Eq.3", expr3)
            self.eq4 = self.createEquation("eq4", "Eq.4", expr4)
            self.eq5 = self.createEquation("eq5", "Eq.5", expr5)

    diff_mod = differential_model("DA0","Differential Algebraic model")

    diff_mod()

    return diff_mod



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

    assert mod.name == "DA0"

    assert mod.description == "Differential Algebraic model"

    assert list(mod.variables.keys()) == ["y1_DA0","y2_DA0","y3_DA0","y4_DA0","y5_DA0","t_DA0"]

    assert list(mod.equations.keys()) == ["eq1_DA0","eq2_DA0","eq3_DA0","eq4_DA0","eq5_DA0"]

def test_model_enodes(mod):

    assert mod.eq1.equation_expression.symbolic_map[list(mod.y3().symbolic_map.keys())[0]] == mod.y3

    assert mod.eq2.equation_expression.symbolic_map[list(mod.y4().symbolic_map.keys())[0]] == mod.y4

    assert mod.eq1.equation_expression.symbolic_map[list(mod.y3().symbolic_map.keys())[0]] == mod.eq5.equation_expression.symbolic_map[list(mod.y3().symbolic_map.keys())[0]]


def test_simulation_properties(mod, prob, sim):

    prob.addModels(mod)

    prob.resolve()

    sim.setProblem(prob)

    print(sim.__dict__)

    assert sim.name == "simul"

    assert sim.description == "generic simulation"

    assert sim.problem == prob


#Test for either compile differential equations and direct symbolic evaluation
@pytest.mark.parametrize("compile_equations",[True])


def test_simulation_result(mod, prob, sim, compile_equations):

    prob.addModels(mod)

    prob.resolve()

    prob.setInitialConditions({'y1_DA0_d':0.,
                               'y2_DA0_d':0.,
                               'y3_DA0_d':0.,
                               'y4_DA0_d':-9.82,
                               'y5_DA0_d':0.,
                               'y5_DA0':5.,
                               'y4_DA0':0.,
                               'y3_DA0':0.,
                               'y2_DA0':0.,
                               'y1_DA0':1.,
                               't_DA0':0.
                            }
                        )

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0.,
                      end_time=5.,
                      is_dynamic=True,
                      domain=mod.dom,
                      number_of_time_steps=1000,
                      time_variable_name="t_DA0",
                      compile_equations=True,
                      print_output=False,
                      output_headers=["Time","y1","y2","y3","y4","y5"],
                      variable_name_map={"t_DA0":"Time(t)",
                                         "y1_DA0":"Y-1",
                                         "y2_DA0":"Y-2",
                                         "y3_DA0":"Y-3",
                                         "y4_DA0":"Y-4",
                                         "y5_DA0":"Y-5"
                                        }
                      )

    sim.runSimulation()

    result = sim.getResults('dict')

    assert result['t_DA0']['Time(t)'][0] == pytest.approx(0.)

    assert result['t_DA0']['Time(t)'][-1] == pytest.approx(5.)

    assert result['t_DA0']['Y-1'][0] == pytest.approx(1.)

    assert result['t_DA0']['Y-1'][-1] == pytest.approx(0.940142)

    assert result['t_DA0']['Y-2'][0] == pytest.approx(0.)

    assert result['t_DA0']['Y-2'][-1] == pytest.approx(-0.340922)

    assert result['t_DA0']['Y-3'][0] == pytest.approx(0.)

    assert result['t_DA0']['Y-3'][-1] == pytest.approx(-0.882047)

    assert result['t_DA0']['Y-4'][0] == pytest.approx(0.)

    assert result['t_DA0']['Y-4'][-1] == pytest.approx(-2.432436)

    assert result['t_DA0']['Y-5'][0] == pytest.approx(0.)

    assert result['t_DA0']['Y-5'][-1] == pytest.approx(10.041643)
