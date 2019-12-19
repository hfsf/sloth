# *coding:utf-8

"""
Define Simulation class
"""

from .plotter import Plotter
from .problem import Problem
from .model import Model
from . import solvers
from . import analysis
from .core.error_definitions import UnexpectedValueError, UnresolvedPanicError, AbsentRequiredObjectError
import prettytable
import numpy as np
from collections import OrderedDict
import json
from .core.quantity import Quantity

class Simulation:

    """
    Simulation class definition
    """

    def __init__(self, name, description="", problem=None, plotter=None):

        """
        Instantiate Simulation.

        :ivar str name:
            Name for the current simulation

        :ivar str description:
            Description of the current simulation

        :ivar Problem problem:
            Problem to be studied in the current simulation
        """

        self.name = name

        self.description = description

        self.problem = problem

        self.output = None

        self.configurations = None

        if plotter is None:
          plotter = Plotter(simulation=self)

        self.plotter = plotter

        self.domain = None

        self.status = None

    def report(self, object):

        """
        Print the report output for the current object

        :param [Model, Problem] object:
            Object to be analyzed
        """

        analist = analysis.Analysis()

        if isinstance(object, Model):

            print(analist.modelReport(object))

        elif isinstance(object, Problem):

            print(analist.problemReport(object))

        else:

            raise UnexpectedValueError("[Model, Problem]")

    def setProblem(self, problem):

        """
        Set the Problem object for the current simulation

        :param Problem problem:
        """

        self.problem = problem

    def setConfigurations(self,
                          initial_time=0.,
                          end_time=None,
                          linear_solver='sympy',
                          nonlinear_solver='sympy',
                          differential_solver='ODEINT',
                          differential_algebraic_solver='IDA',
                          problem_type=None,
                          is_dynamic=False,
                          compile_equations=True,
                          domain=None,
                          time_variable_name=None,
                          arg_names=[],
                          args=[],
                          verbosity_solver=0,
                          number_of_time_steps=100,
                          configuration_args={},
                          print_output=False,
                          output_headers=None,
                          variable_name_map={},
                          compilation_mechanism="numpy",
                          definition_dict=None,
                          configurations_file=None,
                          number_parameters_to_optimize=0,
                          times_for_solution=None):

        """
        Set the configurations of the current simulation using the defined parameters

        :ivar dict definition_dict:
            Dictionary containing configurations for override all Simulation.runSimulation arguments with those defined in it. Tipically used for performing consecutive simulations (eg: optimization) or using predefined simulation configurations
        """

        if configurations_file is not None:

            with open(configurations_file, "r") as read_file:

                additional_conf = json.load(read_file)

        elif definition_dict is not None and isinstance(definition_dict, dict):

            additional_conf = definition_dict

        else:

            if time_variable_name is None and is_dynamic is True:

                time_variable_name = self.problem.time_variable_name

            additional_conf = {'compile_equations':compile_equations,
                               'domain':domain,
                               'time_variable_name':time_variable_name,
                               'initial_time':initial_time,
                               'end_time':end_time,
                               'is_dynamic':is_dynamic,
                               'arg_names':arg_names,
                               'linear_solver':linear_solver,
                               'nonlinear_solver':nonlinear_solver,
                               'differential_solver':differential_solver,
                               'differential_algebraic_solver':differential_algebraic_solver,
                               'problem_type':problem_type,
                               'args':args,
                               'verbosity_solver':verbosity_solver,
                               'number_of_time_steps':number_of_time_steps,
                               'configuration_args':configuration_args,
                               'print_output':print_output,
                               'output_headers':output_headers,
                               'variable_name_map':variable_name_map,
                               'compilation_mechanism':compilation_mechanism,
                               'number_parameters_to_optimize':number_parameters_to_optimize,
                               'times_for_solution':times_for_solution
                               }

        #print("additional_conf is: %s"%additional_conf)

        if number_parameters_to_optimize != 0 and additional_conf['number_parameters_to_optimize'] != number_parameters_to_optimize:

            additional_conf['number_parameters_to_optimize'] = number_parameters_to_optimize

        self.configurations = additional_conf

    def runSimulation(self, show_output_msg = False):

        problem_type = self.configurations['problem_type']

        number_parameters_to_optimize = self.configurations['number_parameters_to_optimize']

        if problem_type == None:

            problem_type = self.problem._getProblemType()

        if problem_type == "linear":

            solver_mechanism = solvers._createSolver(self.problem, self.configurations)

        elif problem_type == "nonlinear":

            solver_mechanism = solvers._createSolver(self.problem, self.configurations)

        elif problem_type == "differential":

            solver_mechanism = solvers._createSolver(self.problem, self.configurations)

        elif problem_type == "differential-algebraic":

            solver_mechanism = solvers._createSolver(self.problem, self.configurations)
        else:

            raise UnexpectedValueError("EquationBlock")

        dof_analist = analysis.DOF_Analysis(self.problem, number_parameters_to_optimize)

        dof_analist._makeSanityChecks()

        out = solver_mechanism.solve(self.configurations)

        '''
        if print_output==True and problem_type != 'differential':

          print("\n ->{}".format(out))
        '''

        self.output = out

        self.domain = self.configurations['domain']

        if show_output_msg is True:

            exit_status = self.getStatus()

            if exit_status == 0:

                print("Simulation ended sucessfully with status ",exit_status,".")

            if exit_status is not 0:

                print("Simulation ended unsucessfully with status=",exit_status,".\n Some sort of error ocurred.")

    def getStatus(self):

        """
        Get the status of the current simulation (0 for sucess, >=1 for errors)
        """

        if self.getResults() is not []:

            self.status = 0

        else:

            self.status = 1

        return self.status

    def showResults(self):

        """
        Show the results for the current simulation in a table for easy visualization
        """

        assert self.output!=None, "\nShould run the simulation prior to showing results."

        if self.configurations['is_dynamic'] == True:

            # Dynamic output. Output is a tuple (time_points, Y)

            time_points, Y = self.output

            header = '\nResult summary:\n'

            tab = prettytable.PrettyTable()

            tab.field_names = self.configurations['output_headers']

            for i in range(len(time_points)):

                tab.add_row(np.concatenate(([time_points[i]], Y[i,:])))

            print(header+str(tab))

        else:

            header = '\nResult summary:\n'

            tab = prettytable.PrettyTable()

            tab.field_names=["Variable","Unit","Value"]

            for var_i in list(self.output.keys()):

                tab.add_row([ str(var_i),
                              str(self.problem.equation_block.variable_dict[str(var_i)].units),
                              self.output[var_i]
                            ]
                )

            print(header + str(tab))

    def plotTimeSeries(self, x_data=None, y_data=None, set_style='darkgrid', x_label='time', y_label='output', labels=None, linewidth=2.5, markers=None, grid=False, save_file=None, show_plot=True, data=None, legend=False):

        self.plotter.plotTimeSeries(x_data=x_data,
                                     y_data=y_data,
                                     set_style=set_style,
                                     x_label=x_label,
                                     y_label=y_label,
                                     linewidth=linewidth,
                                     labels=labels,
                                     markers=markers,
                                     grid=grid,
                                     save_file=save_file,
                                     show_plot=show_plot,
                                     legend=legend,
                                     data=data
                    )

    def getResults(self, return_type='list'):

        """
        Return the output of the current simulation according to the desired type

        :param str return_type:
            Type of the output to be returned ('dict', 'list'). Defaults to 'list'
        """

        problem_type = self.problem._getProblemType()

        if problem_type == 'linear' or problem_type == 'nonlinear':

            if return_type == 'list':

                try:

                    return [float(i) for i in list(self.output.values())]

                except:

                    print("Output = ",self.output)

                    try:
                        print("Output values = ",self.output.values())

                    except:

                        pass

                    raise TypeError("!")

            elif return_type == 'dict':

                output_dict = OrderedDict(sorted(self.output.items(), key=lambda x: str(x[0])))

                try:

                    output_dict = {str(k):float(v) for (k,v) in output_dict.items()}

                    return output_dict

                except:

                    print("Output = ",self.output)
                    print("Output values = ",self.output.values())

                    raise TypeError("!")

            else:

                raise UnexpectedValueError("string ('list', 'dict')")

        elif problem_type == 'differential' or problem_type == 'differential-algebraic':

            domain_ = self.configurations['domain']

            if return_type == 'list':

                return [domain_.values[ind_i].values
                        for ind_i in domain_.values.keys()
                    ]

            elif return_type == 'dict':

                return {ind_i:domain_.values[ind_i].to_dict(orient='list')
                        for ind_i in domain_.values.keys()
                    }

            else:

                raise UnexpectedValueError("string ('list', 'dict')")

        else:

            raise UnresolvedPanicError("\nProblem type not recognized.\n")

    def dumpConfigurations(self, file_name=None):

        """
        Dump the configurations used for running the simulation into one JSON file for later utilization (eg: optimization studies, or re-simulation)

        :param str file_name:
            File name for dumping the configurations. Defaults to None, which will use the name of the simulation '<NAME_OF_THE_SIMULATION>-conf.json'

        :return:
            JSON file containing the configurations
        :rtype JSON:
        """

        if file_name is None:

            file_name = self.name+'-conf.json'

        with open(file_name, "w") as write_file:

            json.dump(self.configurations, write_file)

    def reset(self):

        """
        Reset current simulation, in order to restore its initial state
        """

        if self.domain is not None:

            self.domain._reset()

    def __getitem__(self, obj):

        """
        Overloaded function for searching for an specific Parameter through the equations defined for the Problem used in current Simulation

        :param (str, Quantity) obj:
            Parameter which will be searched among the equations for the current simulation
        :return obj_reference:
            Parameter referenced by the argument obj_name
        :rtype Quantity:
        """

        if isinstance(obj, str):

            return self.problem.equation_block.parameter_dict[obj]

        elif isinstance(obj, Quantity):

            return self.problem.equation_block.parameter_dict[obj.name]

        else:

            raise UnexpectedValueError("(str, Quantity)")
