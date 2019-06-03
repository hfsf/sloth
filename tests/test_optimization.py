#test_optimization.py

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

import copy

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
            self.a =  self.createParameter("a", dimless, "A")
            self.b =  self.createConstant("b", dimless, "B")
            self.c =  self.createConstant("c", dimless, "C")
            self.d =  self.createConstant("d", dimless, "D")
            self.t = self.createVariable("t", dimless, "t")

            self.dom = Domain("domain",dimless,self.t,"generic domain")

            self.u.distributeOnDomain(self.dom)
            self.v.distributeOnDomain(self.dom)

            #self.a.setValue(1.)
            self.b.setValue(0.1)
            self.c.setValue(1.5)
            self.d.setValue(0.75)

        def DeclareEquations(self):

            expr1 = self.u.Diff(self.t) == self.a()*self.u() - self.b()*self.u()*self.v()

            expr2 = self.v.Diff(self.t) ==  self.d()*self.b()*self.u()*self.v() -self.c()*self.v()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)

    diff_mod = differential_model("D0","Differential model")

    diff_mod._infoModelReport_()

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

    simul_ = simul("simul", "generic simulation")

    return simul_

@pytest.fixture
def prob_opt(mod):
    """
    Create a generic optimization problem
    """

    class problem_optimization(OptimizationProblem):

        def __init__(number_dimensions):

            super().__init__(number_dimensions)

        def DeclareObjectiveFunction(self, x):

            if not isinstance(x, float):

                x = x[0]

            self.simulation_instance[mod.a].setValue(x)

            #Reload problem definitions (Equation symbolic objects etc)

            self.simulation_instance.problem.resolve()

            self.simulation_instance.setConfigurations(
                                        definition_dict=self.simulation_configuration
                            )

            self.simulation_instance.runSimulation()

            result = self.simulation_instance.getResults('dict')

            f = (result['t_D0']['Preys(u)'][-1] - 8.38505427)**2 + (result['t_D0']['Predators(v)'][-1] - 7.1602100083)**2

            #Reset simulation to remove previous results

            self.simulation_instance.reset()

            return [f]

    prob_opt_ = problem_optimization()

    prob_opt_()

    return prob_opt_

@pytest.fixture
def opt(sim, mod, prob, prob_opt):
    """
    Create a generic optimization study
    """

    class opt_study(Optimization):

        def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints, optimization_configuration=None):

            super().__init__(simulation=sim,
                             optimization_problem=optimization_problem,
                             simulation_configuration=simulation_configuration,
                             optimization_parameters=optimization_parameters,
                             constraints=constraints,
                             optimization_configuration=optimization_configuration)

    prob.setTimeVariableName(['t_D0'])

    prob.resolve()

    prob.setInitialConditions({'t_D0':0.,'u_D0':10.,'v_D0':5.})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0.,
                  end_time=16.,
                  is_dynamic=True,
                  domain=mod.dom,
                  print_output=False,
                  compile_equations=True,
                  output_headers=["Time","Preys(u)","Predators(v)"],
                  variable_name_map={"t_D0":"Time(t)",
                                     "u_D0":"Preys(u)",
                                     "v_D0":"Predators(v)"
                            }
            )

    prob_opt()

    return opt_study(sim, prob_opt, None, [mod.a], [-10., 10.], None)

def test_model_properties(mod):

    assert mod.name == "D0"

    assert mod.description == "Differential model"

    assert list(mod.variables.keys()) == ["u_D0","v_D0","t_D0"]

    assert list(mod.constants.keys()) == ["b_D0","c_D0", "d_D0"]

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

@pytest.mark.parametrize("compile_equations",[True,False])
def test_simulation_result(mod, prob, sim, compile_equations):

    mod.a.setValue(1.) # set value of parameter defined for optimization

    mod()

    prob.addModels(mod)

    prob.setTimeVariableName(['t_D0'])

    prob.resolve()

    prob.setInitialConditions({'t_D0':0.,'u_D0':10.,'v_D0':5.})

    sim.setProblem(prob)

    print("===>mod.a:%s"%mod.a)
    print("===>prob.elementary_equations:%s"%[i.elementary_equation_expression for i in prob._equation_list])
    print("===>prob.equations:%s"%[i.equation_expression for i in prob._equation_list])

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

def test_optimization(mod, prob, sim, opt, prob_opt):

    prob.addModels(mod)

    prob.setTimeVariableName(['t_D0'])

    prob.resolve()

    prob.setInitialConditions({'t_D0':0.,'u_D0':10.,'v_D0':5.})

    sim.setProblem(prob)

    prob_opt()

    opt.runOptimization()

    with open("test_log.backup", "w") as openfile:

        openfile.write("==>Results: {}".format(opt.getResults()))

    assert opt.getResults() is not None

    assert opt.run_sucessful is not False