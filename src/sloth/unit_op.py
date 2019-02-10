# unit_op.py

"""
Define Models of some unit operations to be used in the model declaration
"""

from . import model
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *

class _molarFluxConservation(model.Model):

    def __init__(self):

        super().__init__("","")

        self.n_in_dot = self.createVariable("n_in_dot", mol/s, "n_in_dot")
        self.n_out_dot = self.createVariable("n_out_dot", mol/s, "n_out_dot")

        _molar_conservation = self.n_in_dot() - self.n_out_dot()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

class _massFluxConservation(model.Model):

    def __init__(self):

        super().__init__("","")

        self.m_in_dot = self.createVariable("m_in_dot", kg/s, "m_in_dot")
        self.m_out_dot = self.createVariable("m_out_dot", kg/s, "m_out_dot")

        _mass_conservation = self.m_in_dot() - self.m_out_dot()

        self.createEquation("mass_flux_conservation", "Molar flux consevation", _mass_conservation)

class Mixer:

    pass

class Tee:

    pass

class Recycle:

    pass

class Tank:

    pass

class Centrifuge:

    pass

class Fermenter:

    pass

class Valve:

    pass

class Pump:

    pass

class HeatExchanger:

    pass

class Heater:

    pass

class Cooler:

    pass

class Flash:

    pass

class DistillationColumn:

    pass