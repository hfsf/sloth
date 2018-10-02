"""
A class for definition of each process (aka: unitary ops), holding all the equations in one place
"""

import numpy as np
import daetools.pyDAE as pydae


class Process:

    """
    Definition of the process (also known as unitary operations) 
    """

    def __init__(self):

        """
        Initial
        """

    def retrn_info(self):

        """
        List info for the collection of PROCESSES included in the present problem

        :return:
            None
        """

        for i in self.processes.iterkeys():

            print self.processes[i].name, "\n\n", self.processes[i].return_info()

    def count_vars(self):

        """
        Return the number of variables included in the equations for the present process

        :return:
            Number of variables included in the present process
        :rtype: int
        """

        pass


    def count_equations(self):

        """
        Return the number of equations included for the present process

        :return:
            Number of equations included in the present process
        :rtype: int
        """

        pass

