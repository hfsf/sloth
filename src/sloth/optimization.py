# *coding:utf-8 *

"""
Define optimization mechanisms
"""
from .core.error_definitions import *
from .core.quantity import Quantity
import copy
import pygmo as pg
import json
import numpy as np
from time import time, strftime, gmtime
#import ipdb

class OptimizationProblem:

    """
    Definition of an optimization problem. Used by the class Optimization to perform the relevant optimization studies

    *Note:

        Mandatory structure that user should supply when importing OptimizationProblem:

        *DeclareObjectiveFunction

        *DeclareSetBounds (Not recommended)

        *DeclareFitnessComparison

    """

    def __init__(self, number_of_dimensions, name='', description='', bounds=None, is_maximization=False, simulation_instance=None):

        """
        Instantiate OptimizationProblem
        """

        self.name = name

        self.dim = number_of_dimensions

        self.description = description

        self.is_maximization = False

        self.bounds = None

        self.simulation_instance = simulation_instance

        self.simulation_configuration = None

        self._is_ready=False

    def fitness(self,x):

        pass

    def get_bounds(self):

        return self.bounds

    def get_name(self):

        return self.name

    def get_extra_info(self):

        return "\tDimensions: "+str(self.dim)

    def setBounds(self, bounds):

        self.bounds = bounds

    def _setSimulationInstance(self, simulation_instance):

        self.simulation_instance = simulation_instance

    def _setSimulationConfiguration(self, simulation_configuration):

        self.simulation_configuration = simulation_configuration

    def DeclareSetBounds(self):

        """
        Virtual function for overloading the bounds setting
        """

        if np.array(self.bounds).ndim==1:

            return tuple([np.array([i]) for i in self.bounds])

        else:

            return tuple([np.array(i) for i in self.bounds])


    def DeclareFitnessComparison(self, f1, f2):

        """
        Virtual function for overloading the fitness comparison
        """

        if self.is_maximization is True:

            return f1[0]>f2[0]

        else:

            return f1[0]<f2[0]

    def DeclareObjectiveFunction(self, x):

        """
        Virtual function for overloading the fitness evaluation
        """

        pass

    def __call__(self):

        #Reimplement virtual methods

        self.fitness = self.DeclareObjectiveFunction

        self.get_bounds = self.DeclareSetBounds

        self._is_ready = True


class Optimization:

    """
    Define optimization mechanisms. Given variables for an subspecified system, the optimizator will work on the variables or parameters subjected to study towards the minimization (or maximization) of an objective function.
    """

    def __init__(self, simulation, optimization_problem, optimization_parameters, simulation_configuration=None, constraints=None, is_maximization=False, optimizer='de', constraints_fun=None, constraints_additional_args=[], additional_args=[], objective_function=None,optimization_configuration={}):

        """
        Instantiate Optimization

        :ivar Simulation simulation:
            Simulation instance which will be used to perform optimizations

        :ivar OptimizationProblem optimization_problem:
            Optimization problem to be studied

        :ivar (dict, str) simulation_configuration:
            Configuration (either a dictionary or a JSON file name to be loaded) to run the simulations used in the optimization study. Defaults to None, from which the configurations defined for the simulation input will be loaded, raising an exception if it is not possible

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
        
        elif simulation_configuration is None and simulation.configurations is not None:

            self.simulation_configuration = simulation.configurations

        else:

            raise AbsentRequiredObjectError("(Dictionary, file path, simulation with defined configurations)")

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

        self.optimization_configuration = optimization_configuration

        if optimization_configuration is {}:

            self.optimization_configuration = {'number_of_individuals':50,
                                               'number_of_generations':1000,
                                               'crossover_rate':.95,
                                               'mutation_rate':.02,
                                               'elitism':1,
                                               'crossover_type':'exponential',
                                               'mutation_type':'gaussian',
                                               'selection_type':'tournament',
                                               'selection_param':4,
                                               'scale_factor':.8,
                                               'variant_de':2,
                                               'ftol_de':1e-10,
                                               'xtol_de':1e-10,
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

        self.best_parameters = None 

        self.best_fitness = None

        self.run_sucessful = False

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

                #=================================================================

                crossover_type = self.optimization_configuration['crossover_type']

                mutation_type = self.optimization_configuration['mutation_type']

                selection_type = self.optimization_configuration['selection_type']

                selection_param=self.optimization_configuration['selection_param']

                #=================================================================


                algo = pg.algorithm(pg.sga(gen = gen, cr = cr, m = mr, elitism = elitism, mutation=mutation_type, selection=selection_type, crossover=crossover_type, param_s=selection_param))

                #isl = pg.island(algo, self.optimization_problem, ind)

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

                algo = pg.algorithm(pg.de(gen=gen, F=f_w, CR = cr, variant=de_variant, ftol=de_ftol, xtol=de_xtol))

                #isl = pg.island(algo, self.optimization_problem, ind)

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

                algo = pg.algorithm(pg.pso_gen(gen=gen, omega=omega, eta1=eta1, eta2=eta2, max_vel=vcoeff,  variant=pso_variant))

                #isl = pg.island(algo, self.optimization_problem, ind)

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

    def getOptimizationInfo(self):

        """
        Return information about the optimization task to be performed
        """

        print("Starting optimization")
        print("\tOptimization problem: %s"%self.optimization_problem.name)
        param_names = [i if isinstance(i,str) else i.name for i in self.optimization_parameters]
        print("\tParameters to optimize: %s"%param_names)
        print("\tOptimization algorithm: %s"%self.optimization_mechanism.get_name())
        try:
            print("\tAlgorithm parameters: \n %s"%self.optimization_mechanism.get_extra_info().replace("\t","\t\t"))
        except:
            pass


    def runOptimization(self, print_output=False, report_frequency=0):

        if self._performSaneTests() == True:

            self.optimization_problem._setSimulationInstance(self.simulation)

            self.optimization_problem._setSimulationConfiguration(self.simulation_configuration)

            self.optimization_problem.setBounds(self.constraints)

            self.optimization_mechanism.set_verbosity(report_frequency)

            # Print information

            start_time = time()

            self.getOptimizationInfo()

            # Run optimization

            prob = pg.problem(self.optimization_problem)

            pop = pg.population(prob, size=self.optimization_configuration['number_of_individuals'])

            pop = self.optimization_mechanism.evolve(pop)

            self.best_parameters = pop.champion_x

            self.best_fitness = pop.champion_f

            end_time = time()

            elapsed_time = end_time - start_time

            print("\n\tOptimization ended. \n\t Elapsed time:{}".format(strftime("%H:%M:%S", gmtime(elapsed_time))))

            if print_output is True:
                print("Best individual: \n%s -> finess: %s"%(pop.champion_x, pop.champion_f))

            self.run_sucessful=True

        else:

            raise Exception("Ill-formed optimization configuration")

    def getResults(self):

        """
        Return the results obtained by the optimization
        
        :return (self.best_parameters, self.best_fitness):
            Tuple containing the best parameters obtained by the optimization algorithm (aka the decision vector) and the best fitness obtained
        :rtype tuple(numpy.array, numpy.array)
        """

        if self.best_fitness is None and self.best_parameters is None:

            raise Exception("Should run the optimization first to return its results")

        else:

            return (self.best_parameters, self.best_fitness)


