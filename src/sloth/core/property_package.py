#coding:utf-8

"""
Define ProperyPackage class, which holds the information about the species involved in the simulation, and act as a container for their properties
"""

import thermo
from .error_definitions import *

class PropertyPackage:

    """
    Class that defines the PropertyPackage object, which constains information about the species involved in the simulation and their properties
    """

    def __init__(self, phases=1, phase_names=['water']):

        """
        Instantiate PropertyPackage
        """

        self.number_of_phases = phases

        self.phase_names = phase_names

        self.T = 298.15

        self.P = 101325

        self.phases = {phase_i: thermo.chemical.Chemical(phase_i, self.T, self.P) for phase_i in phase_names if phase_i is not None}

        self.eos = {}

    def set_T(self, T):

        """
        """

        if isinstance(T, float):

            self.T = T

        else:

            raise AbsentRequiredObjectError("float")

    def set_P(self, P):

        """
        """

        if isinstance(P, float):

            self.P = P

        else:

            raise AbsentRequiredObjectError("float")

    def set_eos(self):

        """
        """

        pass

    def __getitem__(self, phase_name):

        """
        """

        if phase_name == "*":

            phase_name = list(self.phases.keys())[-1]

        return self.phases[phase_name]

    def calculate(self, T=298.15, P=101325):

        """
        """

        #Update properties of all phases

        _ = [self.phases[i].calculate(T,P) for i in self.phase_names]