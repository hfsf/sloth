#test_model.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.model import Model

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

def test_model_properties(mod):

    assert mod.name == "D0" and \
           mod.description == "Differential model" and \
           list(mod.variables.keys()) == ["u_D0","v_D0","t_D0"] and \
           list(mod.constants.keys()) == ["a_D0","b_D0","c_D0", "d_D0"] and \
           list(mod.equations.keys()) == ["eq1_D0","eq2_D0"]

def test_model_enodes(mod):

    assert mod.eq1.equation_expression.symbolic_map[list(mod.a().symbolic_map.keys())[0]] == mod.a and \
           mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.b and \
           mod.eq1.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]] == mod.eq2.equation_expression.symbolic_map[list(mod.b().symbolic_map.keys())[0]]
