from sloth.model import *
from sloth.problem import Problem
from sloth.simulation import Simulation
from sloth.optimization import Optimization, OptimizationProblem
from sloth.core.domain import Domain
import numpy as np
import matplotlib.pyplot as plt


class ethanol_opt_1(Model):

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
        self.mu0.setValue(0.408)
        self.q0 = self.createParameter("q0", dimless, "")
        self.q0.setValue(1)
        self.ks = self.createParameter("ks", dimless, "")
        self.ks.setValue(0.22)
        self.ksI = self.createParameter("ksI", dimless, "")
        self.ksI.setValue(0.44)
        self.kp = self.createParameter("kp", dimless, "")
        self.kp.setValue(16.)
        self.kpI = self.createParameter("kpI", dimless, "")
        self.kpI.setValue(71.5)
        self.y = self.createParameter("y", dimless, "")
        self.y.setValue(0.1)
        self.x2_0 = self.createParameter("x2_0", dimless, "")
        self.x2_0.setValue(150.)

        self.tf = self.createParameter("tf", dimless, "tf")
        self.a = self.createParameter("a", dimless, "a")
        self.b = self.createParameter("b", dimless, "b")
        self.c = self.createParameter("c", dimless, "c")
        self.d = self.createParameter("d", dimless, "d")

    def DeclareEquations(self):

        #self.F = self.a0.value + self.a1.value + self.w1.value#self.a0() + self.a1()*Exp(self.w1()+ self.t()/self.tf())

        mu = (self.mu0()/(1.+self.x4()/self.kp()))*(self.x3()/(self.ks()+self.x3()))
        q = (self.q0()/(1.+self.x4()/self.kpI()))*(self.x3()/(self.ksI()+self.x3()))

        F_exp = self.a()*(self.t()/self.tf())**3. + self.b()*(self.t()/self.tf())**2. + self.c()*(self.t()/self.tf()) + self.d()

        #F_exp = self.a()*Cos(self.b()*(self.t()/self.tf()) + self.c()) + self.d()*Cos(self.e()*(self.t()/self.tf()) + self.f()) + self.g()

        u = Max(Min(F_exp, 12.),0.)

        #self.a0()*(self.t()/self.tf())**2 + self.a1()*(self.t()/self.tf()) + self.w1()

        eqx1 = self.x1.Diff(self.t) == u #+ 0.*(self.tf() + self.a0() + self.a1() + self.w1())
        self.eqx1 = self.createEquation("eq_x1", "", eqx1)

        eqx2 = self.x2.Diff(self.t) == mu*self.x2() - u*(self.x2()/self.x1())
        self.eqx2 = self.createEquation("eq_x2", "", eqx2)

        eqx3 = self.x3.Diff(self.t) == -1*mu*(self.x2()/self.y()) + u*(self.x2_0()-self.x3())/self.x1()
        self.eqx3 = self.createEquation("eq_x3", "", eqx3)

        eqx4 = self.x4.Diff(self.t) == q*self.x2() - u*(self.x4()/self.x1())
        self.eqx4 = self.createEquation("eq_x4", "", eqx4)


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
        self.mu0.setValue(0.408)
        self.q0 = self.createParameter("q0", dimless, "")
        self.q0.setValue(1)
        self.ks = self.createParameter("ks", dimless, "")
        self.ks.setValue(0.22)
        self.ksI = self.createParameter("ksI", dimless, "")
        self.ksI.setValue(0.44)
        self.kp = self.createParameter("kp", dimless, "")
        self.kp.setValue(16.)
        self.kpI = self.createParameter("kpI", dimless, "")
        self.kpI.setValue(71.5)
        self.y = self.createParameter("y", dimless, "")
        self.y.setValue(0.1)
        self.x2_0 = self.createParameter("x2_0", dimless, "")
        self.x2_0.setValue(150.)

        self.tf = self.createParameter("tf", dimless, "tf")
        self.a = self.createParameter("a", dimless, "a")
        self.b = self.createParameter("b", dimless, "b")
        self.c = self.createParameter("c", dimless, "c")
        self.d = self.createParameter("d", dimless, "d")
        self.e = self.createParameter("e", dimless, "e")
        self.f = self.createParameter("f", dimless, "f")
        self.g = self.createParameter("g", dimless, "g")

    def DeclareEquations(self):

        #self.F = self.a0.value + self.a1.value + self.w1.value#self.a0() + self.a1()*Exp(self.w1()+ self.t()/self.tf())

        mu = (self.mu0()/(1.+self.x4()/self.kp()))*(self.x3()/(self.ks()+self.x3()))
        q = (self.q0()/(1.+self.x4()/self.kpI()))*(self.x3()/(self.ksI()+self.x3()))

        #F_exp = self.a()*(self.t()/self.tf())**3. + self.b()*(self.t()/self.tf())**2. + self.c()*(self.t()/self.tf()) + self.d()

        F_exp = self.a()*Cos(self.b()*(self.t()/self.tf()) + self.c()) + self.d()#*Cos(self.e()*(self.t()/self.tf()) + self.f()) + self.g()

        u = Max(Min(F_exp, 12.),0.)

        #self.a0()*(self.t()/self.tf())**2 + self.a1()*(self.t()/self.tf()) + self.w1()

        eqx1 = self.x1.Diff(self.t) == u #+ 0.*(self.tf() + self.a0() + self.a1() + self.w1())
        self.eqx1 = self.createEquation("eq_x1", "", eqx1)

        eqx2 = self.x2.Diff(self.t) == mu*self.x2() - u*(self.x2()/self.x1())
        self.eqx2 = self.createEquation("eq_x2", "", eqx2)

        eqx3 = self.x3.Diff(self.t) == -1*mu*(self.x2()/self.y()) + u*(self.x2_0()-self.x3())/self.x1()
        self.eqx3 = self.createEquation("eq_x3", "", eqx3)

        eqx4 = self.x4.Diff(self.t) == q*self.x2() - u*(self.x4()/self.x1())
        self.eqx4 = self.createEquation("eq_x4", "", eqx4)

