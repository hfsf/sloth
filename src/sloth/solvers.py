# *coding:utf-8 *

"""
Define solver mechanisms
"""

import numpy as np
from scipy.linalg import solve as scp_solve
import sympy as sp
from assimulo.solvers import IDA
from assimulo.problem import Implicit_Problem
import pylab as P
import scipy.integrate as integrate
from assimulo.problem import Explicit_Problem
from assimulo.solvers import CVode
from collections import OrderedDict
from .core.error_definitions import AbsentRequiredObjectError, UnexpectedValueError, NumericalError
from .core.equation_operators import *
import prettytable

from pyneqsys.symbolic import SymbolicSys


def _createSolver(problem, additional_configurations):

    """
    Create a solver object given the considerations for the problem, and return the object.

    :param Problem problem:
        Problem in which the created solver will operate. Used to infer the system type formed by the equations in the Problem object.

    :param dict additional_configurations:
        Dictionary containing additional configurations for the solver definition
    """
    try:
        domain = additional_configurations['domain']
    except:
        domain = None

    try:
        time_variable_name = additional_configurations['time_variable_name']
    except:
        time_variable_name = None

    linear_solver = additional_configurations['linear_solver']

    nonlinear_solver = additional_configurations['nonlinear_solver']

    differential_solver = additional_configurations['differential_solver']

    differential_algebraic_solver = additional_configurations['differential_algebraic_solver']

    problem_type = problem._getProblemType()

    if problem_type == "linear":

        return LASolver(problem, linear_solver, additional_configurations=additional_configurations)

    elif problem_type == "nonlinear":

        return NLASolver(problem, nonlinear_solver, additional_configurations=additional_configurations)

    elif problem_type == "differential":

        return DSolver(problem, solver=differential_solver, additional_configurations=additional_configurations)

    elif problem_type == "differential-algebraic":

        return DaeSolver(problem, solver=differential_algebraic_solver, additional_configurations=additional_configurations)

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

    def _printSolvingInfo(self):

        """
        Print information about current equation sytem etc
        :return:
        """

        pass


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

        if self.solver==None or self.solver == 'sympy':

            return self._sympySolveMechanism

        if self.solver=='scipy':

            return self._scipySolveMechanism

        if self.solver=='scipy_LU':

            pass

    def _sympySolveMechanism(self):

        X = sp.solve(self.problem.equation_block._equations_list, dict=True)

        return X[0]

    def _scipySolveMechanism(self):

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

        self.expected_solver_names = ['*']

        self.solver_mechanism = self.lookUpForSolver()

    def lookUpForSolver(self):

        """
        Define the solver mechanism used for solution of the problem, given the name of desired mechanism in the instantiation of current Solver object
        Uses the mechanism provided by the pyneqsys package
        """

        if self.solver==None or self.solver == '*':

            return self._defaultSolveMechanism

        else:

            raise AbsentRequiredObjectError("element from {}" % self.expected_solver_names, self.solver)


    def _defaultSolveMechanism(self):

        var_names = [i for i in self.problem.equation_block._var_list]

        equations_list = self.problem.equation_block._equations_list

        # TODO: Improve initial guess determination and/or employ a more robust solver

        guess = [1.e-2]*len(var_names)

        eqSys = SymbolicSys(var_names, equations_list)

        x_out, sol_state = eqSys.solve(guess, solver='scipy', tol=1e-6)

        print(sol_state)

        if sol_state['success'] is True:

            x_out_dict = {var_i: val_i for var_i, val_i in zip(var_names,x_out)}

            return x_out_dict

        else:

            raise NumericalError()

    def solve(self, verbose=True):

        if verbose is True:

            self._printSolvingInfo()

        X = self.solver_mechanism()

        return X


