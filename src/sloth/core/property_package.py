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

    def __init__(self, phases=1, phase_names=['water'], ws=[.1], zs=None):

        """
        Instantiate PropertyPackage
        """

        self.number_of_phases = phases

        self.phase_names = phase_names

        self.T = 298.15

        self.P = 101325

        self.phases = {phase_i: thermo.chemical.Chemical(phase_i, self.T, self.P) for phase_i in phase_names if phase_i is not None}

        self.ws = ws

        self.zs = zs

        self.mixture = None

        self.eos = {}

    def resolve_mixture(self):

        self.mixture = thermo.mixture.Mixture(phase_names, ws, zs)

        self.zs = self.mixture.zs

        self.ws = self.mixture.ws

    def __add__(self, pp):

        """
        Overloaded function for inclusion of property packages into one resultant object
        """

        if isinstance(pp, self.__class__):

            for phase_i in pp.phase_names :

                if phase_i not in self.phase_names:

                    self.phase_names.append(phase_i)

                    self.phases.update({phase_i: pp.phases[phase_i]})

            return self

        else:

            raise UnexpectedValueError("PropertyPackage")


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