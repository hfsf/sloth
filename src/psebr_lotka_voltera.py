from sloth.model import *
from sloth.problem import Problem
from sloth.simulation import Simulation
from sloth.optimization import Optimization, OptimizationProblem
from sloth.core.domain import Domain

class lotka_voltera(Model):

        def __init__(self, name, description):

            super().__init__(name, description)

            self.x =  self.createVariable("x", dimless, "Preys")
            self.y =  self.createVariable("y", dimless, "Predators")
            self.alfa1 =  self.createParameter("alfa1", dimless, "A1")
            self.beta1 =  self.createConstant("beta1", dimless, "B1")
            self.alfa2 =  self.createConstant("alfa2", dimless, "A2")
            self.beta2 =  self.createConstant("beta2", dimless, "B2")
            self.t = self.createVariable("t", dimless, "t")

            self.dom = Domain("domain",dimless,self.t,"generic domain")

            self.x.distributeOnDomain(self.dom)
            self.y.distributeOnDomain(self.dom)

            self.alfa1.setValue(1.)
            self.beta1.setValue(0.1)
            self.beta2.setValue(1.5)
            self.alfa2.setValue(0.75)

        def DeclareEquations(self):

            expr1 = self.x.Diff(self.t) == self.alfa1()*self.x() - self.beta1()*self.x()*self.y()

            expr2 = self.y.Diff(self.t) ==  self.alfa2()*self.beta1()*self.x()*self.y() -self.beta2()*self.y()

            self.eq1 = self.createEquation("eq1", "Equation 1", expr1)
            self.eq2 = self.createEquation("eq2", "Equation 2", expr2)

class lotka_prob(OptimizationProblem):

    def __init__(self, number_of_dimensions, mod):

        super().__init__(number_of_dimensions)

        self.mod = mod

    def DeclareObjectiveFunction(self, x):

        a0 = x[0]
        a1 = x[1]
        w1 = x[2]

        self.simulation_instance[self.mod.a0].setValue(a0)
        self.simulation_instance[self.mod.a1].setValue(a1)
        self.simulation_instance[self.mod.w1].setValue(w1)

        self.simulation_instance.problem.resolve()

        self.simulation_instance.setConfigurations(definition_dict=self.simulation_configuration)

        self.simulation_instance.runSimulation()

        result = self.simulation_instance.getResults('dict')

        f = result['t_E0']['Ethanol(x4)'][-1] * result['t_E0']['Volume(x1)'][-1]

        self.simulation_instance.reset()

        return[f]

    def DeclareSetBounds(self):

        return(tuple(self.bounds))

def problem_pse():

    return Problem("problem_PSE","Ethanol maximization problem")

def simulation_pse():

    return Simulation("problem_PSE","Ethanol maximization problem")

def ethanol_optimization():

    sim = simulation_pse()

    mod = ethanol_opt()
    mod()

    prob = problem_pse()

    prob_opt = ethanol_max_prob(3, mod)

    class opt_study(Optimization):

        def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints, optimization_configuration=None):

            super().__init__(simulation=sim, optimization_problem=optimization_problem, simulation_configuration=simulation_configuration,optimization_parameters=optimization_parameters, constraints=constraints, optimization_configuration=optimization_configuration)

    sim.setConfigurations(initial_time=0., end_time=24.,domain=mod.dom, time_variable_name='t_E0', is_dynamic=True, print_output=True, compile_equations=True, output_headers=["Time","Volume(x1)","Biomass(x2)","Substrate(x3)","Ethanol(x4)"], variable_name_map={"t_E0":"Time(t)", "x1_E0":"Volume(x1)", "x2_E0":"Biomass(x2)", "x3_E0":"Substrate(x3)","x4_E0":"Ethanol(x4)"})

    prob.addModels(mod)

    prob.resolve()

    prob.setInitialConditions({'t_E0':0., 'x1_E0':10., 'x2_E0':1., 'x3_E0':150., 'x4_E0':0.})

    sim.setProblem(prob)

    prob_opt()

    return opt_study(simulation=sim, optimization_problem=prob_opt, simulation_configuration=None, optimization_parameters=[mod.a0, mod.a1, mod.w1],
        constraints=([-5,-5,-5],[5,5,5]))


def run_optimization_study():

    sim = simulation_pse()

    mod = ethanol_opt()
    mod()

    prob = problem_pse()

    prob_opt = ethanol_max_prob(3, mod)

    class opt_study(Optimization):

        def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints, optimization_configuration=None):

            super().__init__(simulation=sim, optimization_problem=optimization_problem, simulation_configuration=simulation_configuration,optimization_parameters=optimization_parameters, constraints=constraints, optimization_configuration=optimization_configuration)

    sim.setConfigurations(initial_time=0., end_time=24.,domain=mod.dom, time_variable_name='t_E0', is_dynamic=True, print_output=True, compile_equations=True, output_headers=["Time","Volume(x1)","Biomass(x2)","Substrate(x3)","Ethanol(x4)"], variable_name_map={"t_E0":"Time(t)", "x1_E0":"Volume(x1)", "x2_E0":"Biomass(x2)", "x3_E0":"Substrate(x3)","x4_E0":"Ethanol(x4)"})

    prob.addModels(mod)

    prob.resolve()

    prob.setInitialConditions({'t_E0':0., 'x1_E0':10., 'x2_E0':1., 'x3_E0':150., 'x4_E0':1e-18})

    sim.setProblem(prob)

    prob_opt()

    opt = opt_study(simulation=sim, optimization_problem=prob_opt, simulation_configuration=None, optimization_parameters=[mod.a0, mod.a1, mod.w1],
        constraints=([-10.,-10.,-100.],[10.,10.,100.]))

    opt.optimization_problem()

    #opt.optimization_problem.bounds = ([-10.,-10.,-100.],[10.,10.,100.])

    opt.runOptimization()

    with open("test_log.backup", "w") as openfile:

        openfile.write("==>Results: {}".format(opt.getResults()))

    print("Sucessful run? ", opt.run_sucessful)

def run_simulation_study():

    sim = simulation_pse()

    mod = lotka_voltera("D0","")
    mod()

    prob = problem_pse()

    prob.addModels(mod)

    prob.resolve()

    prob.setInitialConditions({'t_D0':0.,'x_D0':10.,'y_D0':5.})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0.,
                      end_time=16.,
                      is_dynamic=True,
                      domain=mod.dom,
                      time_variable_name="t_D0",
                      print_output=False,
                      compile_equations=True,
                      output_headers=["Time","Preys(x)","Predators(y)"],
                      variable_name_map={"t_D0":"Time(t)",
                                         "x_D0":"Preys(x)",
                                         "y_D0":"Predators(y)"
                                }
                )

    sim.runSimulation()

    sim.plotTimeSeries(x_data=[sim.domain[('t_D0','Time(t)')]],
                    y_data=sim.domain[('t_D0',['Preys(x)','Predators(y)'])],
                    save_file='test_plot.png',
                    labels=['Preys($x$)','Predators($y$)'],
                    x_label=r'Time$\,(t)$',
                    y_label=r'Individuals$\,(\#)$',
                    grid=True,
                    legend=True
            )

    sim.showResults()