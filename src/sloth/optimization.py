# *coding:utf-8 *

"""
Define optimization mechanisms
"""
from .core.error_definitions import *
from .core.quantity import Quantity
import copy
import PyGMO as pygmo
from PyGMO.problem import base as pygmo_base
import json

class OptimizationProblem(pygmo_base):

    """
    Definition of an optimization problem. Used by the class Optimization to perform the relevant optimization studies

    *Note:

        Mandatory structure that user should supply when importing OptimizationProblem:

        *DeclareObjectiveFunction

        *DeclareFitnessComparison

    """

    def __init__(self, number_of_dimensions, name='', description='', bounds=None, is_maximization=False, simulation_instance=None):

        """
        Instantiate OptimizationProblem
        """

        super(OptimizationProblem, self).__init__(number_of_dimensions)

        self.name = name

        self.description = description

        self.is_maximization = False

        if isinstance(bounds, list):
            self.setBounds(*bounds)
        elif isinstance(bounds, tuple):
            self.setBounds(bounds)

        self.simulation_instance = simulation_instance

        self.simulation_configuration = None

        self._is_ready=False

    def _setSimulationInstance(self, simulation_instance):

        self.simulation_instance = simulation_instance

    def _setSimulationConfiguration(self, simulation_configuration):

        self.simulation_configuration = simulation_configuration

    def setBounds(self, x_0, x_f):

        self.set_bounds(x_0, x_f)

    def DeclareFitnessComparison(self, f1, f2):

        """
        Virtual function for overloading the fitness comparison
        """

        if self.is_maximization is True:

            return f1[0]>f2[0]

        else:

            return f1[0]<f2[0]

    def DeclareObjectiveFunction(self, x):

        pass

    def __call__(self):

        #Reimplement virtual methods

        self._objfun_impl = self.DeclareObjectiveFunction

        self._comparefitness_impl = self.DeclareFitnessComparison

        self._is_ready = True


