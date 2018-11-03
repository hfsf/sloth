import model
import problem
import analysis
from core.template_units import *

class modelTest1(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.F1 =  self.createVariable("F1", kg/s, "Mass flux")
        self.F2 =  self.createVariable("F2", kg/s, "Mass flux")
        self.F3 =  self.createVariable("F3", kg/s, "Mass flux", is_exposed=True, type="output")
        self.k1 = self.createParameter("K1", kg/s, "Spec. parameter")
        self.k2 = self.createParameter("K2", kg/s, "Unespec. parameter")

        self.k1.setValue(10.)

    def DeclareEquations(self):

        expr = self.F1()-self.F3()+self.k1()

        self.eq = self.createEquation("eq1", "Mass continuity", expr)

class modelTest2(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.F4 =  self.createVariable("F4", kg/s, "Mass flux", is_exposed=True, type="input")
        self.F5 =  self.createVariable("F5", kg/s, "Mass flux")
        self.F6 =  self.createVariable("F6", kg/s, "Mass flux", is_exposed=True, type="output")

    def DeclareEquations(self):

        expr = self.F4()+self.F5()-self.F6()

        self.eq = self.createEquation("eq2", "Mass continuity", expr)


class modelTest3(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.F1 =  self.createVariable("F1", kg/s, "Mass flux")
        self.F2 =  self.createVariable("F2", kg/s, "Mass flux")
        self.F3 =  self.createVariable("F3", kg/s, "Mass flux", is_exposed=True, type="output")
        self.k1 = self.createParameter("K1", kg/s, "Spec. parameter")
        self.k2 = self.createParameter("K2", kg/s, "Unespec. parameter")

        self.k1.setValue(10.)

    def DeclareEquations(self):

        expr = self.F1()-self.F3()+self.k1()

        self.eq = self.createEquation("eq1", "Mass continuity", expr)

prob = problem.Problem("test_problem", "A problem for testint purposes")

mod1 = modelTest1("test_model1", "A model for testing purposes")
mod2 = modelTest2("test_model2", "A model for testing purposes")
mod3 = modelTest2("test_model3", "A model for testing purposes")

analist = analysis.Analysis()

def xec():

    mod1()
    mod2()
    mod3()

    print("Exposed from model#1: %s "%(mod1.exposed_vars))
    print("Variables from model#1: %s "%(mod1.variables))


    print("\nExposed from model#2: %s "%(mod2.exposed_vars))
    print("Variables from model#2: %s "%(mod2.variables))

    #mod1._infoDegreesOfFreedom_()
    #mod2._infoDegreesOfFreedom_()

    prob.addModels([mod1,mod2,mod3])
    prob.createConnection(mod1, mod2, mod1.F3, mod2.F4)

    print("\nProblem models: %s"%(prob.models))

    print("\nProblem connections: %s"%(prob.connections))

    print("\nPerforming model analysis: \n")

    print( analist.problemReport(prob) )