class ethanol_max_prob(OptimizationProblem):

    def __init__(self, number_of_dimensions, mod):

        super().__init__(number_of_dimensions)

        self.mod = mod

    def DeclareObjectiveFunction(self, x):


        a = x[0]
        b = x[1]
        c = x[2]
        d = x[3]
        #e = x[4]
        #f = x[5]
        #g = x[6]
        tf = x[4]

        self.simulation_instance[self.mod.a].setValue(a)
        self.simulation_instance[self.mod.b].setValue(b)
        self.simulation_instance[self.mod.c].setValue(c)
        self.simulation_instance[self.mod.d].setValue(d)
        #self.simulation_instance[self.mod.e].setValue(e)
        #self.simulation_instance[self.mod.f].setValue(f)
        #self.simulation_instance[self.mod.g].setValue(g)
        self.simulation_instance[self.mod.tf].setValue(tf)

        '''
        if self.simulation_instance[self.mod.F] < 0. :

            self.mod.F = 0.

        if self.simulation_instance[self.mod.F] > 12.:

            self.mod.F = 12.
        '''

        self.simulation_instance.problem.setTimeVariableName(['t_E0'])

        self.simulation_instance.problem.resolve()

        self.simulation_configuration['end_time'] = tf

        self.simulation_instance.setConfigurations(definition_dict=self.simulation_configuration)

        self.simulation_instance.runSimulation()

        result = self.simulation_instance.getResults('dict')

        print("\n\n==>Ethanol = ",result['t_E0']['Ethanol(x4)'][-1])
        print("\n\n==>Volume = ",result['t_E0']['Volume(x1)'][-1])
        print("\n\n==>Time = ",result['t_E0']['Time(t)'][-1])

        f = -1*(result['t_E0']['Ethanol(x4)'][-1]*result['t_E0']['Volume(x1)'][-1])/result['t_E0']['Time(t)'][-1]

        self.simulation_instance.reset()

        if result['t_E0']['Volume(x1)'][-1] <= 11. :

            f = 1e100

        if f > 0. or result['t_E0']['Ethanol(x4)'][-1] < 0. :

            f = 1e100

        if result['t_E0']['Volume(x1)'][-1] < 0. :

            f = 1e100

        if any(V_i >= 200.  for V_i in result['t_E0']['Volume(x1)'][:]):

            f = 1e100

        print("\n\n==>OBJ = ",f)

        print("\n\n==>x = ", x)

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

    prob_opt = ethanol_max_prob(8, mod)

    class opt_study(Optimization):

        def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints, optimization_configuration=None):

            super().__init__(simulation=sim, optimization_problem=optimization_problem, simulation_configuration=simulation_configuration,optimization_parameters=optimization_parameters, constraints=constraints, optimization_configuration=optimization_configuration)

    sim.setConfigurations(initial_time=0., end_time=mod.tf.value,domain=mod.dom, time_variable_name='t_E0', is_dynamic=True, print_output=True, compile_equations=True, output_headers=["Time","Volume(x1)","Biomass(x2)","Substrate(x3)","Ethanol(x4)"], variable_name_map={"t_E0":"Time(t)", "x1_E0":"Volume(x1)", "x2_E0":"Biomass(x2)", "x3_E0":"Substrate(x3)","x4_E0":"Ethanol(x4)"})

    prob.addModels(mod)

    prob.resolve()

    prob.setInitialConditions({'t_E0':0., 'x1_E0':10., 'x2_E0':1., 'x3_E0':150., 'x4_E0':0.})

    sim.setProblem(prob)

    prob_opt()


    opt = opt_study(simulation=sim, optimization_problem=prob_opt, simulation_configuration=None,  optimization_parameters=[mod.a, mod.b, mod.c, mod.d, mod.tf], constraints=([-100,-100,-100,-100,4.],[100.,100.,100.,100,96.]))

    opt.optimization_configuration['number_of_generations'] = 10
    opt.optimization_configuration['number_of_individuals'] = 10

    return opt


