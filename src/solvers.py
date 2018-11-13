# *coding:utf-8 *

"""
Define solver mechanisms
"""

import numpy as np
from scipy.linalg import solve as scp_solve
import sympy as sp

def createSolver(problem, is_dynamic=False, time_horizon=[None, None], LA_solver=None, NLA_solver=None, D_solver=None, DAE_solver=None):

    """
    Create a solver object given the considerations for the problem, and return the object.

    :param Problem problem:
        Problem in which the created solver will operate. Used to infer the system type formed by the equations in the Problem object.

    :param bool is_dynamic:
        Defines if the problem is dynamic(True) or steady(False). Defaults to steady problems.

    :param [float, float] time_horizon:
        Defines the initial and end time for the current dyanamic problem

    :param bool LA_solver:

    :param bool NLA_solver:

    :param bool D_solver:

    :param bool DAE_solver:

    :return:
        Solver object accordingly to the configurations provided and infered from the Problem.
    :rtype:
         Solver
    """

    is_linear = len(problem.equation_block._equation_groups['linear']) > 0

    is_nonlinear = len(problem.equation_block._equation_groups['nonlinear']) > 0

    is_differential = len(problem.equation_block._equation_groups['differential']) > 0

    # Check if the problem is D (strictly Differential), DAE (differential + linear or nonlinear), NLA (nonlinear) or LA (linear)

    is_D = is_differential==True and (is_linear==False and is_nonlinear==False)
    is_DAE = is_differential==True and (is_linear==True or is_nonlinear==True)
    is_NLA = is_differential==False and (is_nonlinear==True)
    is_LA = is_differential==False and (is_nonlinear==False and is_linear==True)

    if is_LA:

        return LASolver(problem, LA_solver)

    elif is_NLA:

        return NLASolver(problem, NLA_solver)

    elif is_D:

        pass

    elif is_DAE:

        pass

class Solver:

    """
    Defines generic Solver class
    """

    def __init__(self, problem, solver):

        """
        Instantiate Solver class

        :ivar Problem problem:
            Problem object on which the solver will operate

        :ivar str solver:
            Name of the solver mechanism that will operate in the problem
        """

        self.solver = solver

        self.problem = problem

        self.solver_mechanism = None


class LASolver(Solver):

    """
    Defines Linear Algebraic Solver class
    """

    def __init__(self, problem, solver=None):

        super().__init__(problem, solver)

        self.solver_mechanism = self.lookUpForSolver()

    def lookUpForSolver(self):

        """
        Define the solver mechanism used for solution of the problem, given the name of desired mechanism in the instantiation of current Solver object 
        """

        if self.solver==None or self.solver == 'simpySolve':

            return self._usingSimpySolve

        if self.solver=='scipySolve':

            return self._usingScipySolve

        if self.solver=='scipyLU':

            pass

    def _usingSimpySolve(self):

        x = sp.solve(self.problem.equation_block._equations_list, self.problem.equation_block._var_list)

        return list(x.values())

    def _usingScipySolve(self):

        A, b = self._getABfromEquations()

        x = scp_solve(A,b)

        return x.tolist()

    def _getABfromEquations(self):

        A, b = sp.linear_eq_to_matrix(self.problem.equation_block._equations_list, self.problem.equation_block._var_list)

        A, b = np.array(A, dtype=np.float64), np.array(b, dtype=np.float64)

        print("\n\nA=%s b=%s"%(A,b))

        return A,b

    def solve(self):

        X = self.solver_mechanism() 

        return X

class NLASolver(Solver):

    """
    Defines Non-Linear Algebraic Solver class
    """

    def __init__(self, problem, solver=None):

        super().__init__(problem, solver)

        self.solver_mechanism = self.lookUpForSolver()

    def lookUpForSolver(self):

        """
        Define the solver mechanism used for solution of the problem, given the name of desired mechanism in the instantiation of current Solver object 
        """

        if self.solver==None or self.solver == 'simpySolve':

            return self._usingSimpySolve

        if self.solver=='scipyLU':

            pass

    def _usingSimpySolve(self):

        x = sp.solve(self.problem.equation_block._equations_list, self.problem.equation_block._var_list)

        print("\n\n->%s"%x)

        return list(x.values())

    def solve(self):

        X = self.solver_mechanism() 

        return X