class Optimization:

    """
    Define optimization mechanisms. Given variables for an subspecified system, the optimizator will work on the variables or parameters subjected to study towards the minimization (or maximization) of an objective function.
    """

    def __init__(self, simulation, optimization_problem, simulation_configuration, optimization_parameters, constraints=None, is_maximization=False, optimizer='de', constraints_fun=None, constraints_additional_args=[], additional_args=[], objective_function=None,optimization_configuration=None):

        """
        Instantiate Optimization

        :ivar Simulation simulation:
            Simulation instance which will be used to perform optimizations

        :ivar OptimizationProblem optimization_problem:
            Optimization problem to be studied

        :ivar (dict, str) simulation_configuration:
            Configuration (either a dictionary or a JSON file name to be loaded) to run the simulations used in the optimization study

        :ivar list(Quantity or str) optimization_parameters:
            List of parameters to be optimized for the supplied problem. Can be supplied either the names of the Quantity objects or direct reference to them. 

        :ivar dict constraints:
            Dictionary containing the constraints for each one of the studied variables/parameters. If None is provided, look for the constraints in the quantity object definition (only for variables). Defaults to None

        :ivar bool is_maximization:
            Determine if the objective function need to be maximized, or if it is a minimization work. Defaults to False (thus, minimization).
        
        :ivar [decorated function, str] optimizer:
            The optimization routine to be employed. The user can either provide an decorated function, or a string with the name of the default optimizers

        :ivar function constraints_fun:
            Function for determination of the constraints on-the-fly given the simulation output variables, which signature is [(DataFrame) output_variables, constraints_additional_args=None]

        :ivar list constraints_additional_args:
            Additional args to be passed to the function that determines constraints on-the-fly. Defaults to []  

        :ivar list additional_args:
            Additional args to be passed to the optimizer. Defaults to []

        :ivar [decorated function] objective_function:
            Function to be optimized, which signature is [(DataFrame) output_variables, (function) constraints]  and should return one value as output

        :ivar dict optimization_configuration:
            Dictionary containing the information needed to run the optimization mechanism.
        """

        self.optimization_problem = optimization_problem

        self.simulation = simulation

        self.simulation_configuration = None

        if isinstance(simulation_configuration, dict):

            self.simulation_configuration = simulation_configuration

        elif isinstance(simulation_configuration, str):

            with open(simulation_configuration, "r") as read_file:

                self.simulation_configuration = json.load(read_file)
        else:

            raise AbsentRequiredObjectError("(Dictionary, file path)")

        self.optimization_parameters = optimization_parameters

        self.constraints = None

        if constraints is not None:

            self.setConstraints(constraints)

        self.is_maximization = is_maximization

        self.constraints_fun = constraints_fun

        self.constraints_additional_args = constraints_additional_args

        self.additional_args = additional_args

        self.objective_function = objective_function

        self.original_optimization_parameters_state = copy.deepcopy(self.optimization_parameters)

        self.optimization_mechanism = None

        self.optimization_configuration = None

        print("Optimization configuration is: %s"%optimization_configuration)
        print("Constraints is: %s"%self.constraints)

        if optimization_configuration is None:

            self.optimization_configuration = {'number_of_individuals':50,
                                               'number_of_generations':1000,
                                               'crossover_rate':.95,
                                               'mutation_rate':.02,
                                               'elitism':1,
                                               'crossover_type':'exponential',
                                               'mutation_type':'gaussian',
                                               'selection_type':'roulette',
                                               'scale_factor':.8,
                                               'variant_de':2,
                                               'ftol_de':1e-6,
                                               'xtol_de':1e-6,
                                               'omega_pso':0.7298,
                                               'eta1_pso':2.05,
                                               'eta2_pso':2.05,
                                               'variant_pso':5,
                                               'max_v_pso':0.5,
                                               'neighborhood_type_pso':2,
                                               'neighborhood_param_pso':4, 
                                    }

        elif isinstance(optimization_configuration, str):

            with open(optimization_configuration, "r") as read_file:

                self.optimization_configuration = json.load(read_file)

        elif isinstance(optimization_configuration, dict):

            self.optimization_configuration = optimization_configuration

        else:

            raise AbsentRequiredObjectError("(Dictionary, file path)")

        self.optimizer = self._setOptimizer(optimizer)


    def saveConfigurations(self, file_name):

        with open(file_name, "w") as write_file:

            json.dump(self.optimization_configuration, write_file)

    def setConstraints(self, constraints):

        self.constraints = constraints

    def _getFixedConstraints(self):

        return self.constraints

    def setOptimizationProblem(self, optimization_problem):

        """
        Set the optimization problem for the current optimization study
        """

        self.optimization_problem = optimization_problem

    def _getConstraintsOnTheFly(self):

        return self.constraints_fun()

    def _setOptimizer(self, optimizer):

        if callable(optimizer) == True:

            # User-defined optimizer function

            pass

        elif isinstance(optimizer, str):

            # Pre-defined optimizer

            if optimizer == 'ga':

                gen = self.optimization_configuration['number_of_generations']

                cr = self.optimization_configuration['crossover_rate']

                mr = self.optimization_configuration['mutation_rate']

                elitism = self.optimization_configuration['elitism']

                ind = self.optimization_configuration['number_of_individuals']

                #==================================================================

                crossover_type = self.optimization_configuration['crossover_type']

                if crossover_type is 'binomial' or crossover_type is 'Binomial':

                    crossover_type = pygmo.algorithm._algorithm._sga_crossover_type.BINOMIAL

                if crossover_type is 'exponential' or crossover_type is 'Exponential':

                    crossover_type = pygmo.algorithm._algorithm._sga_crossover_type.EXPONENTIAL

                #==================================================================

                mutation_type = self.optimization_configuration['mutation_type']

                if mutation_type is 'gaussian' or mutation_type is 'Gaussian':

                    mutation_type = pygmo.algorithm._algorithm._sga_mutation_type.GAUSSIAN

                if mutation_type is 'random' or mutation_type is 'Random':

                    mutation_type = pygmo.algorithm._algorithm._sga_mutation_type.RANDOM

                #==================================================================


                selection_type = self.optimization_configuration['selection_type']

                if selection_type is 'roulette' or selection_type is 'Roulette':

                    selection_type = pygmo.algorithm._algorithm._sga_selection_type.ROULETTE

                if selection_type is 'best20' or selection_type is 'Best20':

                    selection_type = pygmo.algorithm._algorithm._sga_selection_type.BEST20

                #==================================================================


                algo = pygmo.algorithm.sga(gen = gen, cr = cr, m = mr, elitism = elitism, mutation=mutation_type, selection=selection_type, crossover=crossover_type)

                #isl = pygmo.island(algo, self.optimization_problem, ind)

                self.optimization_mechanism = algo

            if optimizer == 'de':

                gen = self.optimization_configuration['number_of_generations']

                cr = self.optimization_configuration['crossover_rate']

                f_w = self.optimization_configuration['scale_factor']

                de_variant = self.optimization_configuration['variant_de']

                de_ftol = self.optimization_configuration['ftol_de']

                de_xtol = self.optimization_configuration['xtol_de']

                ind = self.optimization_configuration['number_of_individuals']

                #==================================================================

                algo = pygmo.algorithm.de(gen=gen, f=f_w, cr = cr, variant=de_variant, ftol=de_ftol, xtol=de_xtol)

                #isl = pygmo.island(algo, self.optimization_problem, ind)

                self.optimization_mechanism = algo

            if optimizer == 'pso':


                gen = self.optimization_configuration['number_of_generations']

                omega = self.optimization_configuration['omega_pso']

                eta1 = self.optimization_configuration['eta1_pso']

                eta2 = self.optimization_configuration['eta2_pso']

                vcoeff = self.optimization_configuration['max_v_pso']

                pso_variant = self.optimization_configuration['variant_pso']

                neighb_type = self.optimization_configuration['neighborhood_type_pso']

                neighb_param = self.optimization_configuration['neighborhood_param_pso']                

                ind = self.optimization_configuration['number_of_individuals']

                #==================================================================

                algo = pygmo.algorithm.pso_gen(gen=gen, omega=omega, eta1=eta1, eta2=eta2,vcoeff=vcoeff,  variant=pso_variant, ftol=de_ftol, xtol=de_xtol)

                #isl = pygmo.island(algo, self.optimization_problem, ind)

                self.optimization_mechanism = algo

        else:

            raise UnexpectedValueError("(decorated function, str)")

    def setProblem(self, problem):

        self.problem = problem

    def _performSaneTests(self):

        """
        Perform sanity tests preemptory to the execution of the optimization
        
        :return:
            Result indicating if the system is well formed (True) or not (False)
        :rtype bool:
        """

        if self.constraints is not None and isinstance(self.constraints,dict):

            if isinstance(self.optimization_parameters[0], Quantity):

                if not all(op_i.name in self.constraints for op_i in self.optimization_parameters):

                    raise AbsentRequiredObjectError("Constraints")

            if isinstance(self.optimization_parameters[0], str):

                if not all(op_i in self.constraints for op_i in self.optimization_parameters):

                    raise AbsentRequiredObjectError("Constraints")

        if self.optimization_configuration is None:

                    raise AbsentRequiredObjectError("(Simulation with pre-defined configurations)")

        if self.optimization_problem._is_ready is not True:

            raise AbsentRequiredObjectError("(Resolved OptimizationProblem object)")

        return True

    def _setParameters(self, new_parameters):

        if isinstance(self.optimization_parameters[0], Quantity):

            pass

        elif isinstance(self.optimization_parameters[0], str):

            pass

        else:

            raise AbsentRequiredObjectError("(New values to parameters)")

    def runOptimization(self):

        if self._performSaneTests() == True:

            '''
            def _optimizationWorkflow(parameters, args=None):

                self._setParameters(parameters)

                self.simulation.runSimulation(definition_dict=self.simulation.configurations)

                simulation_output = self.simulation.output

                obj_func_result = self.objective_function(simulation_output,
                                                          args
                                                )

                return obj_func_result

            opt_params, opt_obj_func = \
                self.optimization_mechanism(workflow=_optimizationWorkflow,                   constraints = self._getFixedConstraints()
                                )
            '''

            # Run optimization

            self.optimization_problem._setSimulationInstance(self.simulation)

            self.optimization_problem._setSimulationConfiguration(self.simulation_configuration)

            self.optimization_problem.setBounds(*self.constraints)

            print("\n\n==>Optimization problem:")
            print(self.optimization_problem)

            print("\n\n==>Optimization algorithm:")
            print(self.optimization_mechanism)

            pop = pygmo.population(self.optimization_problem,self.optimization_configuration['number_of_individuals'])

            pop = self.optimization_mechanism.evolve(pop)

            print("Best individual: \n%s"%pop.champion)

        else:

            raise Exception("Ill-formed optimization configuration")