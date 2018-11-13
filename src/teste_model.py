import model
import problem
import analysis
import solvers
from core.equation_operators import *
from core.template_units import *

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

mod1 = modelTest1("test_model1", "A model for testing purposes")

analist = analysis.Analysis()

def xec():

    mod1()

    prob.addModels(mod1)

    prob.resolve()

    print(analist.problemReport(prob))
    
    s = solvers.createSolver(prob,LA_solver='simpySolve')

    rtrn = s.solve()
   
    print("=>: %s"%(rtrn))
