"""
Define Equation class.
Creates objects that holds variables, parameters
"""

import numpy as np

class Equation:

    """

    Equation class, that holds capabilites to:
    - Almost-writing-syntax equations using previously defined variables and parameters objects
    - Use dimensional coherence analisys for mathematical operations among variables and parameters


    *TODO: - Dimensional coherence among math operations
           - Overload basic mathematical operators (add, subtract, multiply, divide)
    """

    def __init__(self, name, description):

        """
        Inidial definitions.

        :param str name:
        Name for the current equation

        :param str description:
        Description for the present equation. Defauls to ""
        
        """

        self.name = name

        self.description = description

        #Residual of the current equation

        self.residual = None


