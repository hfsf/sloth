from sloth.model import *
from sloth.problem import Problem
from sloth.simulation import Simulation
from sloth.optimization import Optimization, OptimizationProblem
from sloth.core.domain import Domain

class ethanol_opt(Model):

    def __init__(self):

        super().__init__(name="E0", description="Ethanol optimization problem")

        self.t = self.createVariable("t", dimless, "t")
        self.dom = Domain("domain", dimless, self.t, "generic domain")

        self.x1 = self.createVariable("x1", dimless, "x1")
        self.x2 = self.createVariable("x2", dimless, "x2")
        self.x3 = self.createVariable("x3", dimless, "x3")
        self.x4 = self.createVariable("x4", dimless, "x4")

        self.x1.distributeOnDomain(self.dom)
        self.x2.distributeOnDomain(self.dom)
        self.x3.distributeOnDomain(self.dom)
        self.x4.distributeOnDomain(self.dom)

        self.mu0 = self.createParameter("mu0", dimless, "")
        self.mu0.setValue(0.8)
        self.q0 = self.createParameter("q0", dimless, "")
        self.q0.setValue(1)
        self.ks = self.createParameter("ks", dimless, "")
        self.ks.setValue(0.22)
        self.ksI = self.createParameter("ksI", dimless, "")
        self.ksI.setValue(0.44)
        self.kp = self.createParameter("kp", dimless, "")
        self.kp.setValue(16)
        self.kpI = self.createParameter("kpI", dimless, "")
        self.kpI.setValue(71.5)
        self.y = self.createParameter("y", dimless, "")
        self.y.setValue(0.1)
        self.x20 = self.createParameter("x20", dimless, "")
        self.x20.setValue(150)
        self.tf = self.createParameter("tf", dimless, "tf")
        self.tf.setValue(24.)

        self.a0 = self.createParameter("a0", dimless, "a0")
        self.a1 = self.createParameter("a1", dimless, "a1")
        self.w1 = self.createParameter("w1", dimless, "w1")

    def DeclareEquations(self):

        u = self.a0() + self.a1()*Exp(self.w1()+ self.tf()/self.tf())
        eqx1 = self.x1.Diff(self.t) == u
        self.eqx1 = self.createEquation("eq_x1", "", eqx1)

        mu = (self.mu0()/(1.+self.x4()/self.kp()))*(self.x3()/(self.ks()+self.x3()))
        q = (self.q0()/(1.+self.x4()/self.kpI()))*(self.x3()/(self.ksI()+self.x3()))

        eqx2 = self.x2.Diff(self.t) == mu*self.x2() - u*self.x2()/self.x1()
        self.eqx2 = self.createEquation("eq_x2", "", eqx2)

        eqx3 = self.x3.Diff(self.t) == -1*mu*self.x2()/self.y() + u*(self.x20()-self.x3())/self.x1()
        self.eqx3 = self.createEquation("eq_x3", "", eqx3)

        eqx4 = self.x4.Diff(self.t) == q*self.x4() - u*(self.x4()/self.x1())
        self.eqx4 = self.createEquation("eq_x4", "", eqx4)

class ethanol_max_prob(OptimizationProblem):

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

def run_simulation_study(a0, a1, w1):

    sim = simulation_pse()

    mod = ethanol_opt()
    mod.a0.setValue(a0)
    mod.a1.setValue(a1)
    mod.w1.setValue(w1)
    mod()

    prob = problem_pse()

    prob.addModels(mod)

    prob.setTimeVariableName(['t_E0'])

    prob.resolve()

    prob.setInitialConditions({'t_E0':0., 'x1_E0':10., 'x2_E0':1., 'x3_E0':150., 'x4_E0':1e-18})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0., end_time=24.,domain=mod.dom, is_dynamic=True, print_output=True, compile_equations=True, output_headers=["Time","Volume(x1)","Biomass(x2)","Substrate(x3)","Ethanol(x4)"], variable_name_map={"t_E0":"Time(t)", "x1_E0":"Volume(x1)", "x2_E0":"Biomass(x2)", "x3_E0":"Substrate(x3)","x4_E0":"Ethanol(x4)"})

    sim.runSimulation()

    sim.showResults()