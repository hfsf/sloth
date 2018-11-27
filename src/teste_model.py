import model
import problem
import analysis
import solvers
from core.equation_operators import *
from core.template_units import *
from core.domain import *


class modelTest0(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.u =  self.createVariable("u", dimless, "Number of preys")
        self.v =  self.createVariable("v", dimless, "Number of predators")
        self.a =  self.createParameter("a", dimless, "Growth of rabbits")
        self.b =  self.createParameter("b", dimless, "Growth of rabbits")
        self.c =  self.createParameter("c", dimless, "Growth of rabbits")
        self.d =  self.createParameter("d", dimless, "Growth of rabbits")
        self.a.setValue(1.)
        self.b.setValue(0.1)
        self.c.setValue(1.5)
        self.d.setValue(0.75)

        self.t =  self.createVariable("t", dimless, "Time(s)")

        self.dom = Domain("Time domain", dimless, self.t)

        self.u.distributeOnDomain(self.dom)
        self.v.distributeOnDomain(self.dom)

    def DeclareEquations(self):

        expr1 = self.u.Diff(self.t) == self.a()*self.u() - self.b()*self.u()*self.v()
        expr2 = self.v.Diff(self.t) == self.d()*self.b()*self.u()*self.v() - self.c()*self.v()

        self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
        self.eq2 = self.createEquation("eq2", "Equation 2", expr2)


class modelTest1(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.P1 =  self.createParameter("P1", atm, "Pressure-1")
        self.V1 =  self.createParameter("V1", m**3, "Volume-1")
        self.T1 =  self.createParameter("T1", K, "Temperature-1")
        self.n1 =  self.createVariable("n1", mol, "Mol-1")
        self.P1.setValue(1)
        self.V1.setValue(0.2832)
        self.T1.setValue(294.26)        

        self.P2 =  self.createParameter("P2", atm, "Pressure-2")
        self.V2 =  self.createVariable("V2", m**3, "Volume-2")
        self.T2 =  self.createParameter("T2", K, "Temperature-2")
        self.n2 =  self.createVariable("n2", mol, "Mol-2")
        self.P2.setValue(2.5)
        self.T2.setValue(594.26)

        self.R =  self.createConstant("R", UniversalIdealGasConstant, "Universal Ideal Gas Constant")
        self.R.setValue(8.20574587e-5)

    def DeclareEquations(self):

        expr = self.P1()*self.V1() - self.n1()*self.R()*self.T1()

        self.eq1 = self.createEquation("eq1", "Equation 1", expr)

        expr = self.P2()*self.V2() - self.n2()*self.R()*self.T2()

        self.eq2 = self.createEquation("eq2", "Equation 2", expr)

        expr = self.n2()-self.n1()

        self.eq3 = self.createEquation("eq3", "Molar conservation", expr)

prob = problem.Problem("test_problem", "A problem for testing purposes")

# mod1 = modelTest1("test_model1", "A model for testing purposes")

mod0 = modelTest0("test_model0", "A model for testing purposes")

analist = analysis.Analysis()

def xec():

    """
    mod1()

    prob.addModels(mod1)

    prob.resolve()

    print(analist.problemReport(prob))
    
    s = solvers.createSolver(prob,LA_solver='simpySolve')

    rtrn = s.solve()
   
    print("=>: %s"%(rtrn))
    """

    mod0()

    prob.addModels(mod0)

    prob.resolve()

    print(analist.problemReport(prob))

    prob.setInitialConditions({'t':0.,'u':10.,'v':5.})
    
    s = solvers.createSolver(prob, domain=mod0.dom, D_solver='scipy')

    s.integrate(end_time=15., number_of_time_steps=100)

    print(mod0.dom.values['t'])