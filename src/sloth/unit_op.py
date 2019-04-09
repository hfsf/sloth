# unit_op.py

"""
Define Models of some unit operations to be used in the model declaration
"""

from . import model
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *

class _mechanicalEquilibrium(model.Model):

    def __init__(self, name, description=""):

        super().__init__(name,"Mechanical Equilibrium")

        self.P_In = self.createVariable("P_In", Pa, "p_in")
        self.P_Out = self.createVariable("P_Out", Pa, "p_out")

        _mechanical_equilibrium = self.P_In() - self.P_Out()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

class _molarFluxConservation(model.Model):

    def __init__(self, name, description=""):

        super().__init__(name,"Mass flux conservation")

        self.N_In_Dot = self.createVariable("N_In_Dot", mol/s, "n_in_dot")
        self.N_Out_Dot = self.createVariable("N_Out_Dot", mol/s, "n_out_dot")

        _molar_conservation = self. self.N_In_Dot() - self.N_Out_Dot()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

class _massFluxConservation(model.Model):

    def __init__(self, name, description=""):

        super().__init__(name,"Mass flux conservation")

        self.M_In_Dot = self.createVariable("M_In_Dot", kg/s, "m_in_dot")
        self.M_Out_Dot = self.createVariable("M_Out_Dot", kg/s, "m_out_dot")

        _mass_conservation = self.M_In_Dot() - self.M_Out_Dot()

        self.createEquation("mass_flux_conservation", "Molar flux consevation", _mass_conservation)

class Mixer(model.Model):
    """
    Model for a mixer of material streams
    """

    def __init__(self, name, description="Mixer model", property_package=None):

        super().__init__(name, description, property_package)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass consevation", _mass_conservation)

        self.P_in = self.createVariable("P_in", Pa, "p_in", latex_text="{P}_{in}", is_exposed=True, type='input')
        self.P_out = self.createVariable("P_out", Pa, "p_out", latex_text="{P}_{out}", is_exposed=True, type='output')

        _mechanical_equilibrium = self.P_out() - self.P_in()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

class Tee(Mixer):

    """
    Model for a tee (separation in multiple streams from one initial one) of material streams
    """

    def __init__(self, name, description="Tee model", property_package=None):

        super().__init__(name, description, property_package)


class Tank(model.Model):


    def __init__(self, name, description="Tank"):

        super().__init__(name)

        self.t = self.createVariable("t",s,"time",latex_text="t")

        self.time_domain = Domain("time_domain", s, self.t, "time domain")

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')
        self.N = self.createVariable("N", mol, "molar holdup", latex_text="N")

        self.N.distributeOnDomain(self.time_domain)

        _molar_conservation = self.N.Diff(self.t) == self. self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')
        self.M = self.createVariable("M", kg, "mass holdup", latex_text="M")

        self.M.distributeOnDomain(self.time_domain)

        _mass_conservation = self.M.Diff(self.t) ==  self. self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        self.h_in  = self.createVariable("h_in", J/mol, "molar enthalpy input", latex_text="h_{in}", is_exposed=True, type='input')
        self.h_out = self.createVariable("h_out", J/mol, "molar enthalpy output", latex_text="h_{out}", is_exposed=True, type='output')
        self.E = self.createVariable("E", J, "Internal energy", latex_text="E")

        self.Q = self.createParameter("Q", J, "Heat rate", latex_text="Q", value=0.)

        self.E.distributeOnDomain(self.time_domain)

        _energy_balance = self.E.Diff(self.t) == self.n_dot_in*self.h_in() - self.n_dot_out*self.h_out() + self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        self.level = self.createVariable("level", m, "liquid level", latex_text="L")
        self.area_sec = self.createParameter("area_sec", m**2, "squared section area", latex_text="{A}_{sec}")

        self.P_In = self.createVariable("P_In", Pa, "p_in")
        self.P_Out = self.createVariable("P_Out", Pa, "p_out")

        _mechanical_equilibrium = self.P_In() - self.P_Out()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)


class Centrifuge:

    pass

class Fermenter(Tank):

    def __init__(self, name, description="Fermenter", property_package=None):

        super().__init__(name, description, property_package)

class Valve(model.Model):

    def __init__(self, name, description="Valve", property_package=None):

        super().__init__(name, description, property_package)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        self.perc_open = self.createParameter("perc_open", dimless, "percentage of opening", latex_text="{\\%}_{open}")

        self.H_in = self.createVariable("H_in", J/mol, "input molar enthalpy", latex_text="{H}_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "output molar enthalpy", latex_text="{H}_{out}", is_exposed=True, type='output')

        self.P_in = self.createVariable("P_In", Pa, "p_in", latex_text="{P}_{in}", is_exposed=True, type='input')
        self.P_out = self.createVariable("P_Out", Pa, "p_out", latex_text="{P}_{out}", is_exposed=True, type='output')
        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")


    def DeclareEquations(self):


        _molar_conservation = self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        _mass_conservation = self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        _isoenthalpy = self.H_in()*self.ndot_in() - self.H_out()*self.ndot_out()

        self.createEquation("isoenthalpy", "isoenthalpy", _isoenthalpy)

        _mechanical_equilibrium = self.P_out() - self.P_in() + self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)


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