def run_optimization_study(compile_equations=False):

    sim = simulation_pse()

    mod = ethanol_opt()
    mod()

    prob = problem_pse()

    prob_opt = ethanol_max_prob(8, mod)

    class opt_study(Optimization):

        def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints, optimization_configuration=None):

            super().__init__(simulation=sim, optimization_problem=optimization_problem, simulation_configuration=simulation_configuration,optimization_parameters=optimization_parameters, constraints=constraints, optimization_configuration=optimization_configuration)

    sim.setConfigurations(initial_time=0., end_time=mod.tf.value,domain=mod.dom, time_variable_name='t_E0', is_dynamic=True, print_output=True, compile_equations=compile_equations, output_headers=["Time","Volume(x1)","Biomass(x2)","Substrate(x3)","Ethanol(x4)"], variable_name_map={"t_E0":"Time(t)", "x1_E0":"Volume(x1)", "x2_E0":"Biomass(x2)", "x3_E0":"Substrate(x3)","x4_E0":"Ethanol(x4)"}, differential_solver='ODEINT')

    prob.addModels(mod)

    prob.setTimeVariableName(['t_E0'])

    prob.resolve()

    prob.setInitialConditions({'t_E0':0., 'x1_E0':10., 'x2_E0':1., 'x3_E0':150., 'x4_E0':0.})

    sim.setProblem(prob)

    prob_opt()

    opt = opt_study(simulation=sim, optimization_problem=prob_opt, simulation_configuration=None, optimization_parameters=[mod.a, mod.b, mod.c, mod.d,mod.tf], constraints=([-100,-100,-100,-100,4.],[100.,100.,100.,100,96.]))

    opt.optimization_problem()

    #opt.optimization_problem.bounds = ([-10.,-10.,-100.],[10.,10.,100.])

    opt.runOptimization()

    with open("test_log.backup", "w") as openfile:

        openfile.write("==>Results: {}".format(opt.getResults()))

    print("Sucessful run? ", opt.run_sucessful)

    print("\n\n--->RESULT: ",opt.getResults())

