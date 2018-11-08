# *coding:utf-8 *

"""
Define solver mechanisms
"""

class Solver:

    """
    Defines generic Solver class
    """

    def __init__(self, problem):

        """
        Instantiate Solver class

        :ivar Problem problem:
            Problem object on which the solver will operate
        """

        self.solver = None

        self.problem = problem

    