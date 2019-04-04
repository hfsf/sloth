#test_plotter.py

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

import os


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

            expr1 = self.u.Diff(self.t) == self.a()*self.u() - self.b()*self.u()*self.v()

            expr2 = self.v.Diff(self.t) ==  self.d()*self.b()*self.u()*self.v() -self.c()*self.v()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)

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


@pytest.mark.parametrize("compile_equations",[True, False])
@pytest.mark.parametrize("short_reference_to_domain",[True, False])

def test_plotter_after_simulation(mod, prob, sim, compile_equations, short_reference_to_domain):

    prob.addModels(mod)

    prob.resolve()

    prob.setInitialConditions({'t_D0':0.,'u_D0':10.,'v_D0':5.})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0.,
                      end_time=16.,
                      is_dynamic=True,
                      domain=mod.dom,
                      time_variable_name="t_D0",
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

    #Check if all results are OK

    assert result['t_D0']['Time(t)'][0] == pytest.approx(0.)

    assert result['t_D0']['Time(t)'][-1] == pytest.approx(16.)

    assert result['t_D0']['Preys(u)'][0] == pytest.approx(10.)

    assert result['t_D0']['Preys(u)'][-1] == pytest.approx(8.38505427)

    assert result['t_D0']['Predators(v)'][0] == pytest.approx(5.)

    assert result['t_D0']['Predators(v)'][-1] == pytest.approx(7.1602100083)

    #Check if a output file is produced

    if short_reference_to_domain is True:

        sim.plotTimeSeries( x_data='Time(t)',
                            y_data=['Preys(u)','Predators(v)'],
                            save_file='test_plot.png',
                            data=sim.domain,
                            labels=['Preys($u$)','Predators($v$)'],
                            x_label=r'Time$\,(s)$',
                            y_label=r'Individuals$\,(\#)$',
                            show_plot=False,
                            grid=True,
                            legend=True
                        )

        assert os.path.isfile('test_plot.png')

    if short_reference_to_domain is False:

        sim.plotTimeSeries( x_data=[sim.domain[('t_D0','Time(t)')]],
                            y_data=sim.domain[('t_D0',['Preys(u)','Predators(v)'])],
                            save_file='test_plot.png',
                            labels=['Preys($u$)','Predators($v$)'],
                            x_label=r'Time$\,(s)$',
                            y_label=r'Individuals$\,(\#)$',
                            show_plot=False,
                            grid=True,
                            legend=True
                        )

        assert os.path.isfile('test_plot.png')