class DSolver(Solver):

    """
    Defines Ordinary Differential Solver class

    * TODO: Include terminate clause in integrate method by using terminate optional argument provided for odespy solvers. The terminate should receive the data in odespy format (Y,t, args), thus, a convenience function should be provided to allow the user to express its conditional function using a dictionary approach (eg: vars['x'] > 0)
    """

    def __init__(self, problem, solver=None, additional_configurations={}):

        super().__init__(problem, solver)

        self.domain = additional_configurations['domain']

        self.times_for_solution = additional_configurations['times_for_solution']

        time_variable_name = additional_configurations['time_variable_name']

        arg_names = additional_configurations['arg_names'] 

        if isinstance(time_variable_name, list):

            has_initial_time_condition_declared = all(t_i in problem.initial_conditions for t_i in time_variable_name)

        else:

            has_initial_time_condition_declared = time_variable_name in problem.initial_conditions

        if has_initial_time_condition_declared is not True:

            raise AbsentRequiredObjectError("initial condition for time variable (%s)"%time_variable_name)

        if time_variable_name not in arg_names:

            arg_names.append(time_variable_name)

        self.diffSystem = self.setUpDiffSystem()

        self.diffY = self.setUpDiffY()

        self.arg_names = arg_names

        # Differently from another solvers, solver_mechanism is not initialized because this is done in the solving time (Simulation.runSimulation), where the user can set additional args and configuration args

        self.solver_mechanism = solver #None

        self.additional_configurations = additional_configurations

        self.compiled_equations = None

        self.compilation_mechanism = additional_configurations['compilation_mechanism']

        if self.additional_configurations['compile_equations']==True:

            self.compiled_equations = self._compileDiffSystemIntoFunction()

    def lookUpForSolver(self):

        """
        Define the solver mechanism used for solution of the problem, given the name of desired mechanism in the instantiation of current Solver object
        """

        if self.solver == None or self.solver == 'ODEINT':

            return integrate.odeint

        if self.solver == 'RADAU':

            return integrate.Radau

        if self.solver == 'CVODE':

            return self._assimuloSolveMechanism

    def _compileDiffSystemIntoFunction(self):

        """
        Return the differential equations composing the differential system as an array of numpy functions

        :return compiled_diff_equations_:
            Array containing each of the differntial equations composing the differential system as numpy functions
        :rtype function:
        """

        # Concatenate all the variable symbolic maps from the differential equations

        '''
        global_var_map = self.diffSystem[0].elementary_equation_expression[1].variable_map

        # Using underscore to ignore list comprehension output

        _ = [global_var_map.update(eq_i.elementary_equation_expression[1].variable_map) for eq_i in self.diffSystem]

        # Convert each equation to corresponding numpy func using global symbolic map, and store it in the compiled_diff_equations atribute

        compiled_diff_equations_ = [eq_i._convertToFunction(global_var_map, 'rhs', self.compilation_mechanism)
                                    for eq_i in self.diffSystem
                                   ]

        return compiled_diff_equations_
        '''

        return self.problem.equation_block._getEquationBlockAsFunction('elementary','rhs', self.compilation_mechanism)

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

    def _assimuloSolveMechanism(self):

        return

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

        times_for_solution = conf_args['times_for_solution']

        conf_args_ = conf_args['configuration_args']

        def diffYinterfaceForScipySolvers(Y, t, args=()):

            Y_ = self._createMappingFromValues(self.diffY.keys(), Y)

            for t_i in self.problem.time_variable_name:

                has_t_i_var_declared_in_diff_eq = self.problem.equation_block._hasVarBeenDeclared(t_i, "differential")

                #print("\n------>t_i = ",t_i)

                #print("\n------> has? ", has_t_i_var_declared_in_diff_eq)

                if has_t_i_var_declared_in_diff_eq is True:

                    Y_.update({t_i:t})

            if len(args)>0:
                args_ = self._createMappingFromValues(self.args_names, args)
            else:
                args_ = {}

            if self.additional_configurations['compile_equations'] == True:

                global_dict = Y_.copy()

                global_dict.update(args_)

                #====== Reorder global_dict from _var_list from equation_block ========

                keys_ = self.problem.equation_block._var_list
                keys_.extend([i for i in list(global_dict.keys()) if i not in keys_])

                global_dict = {k:global_dict[k] for k in keys_}

                #======================================================================

                #print("\n\n\n\t--------->var_list:",self.problem.equation_block._var_list)
                #print("\n\n\n\t--------->global_dict:",global_dict)
                #print("\n\n\n\t--------->list(global_dict.values()):",list(global_dict.values()))

                #res = [f_i(*list(global_dict.values())) for f_i in self.compiled_equations]

                res = self.compiled_equations(*list(global_dict.values()))

                #print("\n\n\n\t--------->res(compiled):",res)
                #print("\n\n\n\t--------->res(NOT compiled):",self._evaluateDiffYfromEquations(Y_, args_))

                #sss=input("...")

            else:

                res = self._evaluateDiffYfromEquations(Y_, args_)

            return res

        def diffYinterfaceForAssimuloSolvers(t, Y, args=()):

            Y_ = self._createMappingFromValues(self.diffY.keys(), Y)

            for t_i in self.problem.time_variable_name:

                has_t_i_var_declared_in_diff_eq = self.problem.equation_block._hasVarBeenDeclared(t_i, "differential")

                #print("\n------>t_i = ",t_i)

                #print("\n------> has? ", has_t_i_var_declared_in_diff_eq)

                if has_t_i_var_declared_in_diff_eq is True:

                    Y_.update({t_i:t})

            if len(args)>0:
                args_ = self._createMappingFromValues(self.args_names, args)
            else:
                args_ = {}

            if self.additional_configurations['compile_equations'] == True:

                global_dict = Y_.copy()

                global_dict.update(args_)

                #====== Reorder global_dict from _var_list from equation_block ========

                keys_ = self.problem.equation_block._var_list
                keys_.extend([i for i in list(global_dict.keys()) if i not in keys_])

                global_dict = {k:global_dict[k] for k in keys_}

                #======================================================================

                #res = [f_i(*list(global_dict.values())) for f_i in self.compiled_equations]

                res = self.compiled_equations(*list(global_dict.values()))

            else:

                res = self._evaluateDiffYfromEquations(Y_, args_)

            return res

        initial_conditions = self.problem.initial_conditions

        #Set solver, determine initial conditions, and execute solver to solve for the defined interval, store results in the domain, returning map for resultant variables

        self.solver_mechanism = self.lookUpForSolver()

        solver = self.solver_mechanism

        # Retrive initial conditions in the right order

        Y_names = self._getDiffYinOrder()

        Y_0 = [initial_conditions[var_i] for var_i in Y_names]

        if number_of_time_steps == None and self.end_time!= None:

            number_of_time_steps = 100#int(1000*(end_time - initial_time))

        if self.times_for_solution is None:

            time_points = np.linspace(initial_time, end_time, number_of_time_steps+1)

        else:

            time_points = times_for_solution

        #print("\n\n\n\t\t---------->", self.solver)

        if self.solver == None or self.solver == 'ODEINT':

            Y = solver( diffYinterfaceForScipySolvers,
                        Y_0,
                        time_points,
                        **conf_args_
                       )

        if self.solver == 'CVODE':

            exp_mod = Explicit_Problem(diffYinterfaceForAssimuloSolvers,
                                        Y_0,
                                        name='CVODE')
            exp_sim = CVode(exp_mod)
            exp_sim.discr='BDF'
            exp_sim.iter='Newton'
            exp_sim.maxord=5
            exp_sim.atol=1e-10
            exp_sim.rtol=1e-10

            time_points, Y = exp_sim.simulate(end_time, ncp_list=time_points)

            time_points = np.array(time_points)
            Y = np.array(Y)

        # print("\ntime_points.T shape=%s\nY.T shape=%s"%(time_points.reshape(1,-1).T.shape,Y.T.shape))

        to_register_ = None

        if self.solver == None or self.solver == 'ODEINT':

            # print("Y.shape=",Y.shape," time_points.shape=",time_points.shape)
            # print("RESULT: \n",Y)

            to_register_ = np.hstack((time_points.reshape(-1,1), Y))

        if self.solver == 'CVODE':

            # print("Y = ",Y)
            # print("time_points = ",time_points)

            #print("Y.shape=",Y.shape," time_points.shape=",time_points.shape)
            #print("RESULT: \n",Y)

            to_register_ = np.hstack((time_points.reshape(-1,1), Y))

        if self.additional_configurations['print_output'] == True:

            tab = prettytable.PrettyTable()

            tab.field_names = self.additional_configurations['output_headers']

            for i in range(len(time_points)):

                tab.add_row(np.concatenate(([time_points[i]], Y[i,:])))

            print(tab)

        #print("\n\n\n--->TO_REGISTER_ = ",to_register_, "\n\n ---> SOLVER = ",self.solver)

        self.domain._register(to_register_)

        # ============ Rename domain columns =============

        variable_name_map = self.additional_configurations['variable_name_map']

        if variable_name_map is not {}:

            self.domain._renameHeaders(variable_name_map)

        # ================================================

        return time_points,Y


