# *coding:utf-8 *

"""
Define optimization mechanisms
"""
from .core.error_definitions import *

class Optimization:

    """
    Define optimization mechanisms. Given variables for an subspecified system, the optimizator will work on the variables or parameters subjected to study towards the minimization (or maximization) of an objective function.
    """

    def __init__(self, problem, optimization_parameters, constraints=None, is_maximization=False, optimizer='ga', constraints_fun=None, constraints_additional_args=[], additional_args=[], objective_function=None):

        """
        Instantiate Optimization

        :ivar Problem problem:
            Problem to be studied

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
            Function to be optimized.  
        """

        self.problem = problem

        self.is_maximization = is_maximization

        self.optimizer = self._setOptimizer(optimizer)

        if constraints is not None:

            self.constraints_given = self._setGivenConstraints(constraints)

        self.constraints_fun = constraints_fun

        self.constraints_additional_args = constraints_additional_args

        self.additional_args = additional_args

    def _setGivenConstraints(self):

        pass

    def _getConstraintsOnTheFly(self):

        pass

    def _setOptimizer(self, optimizer):

        if callable(optimizer) == True:

            # User-defined optimizer function

            pass

        elif isinstance(optimizer, str):

            # Pre-defined optimizer

            pass

        else:

            raise UnexpectedValueError("(decorated function, str)")

    def setProblem(self, problem):

        self.problem = problem

