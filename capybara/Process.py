"""
A class for definition of each process (aka: unitary ops), holding all the equations in one place
"""

import numpy as np
from daetools.pyDAE import *
from pyUnits import m, g, kg, s, K, mol, kmol, J, um
import beautifultable

class Process(daeModel):

    """
    Definition of the process (also known as unitary operations) 
    """

    def __init__(self,name,parent=None,description=""):
        super(Process,self).__init__(self,name,parent,description)

        """
        Initial function for PROCESS loading the parent class daeModel
        """

    def return_info(self):

        """
        List info for the collection of PROCESSES included in the present problem

        :return:
            A table containing number of variables, equations, especifications and degrees of freedom for the current PROCESS
        
        :rtype: str
        """

        info_tab = beautifultable.BeautifulTable()

        info_tab.column_headers = ["Nb. Variables","Nb. Equations","Nb. Especifications"]
        info_tab.append_row([str(self.count_variables()),str(self.count_equations()),str(self.count_specs())])
        info_tab.append_row(["Nb. DgoF. = ", self.count_degrees_of_freedom()," "])

        return(info_tab)

    def count_variables(self):

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


    def count_specs(self):

        """
        Return the number of specifications included for the present process

        :return:
            Number of specifications included in the present process
        :rtype: int
        """

        pass

    def count_degrees_of_freedom(self):

        """
        Return the number of degrees of freedom included for the present process

        :return:
            Number of degrees of freedom included in the present process
        :rtype: int
        """

        pass
