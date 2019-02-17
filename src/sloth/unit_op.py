# unit_op.py

"""
Define Models of some unit operations to be used in the model declaration
"""

from . import model
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *

class _molarFluxConservation(model.Model):

    def __init__(self, name, description=""):

        super().__init__(name,"Mass flux conservation")

        self.N_In_Dot = self.createVariable("N_In_Dot", mol/s, "n_in_dot")
        self.N_Out_Dot = self.createVariable("N_Out_Dot", mol/s, "n_out_dot")

        _molar_conservation = self.N_In_Dot() - self.N_Out_Dot()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

class _massFluxConservation(model.Model):

    def __init__(self, name, description=""):

        super().__init__(name,"Mass flux conservation")

        self.M_In_Dot = self.createVariable("M_In_Dot", kg/s, "m_in_dot")
        self.M_Out_Dot = self.createVariable("M_Out_Dot", kg/s, "m_out_dot")

        _mass_conservation = self.M_In_Dot() - self.M_Out_Dot()

        self.createEquation("mass_flux_conservation", "Molar flux consevation", _mass_conservation)

class Mixer(_molarFluxConservation, _massFluxConservation):

    """
    Model for a mixer of material streams
    """

    def __init__(self, name, description="Mixer model"):

        super().__init__(name)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}")
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}")
        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}")
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}")

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