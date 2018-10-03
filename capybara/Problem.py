"""
A class-container for the problems defined, holding all the equations in one place
"""

import numpy as np
from daetools.pyDAE import *

class Problem:

    """
    Container for several PROCESSES that hold all the equations in one place, thus allowing to simultaneous solving.
    """

    def __init__(self):

        """
        Initial
        """

        self.processes = {}

    def add(self, process_):

        """
        Add one process to this PROBLEM stack, holding the variables for posterior simultaneous utilization

        :param PROCESS process_:
            PROCESS to include in the current PROBLEM
        
        :return:
            None
        :rtype:
            None    
        """

        self.processes[process_.name] = process_

    def remove(self, name_to_remove=None):
        
        """
        Remove (in-place) one process by its name from this PROBLEM stack

        :param str name_to_remove:
            Name of the process to remove (in-place) from the stack. Default is None, which means that the last entry should be removed.

        :return:
            None
        :rtype:
            None
        """    

        if name_to_remove == None:
            name_to_remove = sorted(self.processes.keys())[-1]

        try:
            del (self.processes[name_to_remove])
        except KeyError:
            "\nERROR: Process not present in ",self.name," stack."

    def info(self):

        """
        List info for the collection of PROCESSES included in the present problem

        :return:
            None
        """

        for i in self.processes.iterkeys():

            print self.processes[i].name, "\n\n", self.processes[i].return_info()

    def count_processes(self):

        """
        Return the number of processes included in the present problem

        :return:
            Number of processes included in the present problem
        :rtype: int
        """

        return(len(self.processes.keys())) 


