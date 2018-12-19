# *coding:utf-8

"""
Define Simulation class
"""

from .plotter import Plotter
from .problem import Problem
from .model import Model
from . import solvers
from . import analysis
from .core.error_definitions import UnexpectedValueError, UnresolvedPanicError
import prettytable
import numpy as np
from collections import OrderedDict

class Simulation:

    """
    Simulation class definition
    """

    def __init__(self, name, description="", problem=None):

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

        self.plotter = Plotter()

        self.domain = None

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

    def runSimulation(self, initial_time=0., 
                      end_time=None, 
                      linear_solver='sympy', 
                      nonlinear_solver='sympy', 
                      differential_solver='scipy', 
                      differential_algebraic_solver='scipy', 
                      problem_type=None, 
                      is_dynamic=False, 
                      compile_diff_equations=True, 
                      domain=None, 
                      time_variable_name='t', 
                      arg_names=[], 
                      args=[], 
                      number_of_time_steps=100, 
                      configuration_args={}, 
                      print_output=False, 
                      output_headers=None,
                      variable_name_map={}, 
                      compilation_mechanism="numpy",
                      definition_dict=None
                      ):

        """
        Run the current simulation using the defined parameters

        :ivar dict definition_dict:
            Dictionary containing configuratios for override all Simulation.runSimulation arguments with those defined in it. Tipically used for performing consecutive simulations (eg: optimization) or using predefined simulation configurations
        """

        if definition_dict is not None and isinstance(definition_dict, dict):

            additional_conf = definition_dict

        else:

            additional_conf = {'compile_diff_equations':compile_diff_equations, 
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
                               'args':args,
                               'number_of_time_steps':number_of_time_steps,
                               'configuration_args':configuration_args,
                               'print_output':print_output,
                               'output_headers':output_headers,
                               'variable_name_map':variable_name_map,
                               'compilation_mechanism':compilation_mechanism
                               }

        self.configurations = additional_conf

        if problem_type == None:

            problem_type = self.problem._getProblemType()

        if problem_type == "linear":

            solver_mechanism = solvers._createSolver(self.problem, additional_conf)

        elif problem_type == "nonlinear":

            solver_mechanism = solvers._createSolver(self.problem, additional_conf)
        
        elif problem_type == "differential":

            solver_mechanism = solvers._createSolver(self.problem, additional_conf)     
        elif problem_type == "differential-algebraic":

            pass
        
        else:

            raise UnexpectedValueError("EquationBlock")


        dof_analist = analysis.DOF_Analysis(self.problem)

        dof_analist._makeSanityChecks()

        out = solver_mechanism.solve(additional_conf)

        if print_output==True and problem_type != 'differential':

          print("\n ->{}".format(out))

        self.output = out

        self.domain = additional_conf['domain']

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
                              str(self.problem.equation_block._var_dict[str(var_i)].units),
                              self.output[var_i]
                            ]
                )
            
            print(header + str(tab))

    def plotResults(self, x_data=None, y_data=None, set_style='darkgrid', x_label='time', y_label='output', labels=None, linewidth=2.5, markers=None, grid=False, save_file=None, show_plot=True, data=None, legend=False):
    
        self.plotter.plotSimpleLines(x_data=x_data,
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

                return list(self.output.values())

            elif return_type == 'dict':

                output_dict = OrderedDict(sorted(self.output.items(), key=lambda x: str(x[0])))

                output_dict = {str(k):v for (k,v) in output_dict.items()}

                return output_dict

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
