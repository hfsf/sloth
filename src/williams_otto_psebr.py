from sloth.model import *
from sloth.problem import Problem
from sloth.simulation import Simulation
from sloth.optimization import Optimization, OptimizationProblem
from sloth.core.domain import Domain

class william_otto(Model):

    def __init__(self):

        super().__init__(name="william_otto", description="William Otto Problem")

        self.F_A = self.createParameter("F_A",dimless,"F_A")
        self.F_A.setValue(1.8)
        self.F_B = self.createVariable("F_B",dimless,"F_B")
        #self.F_B.setValue(2.)

        self.X_P = self.createVariable("X_P",dimless,"X_P")
        self.P_P = self.createParameter("P_P",dimless,"P_P")
        self.P_P.setValue(1143.38)
        self.X_E = self.createVariable("X_E",dimless,"X_E")
        self.P_E = self.createParameter("P_E",dimless,"P_E")
        self.P_E.setValue(25.92)
        self.X_A = self.createVariable("X_A",dimless,"X_A")
        self.C_A = self.createParameter("C_A",dimless,"C_A")
        self.C_A.setValue(76.23)
        self.X_B = self.createVariable("X_B",dimless,"X_B")
        self.C_B = self.createParameter("C_B",dimless,"C_B")
        self.C_B.setValue(114.34)

        self.T = self.createParameter("T",dimless,"T")
        self.T.setValue(95.)
        self.W = self.createParameter("W",dimless,"W")
        self.W.setValue(2104.7)

        self.PHI =self.createVariable("PHI",dimless,"PHI")

        a1=1.655e8
        a2=2.611e13
        b1=8077.6
        b2=12348.5

        self.a1 = self.createConstant("A1",dimless,"A1")
        self.a1.setValue(a1)
        self.a2 = self.createConstant("A2",dimless,"A2")
        self.a2.setValue(a2)
        self.b1 = self.createConstant("B1",dimless,"B1")
        self.b1.setValue(b1)
        self.b2 = self.createConstant("B2",dimless,"B2")
        self.b2.setValue(b2)

        self.k1_def = self.a1()*Exp(-1.*self.b1()/self.T())
        self.k2_def = self.a2()*Exp(-1.*self.b2()/self.T())
        self.k1 = self.k1_def#self.createVariable("k1",dimless,"k1")
        self.k2 = self.k2_def#self.createVariable("k2",dimless,"k2")


    def DeclareEquations(self):

        #self.k1eq = self.createEquation("k1_eq","",self.k1() - self.k1_def)

        #self.k2eq = self.createEquation("k2_eq","",self.k2() - self.k2_def)

        conserv_ = self.X_A() + self.X_B() + self.X_P() + self.X_E() - 1.

        self.conservation = self.createEquation("conservation", "conservation", conserv_)

        mass_A = self.F_A() - (self.F_A()+self.F_B())*self.X_A() - self.k1*self.X_A()*self.X_B()*self.W()

        self.mass_A = self.createEquation("mass_balance_A", "Mass balance for A", mass_A)

        mass_B = self.F_B() - (self.F_A()+self.F_B())*self.X_B() - 2*self.k1*self.X_A()*self.X_B()*self.W() - self.k2*self.X_A()*self.X_B()*self.W()

        self.mass_B = self.createEquation("mass_balance_B", "Mass balance for B", mass_B )

        mass_P = 2.*self.k1*self.X_A()*self.X_B()*self.W() - 2.*self.k2*self.X_B()*self.X_A()*self.W()-(self.F_A()+self.F_B())*self.X_P()

        self.mass_P = self.createEquation("mass_balance_P", "Mass balance for P", mass_P )

        mass_E = self.k2*self.X_A()*self.X_B()*self.X_P()*self.W() - (self.F_A()+self.F_B())*self.X_E()

        self.mass_E = self.createEquation("mass_balance_E", "Mass balance for E", mass_E )

        cost_return = (5554.1*(self.F_A()+self.F_B())*self.X_P() + 125.91*(self.F_A() + self.F_B())*self.X_E() - 370.3*self.F_A() - 555.42*self.F_B())

        self.cost = self.createEquation("cost_return", "Cost return", self.PHI() + cost_return)

def problem_WO():

    return Problem("problem_WO","William-Otto problem")

def simulation_WO():

    return Simulation("simulation_WO", "William-Otto simulation")

class wo_opt_problem(OptimizationProblem):

    def __init__(self, number_of_dimensions, mod):

        super().__init__(number_of_dimensions)

        self.mod = mod

    def DeclareObjectiveFunction(self, x):

        F_B = x[0]
        T = x[1]

        self.simulation_instance[self.mod.F_B].setValue(F_B)
        self.simulation_instance[self.mod.T].setValue(T)

        self.simulation_instance.problem.resolve()

        self.simulation_instance.setConfigurations(definition_dict=self.simulation_configuration)

        self.simulation_instance.runSimulation()

        result = self.simulation_instance.getResults('dict')

        print("\n\n RESULT: ",result)

        f = -1*result['PHI_'+self.mod.name]

        self.simulation_instance.reset()

        return[f]

    def DeclareSetBounds(self):

        return(tuple(self.bounds))

def wo_optimization():

    sim = simulation_WO()

    mod = william_otto()
    mod()

    prob = problem_WO()

    prob_opt = wo_opt_problem(4, mod)

    class opt_study(Optimization):

        def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints, optimization_configuration=None):

            super().__init__(simulation=sim, optimization_problem=optimization_problem, simulation_configuration=simulation_configuration,optimization_parameters=optimization_parameters, constraints=constraints, optimization_configuration=optimization_configuration)

    sim.setConfigurations(print_output=True, compile_equations=True)

    prob.addModels(mod)

    prob.resolve()

    sim.setProblem(prob)

    prob_opt()

    return opt_study(simulation=sim, optimization_problem=prob_opt, simulation_configuration=None, optimization_parameters=[mod.F_B, mod.T],
        constraints=([2.,343.15],[10.,373.15]))


def run_wo_simulation_study():

    sim = simulation_WO()

    mod = william_otto()

    mod()

    prob = problem_WO()

    prob.addModels(mod)

    prob.resolve()

    sim.setProblem(prob)

    sim.setConfigurations(is_dynamic=False, print_output=True, compile_equations=True)

    sim.runSimulation()

    sim.showResults()

def run_wo_opt_study():

    opt = wo_optimization()

    opt.optimization_problem()

    print("=>optimization ",opt.__dict__)

    #opt.optimization_problem.bounds = [[1.5624, 0., 0., 322.22],[2.0916, 7.0559, 100., 377.78]] #1.5624, 2.0916), (0, 7.0559), (0,100), (322.22, 377.78)]

    #print("=>optimization_problem bounds",opt.optimization_problem.get_bounds())

    opt.runOptimization()

    with open("test_log.backup", "w") as openfile:

        openfile.write("==>Results: {}".format(opt.getResults()))

    print("Sucessful run? ", opt.run_sucessful)

