"""
Define model class.
Creates equations, variables, parameters instantiating proper classes (Equation,Variable,etc)
"""

import Equation
import numpy as np

class Model:

    """

    Model class, that holds the capabilites for:
    - Equation definition, parameter definition, and parameter specification
    - Evaluation of degrees of freedom

    *TODO: - Implement model template possibility (eg: use another model as template for the current one)
           - Define equation storage mechanism (dict?) 

    """

    def __init__(self, name, description = ""):

        """
        Initial definition.

        :param str name:
        Name for the current model

        :param str description:
        Description for the current model. Defaults to ""

        """

        self.name = name

        self.description = description

    def createEquation(self, name, description = ""):

        """
        Creates a equation for the current model
        """

        pass


    def countNumberOfVariables(self):

        """
        Returns the number of variables contained in the present model

        :rtype int n_vars:
        Number of variables defined in the present model

        """


    def countNumberOfEquations(self):

        """
        Returns the number of equations in the present model

        :rtype int n_eqs:
        Number of equations defined in the present model

        """
