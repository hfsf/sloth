"""

Define Connection class.
- Special type of Equation that are used as source or sink terms (process inlet or outlet, respectively) or to connect two different Model objects.

"""

from core.Equation import *

class base_(object):

    pass

class Connection(base_, Equation):

    def __init__(self, name="", description=""):

        super(self.__class__,self).__init__(name, description)

        pass
