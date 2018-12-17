from . import model
from . import problem
from . import simulation
from . import analysis
from . import solvers
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *


class modelTest0(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.a =  self.createVariable("a", kg_s, "A", is_exposed=True, type='output')
        self.b =  self.createVariable("b", kg_s, "B")
        self.c =  self.createVariable("c", kg, "C")
        self.d =  self.createConstant("d", s**-1, "D")
        self.d.setValue(0.7)

    def DeclareEquations(self):

        expr1 = self.a() + self.b() - 100.

        expr2 = self.c()*self.d() + self.a() - 4

        expr3 = (self.c()*self.d())**2 - self.a()*self.b()

        self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
        self.eq2 = self.createEquation("eq2", "Equation 2", expr2)
        self.eq3 = self.createEquation("eq3", "Equation 3", expr3)

class modelTest1(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.u =  self.createVariable("u", dimless, "u")
        self.v =  self.createVariable("v", dimless, "v")
        self.a =  self.createConstant("a", dimless, "A")
        self.b =  self.createConstant("b", dimless, "B")
        self.c =  self.createConstant("c", dimless, "C")
        self.d =  self.createConstant("d", dimless, "D")
        self.t = self.createVariable("t", dimless, "t")

        # print("creating domain")

        self.dom = Domain("domain",dimless,self.t,"generic domain")

        # print("distributing u")

        self.u.distributeOnDomain(self.dom)

        # print("distributing v")

        self.v.distributeOnDomain(self.dom)

        # print("\n~~~>Domain dependent objs=%s",self.dom.dependent_objs)

        self.a.setValue(1.)
        self.b.setValue(0.1)
        self.c.setValue(1.5)
        self.d.setValue(0.75)

    def DeclareEquations(self):

        expr1 = self.u.Diff(self.t) == self.a()*self.u() - self.b()*self.u()*self.v()

        expr2 = self.v.Diff(self.t) ==  self.d()*self.b()*self.u()*self.v() -self.c()*self.v()

        self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
        self.eq2 = self.createEquation("eq2", "Equation 2", expr2)

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
    #prob.addModels(mod1)

    #prob.createConnection(mod0, mod1, mod0.a, mod1.c)

    prob.resolve()

    #prob.setInitialConditions({'t_M1':0.,'u_M1':10.,'v_M1':5.})

    #print("\n===>%s"%mod1.dom.__dict__)

    sim.setProblem(prob)
    #sim.report(prob)
    '''
    sim.runSimulation(initial_time=0., 
                      end_time=16.,
                      is_dynamic=True,
                      domain=mod1.dom,
                      time_variable_name="t_M1",
                      compile_diff_equations=True,
                      print_output=False,
                      output_headers=["Time","Preys(u)","Predators(v)"],
                      variable_name_map={"t_M1":"Time", 
                                         "u_M1":"Preys (u)", 
                                         "v_M1":"Predators (v)"
                                        } 
                      )
    '''

    sim.runSimulation()

    sim.showResults()

    res = sim.getResults('dict')

    print("\n-> keys:%s     its type:%s"%(list(res.keys()),type(list(res.keys())[0])))

    print("\n===>%s"%sim.getResults('dict'))

    # s = solvers.createSolver(prob, domain=mod0.dom, D_solver='scipy')

    # s.integrate(end_time=15., number_of_time_steps=100)

    # print(mod0.dom.values['t'])

    # maps = {'u':10.,'v':5.,'a':1.,'b':1.,'c':1.,'d':1.}# mod0.eq1.elementary_equation_expression[1].symbolic_map

    # f = mod0.eq1._convertToFunction(maps,'rhs')

    # print("\n=>%s"%f(10.,5.,1.,0.1,1.5,0.75))

    # print("=>%s"%mod0.eq1.elementary_equation_expression[1].symbolic_object)