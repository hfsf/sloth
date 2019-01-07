from . import model
from . import problem
from . import simulation
from . import analysis
from . import solvers
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *
from . import optimization


class modelTest0(model.Model):

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

class modelTest1(model.Model):

    def __init__(self, name, description):

        super().__init__(name, description)

        self.u =  self.createVariable("u", dimless, "u")
        self.v =  self.createParameter("v", dimless, "v")

        # print("creating domain")

        #self.dom = Domain("domain",dimless,self.t,"generic domain")

        # print("distributing u")

        #self.u.distributeOnDomain(self.dom)

        # print("distributing v")

        #self.v.distributeOnDomain(self.dom)

        # print("\n~~~>Domain dependent objs=%s",self.dom.dependent_objs)

    def DeclareEquations(self):

        expr1 = self.u() - self.v()**2

        self.eq1 = self.createEquation("eq1", "Equation 1", expr1)

class simul(simulation.Simulation):

    def __init__(self, name, description):

        super().__init__(name, description)

class opt_prob(optimization.OptimizationProblem):

    def __init__(self,nb_dimension=1, name='', description=''):

        super().__init__(nb_dimension)

        self.name = name

        self.description = description

    def DeclareObjectiveFunction(self, x):

        #print("\nx(%s) is = %s"%(type(x),x))

        #=========== SHOULD AUTOMATE THIS ==============

        self.simulation_instance.problem.equation_block.parameter_dict[mod1.v.name].setValue(x[0])

        #print("\n\n     ===>%s"%self.simulation_instance.problem.equation_block.parameter_dict[mod1.v.name].__dict__)

        #Reload problem definitions (Equation symbolic objects etc)

        self.simulation_instance.problem.resolve() 

        #===============================================

        self.simulation_instance.setConfigurations(
                                    definition_dict=self.simulation_configuration,
                                    number_parameters_to_optimize=1
                        )

        self.simulation_instance.runSimulation()

        #print("\nParameter is {}. Results are: {}".format(x[0],self.simulation_instance.getResults('dict')))
        #print("Equations are: %s"%self.simulation_instance.problem.equation_block._equations_list)

        #f = sum([x[i]**2 for i in range(self.dimension)])

        f = float(self.simulation_instance.getResults('dict')['u_M1'])

        return (f,)


# mod1 = modelTest1("test_model1", "A model for testing purposes")

mod0 = modelTest0("M0", "A model for testing purposes")

mod1 = modelTest1("M1", "A model for testing purposes")

prob = problem.Problem("test_problem", "A problem for testing purposes")

sim = simul("test_simulation", "A simulation for testing purposes")

opt_prob = opt_prob(1,"opt_prob", "Sphere optimization problem")

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

    #mod0()

    mod1()

    #prob.addModels([mod0, mod1])
    #prob.addModels(mod0)
    prob.addModels(mod1)

    prob.resolve()

    analist = analysis.Analysis()
    print(analist.problemReport(prob))

    #prob.createConnection(mod0, mod1, mod0.a, mod1.c)

    #prob.equation_block._getMapForRewriteSystemAsResidual()

    '''
    prob.setInitialConditions({'y1_M0_d':0.,
                               'y2_M0_d':0.,
                               'y3_M0_d':0.,
                               'y4_M0_d':-9.82,
                               'y5_M0_d':0.,
                               'y5_M0':5.,
                               'y4_M0':0.,
                               'y3_M0':0.,
                               'y2_M0':0.,
                               'y1_M0':1.,
                               't_M0':0.     
                            }
                        )
    '''
    #print("\n===>%s"%mod1.dom.__dict__)

    sim.setProblem(prob)
    #sim.report(prob)

    sim.setConfigurations(is_dynamic=False,
                          print_output=True  
                    )
    
    sim.dumpConfigurations('sim_conf.json')

    sss=input("\n\n Press any key to continue ...")

    opt_prob()

    opt = optimization.Optimization(simulation=sim, 
                                    optimization_problem=opt_prob, 
                                    simulation_configuration='sim_conf.json',
                                    optimization_parameters=[mod1.v], 
                                    constraints=[-5.12,5.12],
                                    optimization_configuration=None
                        )

    opt.runOptimization() 

    '''
    sim.runSimulation(initial_time=0., 
                      end_time=5.,
                      is_dynamic=False,
                      #domain=mod0.dom,
                      #number_of_time_steps=1000,
                      #time_variable_name="t_M0",
                      compile_equations=True,
                      print_output=True,
                      #output_headers=["Time","y1","y2","y3","y4","y5"]#,
                      #variable_name_map={"t_M1":"Time(t)", 
                      #                   "u_M1":"Preys(u)", 
                      #                   "v_M1":"Predators(v)"
                      #                  } 
                      )
    '''

    #print("\n===>%s"%mod0.dom.values)

    """
    #sim.runSimulation()

    #sim.showResults()

    #res = sim.getResults('dict')

    #print("\n-> keys:%s     its type:%s"%(list(res.keys()),type(list(res.keys())[0])))

    #print("\n===>%s"%sim.getResults('dict'))
    """

    """
    sim.plotResults(x_data=[sim.domain[('t_M1','Time(t)')]], 
                    y_data=sim.domain[('t_M1',['Preys(u)','Predators(v)'])], 
                    save_file='test_plot.png', 
                    labels=['Preys($u$)','Predators($v$)'], 
                    x_label=r'Time$\,(s)$', 
                    y_label=r'Individuals$\,(\#)$',
                    grid=True,
                    legend=True
            )
    """

    # s = solvers.createSolver(prob, domain=mod0.dom, D_solver='scipy')

    # s.integrate(end_time=15., number_of_time_steps=100)

    # print(mod0.dom.values['t'])

    # maps = {'u':10.,'v':5.,'a':1.,'b':1.,'c':1.,'d':1.}# mod0.eq1.elementary_equation_expression[1].symbolic_map

    # f = mod0.eq1._convertToFunction(maps,'rhs')

    # print("\n=>%s"%f(10.,5.,1.,0.1,1.5,0.75))

    # print("=>%s"%mod0.eq1.elementary_equation_expression[1].symbolic_object)