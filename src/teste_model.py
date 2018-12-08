import model
import problem
import simulation
import analysis
import solvers
from core.equation_operators import *
from core.template_units import *
from core.domain import *


class modelTest0(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.a =  self.createVariable("a", kg_s, "A", is_exposed=True, type='output')
        self.b =  self.createVariable("b", kg_s, "B")
        self.c =  self.createVariable("c", kg_s, "C")
        self.d =  self.createVariable("d", kg_s, "D")

    def DeclareEquations(self):

        expr1 = self.a()*0.001 + self.b() - 1.

        expr2 = self.a() + self.b() - 2

        #expr3 = self.b() - self.a() - Log(3.5)

        self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
        self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
        #self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

class modelTest1(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.a =  self.createVariable("a1", dimless, "A1")
        self.b =  self.createVariable("b1", dimless, "B1")
        self.c =  self.createVariable("c1", dimless, "C1", is_exposed=True, type='input')
    def DeclareEquations(self):

        expr1 = self.a() + self.b() + 5.

        expr2 = self.a() - self.c() - 1.5

        self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
        self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
        #self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

class simul(simulation.Simulation):

    def __init__(self, name, description):

        super().__init__(name, description)


# mod1 = modelTest1("test_model1", "A model for testing purposes")

mod0 = modelTest0("M0", "A model for testing purposes")

mod1 = modelTest1("M1", "A model for testing purposes")

prob = problem.Problem("test_problem", "A problem for testing purposes")

sim = simul("test_simulation", "A simulation for testing purposes")

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

    #mod1()

    #prob.addModels([mod0, mod1])
    prob.addModels(mod0)

    #prob.createConnection(mod0, mod1, mod0.a, mod1.c)

    prob.resolve()

    # prob.setInitialConditions({'t':0.,'u':10.,'v':5.})

    sim.setProblem(prob)

    sim.report(prob)

    sim.runSimulation(initial_time=0., 
                      end_time=16.,
                      #is_dynamic=True,
                      #domain=mod0.dom,
                      print_output=True,
                      output_headers=["Time","Preys(u)","Predators(v)"] 
                      )
    sim.showResults()

    # s = solvers.createSolver(prob, domain=mod0.dom, D_solver='scipy')

    # s.integrate(end_time=15., number_of_time_steps=100)

    # print(mod0.dom.values['t'])

    # maps = {'u':10.,'v':5.,'a':1.,'b':1.,'c':1.,'d':1.}# mod0.eq1.elementary_equation_expression[1].symbolic_map

    # f = mod0.eq1._convertToFunction(maps,'rhs')

    # print("\n=>%s"%f(10.,5.,1.,0.1,1.5,0.75))

    # print("=>%s"%mod0.eq1.elementary_equation_expression[1].symbolic_object)