class DaeSolver(Solver):

    """
    Defines Algebraic Differential Solver class
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

        self.differential_Eqs, self.algebraic_Eqs = self._setUpDaeSystem()

        self.arg_names = arg_names

        self.additional_configurations = additional_configurations

        #======================================================================

        self.compiled_equations = None

        self.compilation_mechanism = additional_configurations['compilation_mechanism']

        self.compiled_equations = self._compileEquationsIntoFunctions()

        #======================================================================

    def _compileEquationsIntoFunctions(self):

        """
        Return the equations composing the differential algebraic system as an array of numpy functions

        :return:
            Function that will return the result for each of the equations in form of an array
        :rtype function:
        """

        return self.problem.equation_block._getEquationBlockAsFunction('residual','rhs', self.compilation_mechanism)

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

    def _setUpDaeSystem(self):

        """
        Set up the DAE system

        :return:
            Tuple containing a list of differential equations, and a list of algebraic (linear and nonlinear) equations
        :rtype tuple(list(Equation),list(Equation)):
        """

        diff_eqs = self.problem.equation_block._equation_groups['differential']

        lin_eqs = self.problem.equation_block._equation_groups['linear']

        nlin_eqs = self.problem.equation_block._equation_groups['nonlinear']

        return diff_eqs, lin_eqs.append(nlin_eqs)

    def solve(self, conf_args={}):

        initial_time = conf_args['initial_time']

        end_time = conf_args['end_time']

        args = conf_args['args']

        number_of_time_steps = conf_args['number_of_time_steps']

        conf_args_ = conf_args['configuration_args']

        initial_conditions = self.problem.initial_conditions

        if number_of_time_steps == None and self.end_time!= None:

            number_of_time_steps = int(2*(end_time - initial_time))

        time_points = np.linspace(initial_time, end_time, number_of_time_steps+1).tolist()

        ydmap,ymap = self.problem.equation_block._getMapForRewriteSystemAsResidual()

        y_0 = [initial_conditions[var_i] for var_i in ymap.keys()]

        #Adopted nomenclature for search for initial conditions defined in the Problem object for differential expressions is original_name+'_d' (eg: u_d)

        yd_0 = [initial_conditions[str(diff_i.args[0])+'_d'] for diff_i in ydmap.keys()]

        if self.solver == None or self.solver == 'IDA':

            yd_0.append(0.)

            # ========= SET SOLVER INSTANCES ==============

            problem_instance = Implicit_Problem(res=self.compiled_equations,
                                                y0=y_0,
                                                yd0= yd_0,
                                                t0=initial_time,
                                                name='IDA'
                                        )

            problem_instance.algvar = self.problem.equation_block._getBooleanDiffFlagsForEquations()

            solver_instance = IDA(problem_instance)

            #solver_instance.suppress_alg = True

            #solver_instance.atol=???

            #========== SOLVE THE PROBLEM =================

            f_0_ = self.compiled_equations

            f_0 = self.compiled_equations(initial_time,y_0, yd_0)

            #print("\n\n y_0 = %s \n yd_0 = %s \n n = %s \n f_0? = %s \n f(t0,y0,yd0) = %s"%(y_0, yd_0, number_of_time_steps, f_0_, f_0))

            solver_instance.make_consistent('IDA_YA_YDP_INIT')

            verbosity_levels={0:50, 1:30, 2:10}

            solver_instance.verbosity = verbosity_levels[conf_args['verbosity_solver']]

            Time, Y, Yd = solver_instance.simulate(end_time, 0, time_points)

            #================================================

        to_register_ = np.hstack((np.array(time_points).reshape(-1,1), Y))

        if self.additional_configurations['print_output'] == True:

            tab = prettytable.PrettyTable()

            tab.field_names = self.additional_configurations['output_headers']

            for i in range(len(time_points)):

                tab.add_row(np.concatenate(([time_points[i]], Y[i,:])))

            print(tab)

        self.domain._register(to_register_)

        # ============ Rename domain columns =============

        variable_map = self.additional_configurations['variable_name_map']

        if variable_map is not {}:

            self.domain._renameHeaders(variable_map)

        # ================================================

        return Time, Y