def run_simulation_study(a, b, c, d, tf, compile_equations=False, with_plots=False, param=1, draw_F=False):

    sim = simulation_pse()

    if param==1:
        mod = ethanol_opt_1()
    else:
        mod = ethanol_opt()

    #mod = ethanol_opt_1()
    mod.a.setValue(a)
    mod.b.setValue(b)
    mod.c.setValue(c)
    mod.d.setValue(d)
    mod.tf.setValue(tf)
    mod()

    prob = problem_pse()

    prob.addModels(mod)

    prob.setTimeVariableName(['t_E0'])

    prob.resolve()

    prob.setInitialConditions({'t_E0':0., 'x1_E0':10., 'x2_E0':1., 'x3_E0':150., 'x4_E0':0.})

    sim.setProblem(prob)

    sim.setConfigurations(initial_time=0., end_time=tf, domain=mod.dom, is_dynamic=True, print_output=True, compile_equations=compile_equations, output_headers=["Time","Volume(x1)","Biomass(x2)","Substrate(x3)","Ethanol(x4)"], variable_name_map={"t_E0":"Time(t)", "x1_E0":"Volume(x1)", "x2_E0":"Biomass(x2)", "x3_E0":"Substrate(x3)","x4_E0":"Ethanol(x4)"}, differential_solver='ODEINT')

    sim.runSimulation()

    sim.showResults()

    print("\n\n\n RESULTS:\n")

    print("\n\n",sim.getResults()[-1][-1])

    if with_plots is True:

        e = 0.
        f = 0.
        g = 0.
        Tf=tf

        def calc_F1(t):

            t = np.array(t)

            return a*(t/Tf)**3 + b*(t/Tf)**2 + c*(t/Tf) + d

        def calc_F2(t):

            t = np.array(t)

            return a*np.cos(b*(t/Tf)+c) + d#*np.cos(e*(t/Tf)+f)+g

        results = sim.getResults('dict')

        time = results['t_E0']['Time(t)']
        X = results['t_E0']['Biomass(x2)']
        S = results['t_E0']['Substrate(x3)']
        P = results['t_E0']['Ethanol(x4)']

        if draw_F == False:

            plt.plot(time, X, ls='-', label=r'Biomassa $(x_2)$')
            plt.plot(time, S, ls='--', label=r'Substrato $(x_3)$')
            plt.plot(time, P, ls='-.', label=r'Bioetanol $(x_4)$')
            plt.xlabel(r'Tempo $(h)$', fontsize=14)
            plt.ylabel(r'Concentração $(g\,L^{-1})$', fontsize=14)
            plt.grid()
            plt.legend()
            plt.savefig('plot_concentrations.png', bbox_inches='tight')

            plt.clf()

        if draw_F == True:

            time = np.linspace(0., Tf, 1000)

            print("Tf = ",Tf)

            print("Time = ",time)

            if param == 1:

                F = calc_F1(time)

            else:

                F = calc_F2(time)

            F[F<0.] = 0.
            F[F>12.] = 12.

            print ("F = ",F)

            plt.step(time, F, where='mid',label=r'$u(t)$')
            plt.xlabel(r'Tempo $(h)$', fontsize=14)
            plt.ylabel(r'Vazão de alimentação $(L\,h^{-1})$')
            plt.grid()
            plt.legend()
            plt.savefig('plot_feed_1.png', bbox_inches='tight')




