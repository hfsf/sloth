# *coding:utf-8 *

"""
Define solver mechanisms
"""

import numpy as np
from scipy.linalg import solve as scp_solve
import sympy as sp
import scipy.integrate as integrate
from collections import OrderedDict
from core.error_definitions import AbsentRequiredObjectError

import prettytable

def createSolver(problem, domain=None, is_dynamic=False, time_horizon=[None, None], LA_solver=None, NLA_solver=None, D_solver=None, DAE_solver=None, time_variable_name='t', args_names=[], initial_time = 0., end_time = None):

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

        return DSolver(problem, domain, time_variable_name=time_variable_name, solver=D_solver)

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

        if self.solver==None or self.solver == 'sympySolve':

            return self._usingSympySolve

        if self.solver=='scipySolve':

            return self._usingScipySolve

        if self.solver=='scipyLU':

            pass

    def _usingSympySolve(self):

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

        if self.solver==None or self.solver == 'sympySolve':

            return self._usingSympySolve

        if self.solver=='scipyLU':

            pass

    def _usingSympySolve(self):

        x = sp.solve(self.problem.equation_block._equations_list, self.problem.equation_block._var_list)

        print("\n\n->%s"%x)

        return list(x.values())

    def solve(self):

        X = self.solver_mechanism() 

        return X


class DSolver(Solver):

    """
    Defines Orinary Differential Solver class

    * TODO: Include terminate clause in integrate method by using terminate opitional argument provided for odespy solvers. The terminate should receive the data in odespy format (Y,t, args), thus, a convenience function should be provided to allow the user to express its conditional function using a dictionary approach (eg: vars['x'] > 0)
    """

    def __init__(self, problem, domain, time_variable_name='t', solver=None, arg_names=[]):

        super().__init__(problem, solver)

        self.domain = domain

        if time_variable_name not in problem.initial_conditions:

            raise AbsentRequiredObjectError("initial condition for time variable (%s)"%time_variable_name)

        if time_variable_name not in arg_names:

            arg_names.append(time_variable_name)

        self.diffSystem = self.setUpDiffSystem()

        self.diffY = self.setUpDiffY()

        self.arg_names = arg_names

        # Differently from another solvers, solver_mechanism is not initialized because this is done in the solving time (integrate), where the user can set additional args and configuration args

        self.solver_mechanism =  None

    def lookUpForSolver(self):

        """
        Define the solver mechanism used for solution of the problem, given the name of desired mechanism in the instantiation of current Solver object 
        """

        if self.solver==None or self.solver == 'sympy':

            return self._sympySolveMechanism

        if self.solver=='scipy':

            return self._scipySolveMechanism


    def _createMappingFromValues(self, var_names, var_vals):

        """
        Create a mapping of Variable objects names and its values, returning a map dictionary for later evaluation

        :param list(str) var_names:
            Names to the variables to the map dictionary

        :param list(float) var_vals:
            Values to create the map dictionary

        :return mapped_dict:
            Mapping dicitonary containing the name of the symbolic objects as keys, and the corresponding values
        :rtype dict:
        """

        mapped_dict = {var_i_name:var_i_val for (var_i_name, var_i_val) in zip(var_names,var_vals)}

        return mapped_dict

    def _evaluateDiffYfromEquations(self, y_dict, args_dict):

        """
        Evaluate differential vector from the differential system defined symbolically, given the input values for the variables.

        :param dict y_dict:
            Dictionary containing the values of the variables used in the differential system of equations
        :param dict args_dict:
            Dictionary containing additional args passed to the solver, defined in the dictionary form likewise the for the variables.

        :return res:
            Values evaluated for the differential equations forming the differential system
        :rtype list:
        """

        y_map_ = {**y_dict, **args_dict}

        res = [eq_i.eval(y_map_, side='rhs') for eq_i in self.diffSystem]

        return res

    def _scipySolveMechanism(self):

        return integrate.odeint

    def _sympySolveMechanism(self):

        pass

    def _getArgsValuesByNames(self):

        """
        Given the name of the arguments, return a dictionary containing their names and values, retrieved from the Problem for the current Solver
        """

        pass

    def _getDiffYinOrder(self):

        y_name = []

        for eq_i in self.diffSystem:

            """
            print("type=%s"%(type(eq_i.elementary_equation_expression[0])))
            print("type2=%s"%(type(eq_i.elementary_equation_expression[0].symbolic_object)))            
            print("type3=%s"%(type(eq_i.elementary_equation_expression[0].symbolic_object.args)))
            print("\neq=%s\nexpression=%s\n expression[0]=%s, args=%s and %s" % 
                (eq_i,
                 eq_i.elementary_equation_expression,
                 eq_i.elementary_equation_expression[0],
                 eq_i.elementary_equation_expression[0].args, 
                 eq_i.elementary_equation_expression[1].args)
                )
            """
            y_name.append(str(eq_i.elementary_equation_expression[0].symbolic_object.args[0]))

        return y_name

    def setUpDiffSystem(self):

        """
        Set up the differential equation system

        :return:
            List of differential equations
        :rtype list(Equation):
        """

        return self.problem.equation_block._equation_groups['differential']

    def setUpDiffY(self):

        """
        Set up the differential variables

        :return:
            Dict of variables used in the differential equations
        :rtype list(Variables):
        """

        # ========== NEEDS TO BE OPTIMIZED ==========
        # diff_eqs_ = self.setUpDiffSystem()

        Y_= OrderedDict({})

        for eq_i in self.diffSystem:

            s_map_dict = eq_i.elementary_equation_expression[0].symbolic_map 

            Y_.update(s_map_dict)

        #============================================

        return Y_

    def integrate(self, args_={}, conf_args_={}, initial_time=0., end_time=None, number_of_time_steps = None):


        def diffYinterfaceForSolver(Y, t, args=()):

            Y_ = self._createMappingFromValues(self.diffY.keys(), Y)

            if len(args)>0:
                args_ = self._createMappingFromValues(self.args_names, args)
            else:
                args_ = {}

            res = self._evaluateDiffYfromEquations(Y_, args_)

            return res

        initial_conditions = self.problem.initial_conditions

        #Set solver, determine initial conditions, and execute solver to solve for the defined interval, store results in the domain, returning map for resultant variables

        self.solver_mechanism = self.lookUpForSolver()

        solver = self.solver_mechanism()

        # Retrive initial conditions in the right order

        Y_names = self._getDiffYinOrder()

        Y_0 = [initial_conditions[var_i] for var_i in Y_names]

        if number_of_time_steps == None and self.end_time!= None:

            number_of_time_steps = int(2*(end_time - initial_time))

        time_points = np.linspace(initial_time, end_time, number_of_time_steps+1)

        Y = solver( diffYinterfaceForSolver,
                    Y_0,
                    time_points, 
                    **conf_args_
                   )

        # print("\ntime_points.T shape=%s\nY.T shape=%s"%(time_points.reshape(1,-1).T.shape,Y.T.shape))

        to_register_ = np.hstack((time_points.reshape(1,-1).T, Y))

        tab = prettytable.PrettyTable()

        tab.field_names=["Time(t)","Preys(u)","Predators(v)"]

        for i in range(len(time_points)):

            tab.add_row([time_points[i],Y[i,0],Y[i,1]])

        print(tab)

        self.domain._register(to_register_)
