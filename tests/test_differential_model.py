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
def mod_zero():
    """
    Create a generic differential model with a zero-valued equation
    """

    class differential_model_zero(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.u = self.createVariable("u", dimless, "u")
            self.v = self.createVariable("v", dimless, "v")
            self.y = self.createVariable("y", dimless, "y")
            self.a = self.createConstant("a", dimless, "A")
            self.b = self.createConstant("b", dimless, "B")
            self.c = self.createConstant("c", dimless, "C")
            self.d = self.createConstant("d", dimless, "D")
            self.z = self.createConstant("z", dimless, "Z")

            self.t = self.createVariable("t", dimless, "t")

            self.dom = Domain("domain",dimless,self.t,"generic domain")

            self.u.distributeOnDomain(self.dom)
            self.v.distributeOnDomain(self.dom)
            self.y.distributeOnDomain(self.dom)


            self.a.setValue(1.)
            self.b.setValue(0.1)
            self.c.setValue(1.5)
            self.d.setValue(0.75)
            self.z.setValue(0.)

        def DeclareEquations(self):

            expr1 = self.u.Diff(self.t) == self.a()*self.u() - self.b()*self.u()*self.v()#*self.tf()

            expr2 = self.v.Diff(self.t) ==  self.d()*self.b()*self.u()*self.v() -self.c()*self.v()

            expr3 = self.y.Diff(self.t) == 0.

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
            self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

    diff_mod = differential_model_zero("D0","Differential model")

    diff_mod()

    return diff_mod

@pytest.fixture
def mod():
    """
    Create a generic linear model
    """

    class differential_model(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.u =  self.createVariable("u", dimless, "u")
            self.v =  self.createVariable("v", dimless, "v")
            self.a =  self.createConstant("a", dimless, "A")
            self.b =  self.createConstant("b", dimless, "B")
            self.c =  self.createConstant("c", dimless, "C")
            self.d =  self.createConstant("d", dimless, "D")
            self.t = self.createVariable("t", dimless, "t")

            self.dom = Domain("domain",dimless,self.t,"generic domain")

            self.u.distributeOnDomain(self.dom)
            self.v.distributeOnDomain(self.dom)


            self.a.setValue(1.)
            self.b.setValue(0.1)
            self.c.setValue(1.5)
            self.d.setValue(0.75)

        def DeclareEquations(self):

            expr1 = self.u.Diff(self.t) == self.a()*self.u() - self.b()*self.u()*self.v()#*self.tf()

            expr2 = self.v.Diff(self.t) ==  self.d()*self.b()*self.u()*self.v() -self.c()*self.v()

            #expr3 = self.tf.Diff(self.t) == self.a()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
            #self.eq2 = self.createEquation("eq3", "Equation 3", expr3)

    diff_mod = differential_model("D0","Differential model")

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

    assert mod.name == "D0"

    assert mod.description == "Differential model"

    print("variables: ",mod.variables.keys())

    assert list(mod.variables.keys()) == ["u_D0","v_D0","t_D0"]

    assert list(mod.constants.keys()) == ["a_D0","b_D0","c_D0", "d_D0"]

    assert list(mod.equations.keys()) == ["eq1_D0","eq2_D0"]

def test_model_enodes(mod):

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.a

    assert mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.b

    assert mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.eq2.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]]


def test_simulation_properties(mod, prob, sim):

    prob.addModels(mod)

    prob.setTimeVariableName(['t_D0'])

    prob.resolve()

    sim.setProblem(prob)

    assert sim.name == "simul"

    assert sim.description == "generic simulation"

    assert sim.problem == prob


#Test for either compile differential equations and direct symbolic evaluation
@pytest.mark.parametrize("compile_equations",[True, False])

def test_simulation_result(mod, prob, sim, compile_equations):

    prob.addModels(mod)

    prob.setTimeVariableName(['t_D0'])

    prob.resolve()

    prob.setInitialConditions({'t_D0':0., 'u_D0':10.,'v_D0':5.})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0.,
                      end_time=16.,
                      is_dynamic=True,
                      domain=mod.dom,
                      print_output=False,
                      compile_equations=compile_equations,
                      output_headers=["Time","Preys(u)","Predators(v)"],
                      variable_name_map={"t_D0":"Time(t)",
                                         "u_D0":"Preys(u)",
                                         "v_D0":"Predators(v)"
                                }
                )

    sim.runSimulation()

    result = sim.getResults('dict')

    assert result['t_D0']['Time(t)'][0] == pytest.approx(0.)

    assert result['t_D0']['Time(t)'][-1] == pytest.approx(16.)

    assert result['t_D0']['Preys(u)'][0] == pytest.approx(10.)

    assert result['t_D0']['Preys(u)'][-1] == pytest.approx(8.38505427)

    assert result['t_D0']['Predators(v)'][0] == pytest.approx(5.)

    assert result['t_D0']['Predators(v)'][-1] == pytest.approx(7.1602100083)

    sim.showResults()


@pytest.mark.parametrize("compile_equations",[True, False])

def test_equation_zero_variable(mod_zero, prob, sim, compile_equations):

    prob.addModels(mod_zero)

    prob.setTimeVariableName(['t_D0'])

    prob.resolve()

    prob.setInitialConditions({'t_D0':0., 'u_D0':10.,'v_D0':5., 'y_D0':0.})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0.,
                      end_time=16.,
                      is_dynamic=True,
                      domain=mod_zero.dom,
                      print_output=False,
                      compile_equations=compile_equations,
                      output_headers=["Time", "Preys(u)", "Predators(v)", "Scum(y)"],
                      variable_name_map={"t_D0":"Time(t)",
                                         "u_D0":"Preys(u)",
                                         "v_D0":"Predators(v)",
                                         "y_D0":"Scum(y)"
                                }
                )

    sim.runSimulation()

    result = sim.getResults('dict')

    assert result['t_D0']['Time(t)'][0] == pytest.approx(0.)

    assert result['t_D0']['Time(t)'][-1] == pytest.approx(16.)

    assert result['t_D0']['Scum(y)'][0] == pytest.approx(0.)

    assert result['t_D0']['Scum(y)'][-1] == pytest.approx(0.)

    assert result['t_D0']['Preys(u)'][0] == pytest.approx(10.)

    assert result['t_D0']['Preys(u)'][-1] == pytest.approx(8.38505427)

    assert result['t_D0']['Predators(v)'][0] == pytest.approx(5.)

    assert result['t_D0']['Predators(v)'][-1] == pytest.approx(7.1602100083)

    sim.showResults()

    #assert False

    #Removed ridiculously wrong test for zero-valued differential equations