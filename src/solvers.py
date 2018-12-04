# *coding:utf-8 *

"""
Define solver mechanisms

* TODO: 
       - Complete differential algebraic solver 
"""

import numpy as np
from scipy.linalg import solve as scp_solve
import sympy as sp
import scipy.integrate as integrate
from collections import OrderedDict
from core.error_definitions import AbsentRequiredObjectError, UnexpectedValueError

import prettytable

def createSolver(problem, additional_configurations):

    """
    Create a solver object given the considerations for the problem, and return the object.

    :param Problem problem:
        Problem in which the created solver will operate. Used to infer the system type formed by the equations in the Problem object.

    :param dict additional_configurations:
        Dictionary containing additional configurations for the solver definition
    """

    domain = additional_configurations['domain']
    
    time_variable_name = additional_configurations['time_variable_name']

    linear_solver = additional_configurations['linear_solver']

    nonlinear_solver = additional_configurations['nonlinear_solver']

    differential_solver = additional_configurations['differential_solver']

    differential_algebraic_solver = additional_configurations['differential_algebraic_solver']

    problem_type = problem._getProblemType()

    if problem_type == "linear":

        return LASolver(problem, linear_solver)

    elif problem_type == "non-linear":

        return NLASolver(problem, nonlinear_solver)

    elif problem_type == "differential":

        return DSolver(problem, solver=differential_solver, additional_configurations=additional_configurations)

    elif problem_type == "differential-algebraic":

        pass

    else:

        raise UnexpectedValueError("EquationBlock")


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

    def __init__(self, problem, solver=None, additional_configurations={}):

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

    def solve(self, conf_args={}):

        X = self.solver_mechanism() 

        return X

class NLASolver(Solver):

    """
    Defines Non-Linear Algebraic Solver class
    """

    def __init__(self, problem, solver=None, additional_configurations={}):

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

    def solve(self, conf_args={}):

        X = self.solver_mechanism() 

        return X


class DSolver(Solver):

    """
    Defines Orinary Differential Solver class

    * TODO: Include terminate clause in integrate method by using terminate opitional argument provided for odespy solvers. The terminate should receive the data in odespy format (Y,t, args), thus, a convenience function should be provided to allow the user to express its conditional function using a dictionary approach (eg: vars['x'] > 0)
    """

    def __init__(self, problem, solver=None, additional_configurations={}):

        super().__init__(problem, solver)

        self.domain = additional_configurations['domain']

        time_variable_name = additional_configurations['time_variable_name']

        arg_names = additional_configurations['arg_names']

        if time_variable_name not in problem.initial_conditions:

            raise AbsentRequiredObjectError("initial condition for time variable (%s)"%time_variable_name)

        if time_variable_name not in arg_names:

            arg_names.append(time_variable_name)

        self.diffSystem = self.setUpDiffSystem()

        self.diffY = self.setUpDiffY()

        self.arg_names = arg_names

        # Differently from another solvers, solver_mechanism is not initialized because this is done in the solving time (integrate), where the user can set additional args and configuration args

        self.solver_mechanism =  None

        self.additional_configurations = additional_configurations

        self.compiled_diff_equations = None

        self.compilation_mechanism = additional_configurations['compilation_mechanism']

        if self.additional_configurations['compile_diff_equations']==True:

            self.compiled_diff_equations = self._compileDiffSystemIntoFunction()

    def lookUpForSolver(self):

        """
        Define the solver mechanism used for solution of the problem, given the name of desired mechanism in the instantiation of current Solver object 
        """

        if self.solver==None or self.solver == 'sympy':

            return self._sympySolveMechanism

        if self.solver=='scipy':

            return self._scipySolveMechanism


    def _compileDiffSystemIntoFunction(self):

        """
        Return the differential equations composing the differential system as an array of numpy functions

        :return compiled_diff_equations_:
            Array containing each of the differntial equations composing the differential system as numpy functions 
        :rtype function:
        """

        # Concatenate all the variable symbolic maps from the differential equations

        global_var_map = self.diffSystem[0].elementary_equation_expression[1].variable_map

        # Using underscore to ignore list comprehension output

        _ = [global_var_map.update(eq_i.elementary_equation_expression[1].variable_map) for eq_i in self.diffSystem]

        # Convert each equation to corresponding numpy func using global symbolic map, and store it in the compiled_diff_equations atribute

        compiled_diff_equations_ = [eq_i._convertToFunction(global_var_map, 'rhs', self.compilation_mechanism)
                                    for eq_i in self.diffSystem
                                   ]

        return compiled_diff_equations_

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

        mapped_dict = OrderedDict({var_i_name:var_i_val for (var_i_name, var_i_val) in zip(var_names,var_vals)})

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

    def solve(self, conf_args={}): 

    # args_={}, conf_args_={}, initial_time=0., end_time=None, number_of_time_steps = None):

        initial_time = conf_args['initial_time']

        end_time = conf_args['end_time']

        args = conf_args['args']

        number_of_time_steps = conf_args['number_of_time_steps']

        conf_args_ = conf_args['configuration_args']

        def diffYinterfaceForSolver(Y, t, args=()):

            Y_ = self._createMappingFromValues(self.diffY.keys(), Y)

            if len(args)>0:
                args_ = self._createMappingFromValues(self.args_names, args)
            else:
                args_ = {}

            if self.additional_configurations['compile_diff_equations'] == True:

                global_dict = Y_.copy()

                global_dict.update(args_)

                res = [f_i(*list(global_dict.values())) for f_i in self.compiled_diff_equations]

            else:

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

        if self.additional_configurations['print_output'] == True:

            tab = prettytable.PrettyTable()

            tab.field_names = self.additional_configurations['output_headers']

            for i in range(len(time_points)):

                tab.add_row(np.concatenate(([time_points[i]], Y[i,:])))

            print(tab)

        self.domain._register(to_register_)
