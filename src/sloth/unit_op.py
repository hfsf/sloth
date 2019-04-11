# unit_op.py

"""
Define Models of some unit operations to be used in the model declaration
"""

from . import model
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *

class MaterialStream(model.Model):

    """
    Model for a simple material stream (homogeneous)

    *INPUTS: -
    *OUTPUTS: mdot_out, mdot_out, h_out, P_out
    *PARAMETERS: mdot, ndot, P, H, T

    *REQUIRES: PropertyPackage
    """

    def __init__(self, name, description="Material stream", property_package=None):

        super().__init__(name, description, property_package)

        self.mdot = self.createParameter("mdot", kg/s, "Mass flux for stream")
        self.ndot = self.createParameter("ndot", mol/s, "Molar flux for stream")
        self.P = self.createParameter("P", Pa, "Pressure for stream")
        self.H = self.createParameter("H", J/mol, "Molar enthalpy for stream")
        self.T = self.createParameter("T", K, "Temperature for stream")

        self.mdot_out = self.createVariable("mdot_out",kg/s, "Mass flux from stream", is_exposed=True, type="output")
        self.ndot_out = self.createVariable("ndot_out",mol/s, "Molar flux from stream",is_exposed=True, type="output")
        self.P_out = self.createVariable("P_out", Pa, "Pressure from stream",is_exposed=True, type="output")
        self.H_out = self.createVariable("H_out", J/mol, "Molar enthalpy from stream",is_exposed=True, type="output")
        self.T_out = self.createVariable("T_out", K, "Temperature from stream",is_exposed=True, type="output")

    def DeclareParameters(self):

        #try to set values if the property_package was defined
        if self.property_package is not None:

            if self.mdot.is_specified is True and self.ndot.is_specified is not True:

                self.ndot.setValue( self.mdot.value/(self.property_package["*"].MW*1e-3) )

            if self.mdot.is_specified is not True and self.ndot.is_specified is True:

                self.mdot.setValue( self.ndot.value*self.property_package["*"].MW*1e-3 )

        #Recalculate property_package if T and P where provided

        if self.T.is_specified is True and self.P.is_specified is False:

            self.property_package.calculate(T=self.T.value)

        if self.T.is_specified is False and self.P.is_specified is True:

            self.property_package.calculate(P=self.P.value)

        if self.T.is_specified is True and self.P.is_specified is True:

            self.property_package.calculate(T=self.T.value, P=self.P.value)

    def DeclareEquations(self):

        #Create equations for output of streams using parameter values

        self.createEquation("mass_flux", self.mdot_out.description, self.mdot_out() - self.mdot() )
        self.createEquation("molar_flux", self.ndot_out.description, self.ndot_out() - self.ndot() )
        self.createEquation("pressure_output", self.P_out.description, self.P_out() - self.P() )
        self.createEquation("enthalpy_output", self.H_out.description, self.H_out() - self.H())
        self.createEquation("temperature_output", self.T_out.description, self.T_out() - self.T())

class MultiphasicMaterialStream(model.Model):


    """
    Model for a biphasic material stream

    *INPUTS: -
    *OUTPUTS: mdot_out, mdot_out, h_out, P_out
    *PARAMETERS: mdot, ndot, P, H, T, x_<phase1_name>, x_<phase2_name>, w_<phase1_name>, w_<phase2_name>

    *REQUIRES: PropertyPackage[phase1, phase2]
    """

    def __init__(self, name, description="Biphasic material stream", property_package=None):

        super().__init__(name, description, property_package)

        self.mdot = self.createParameter("mdot", kg/s, "Mass flux for stream")
        self.ndot = self.createParameter("ndot", mol/s, "Molar flux for stream")
        self.P = self.createParameter("P", Pa, "Pressure for stream")
        self.H = self.createParameter("H", J/mol, "Molar enthalpy for stream")
        self.T = self.createParameter("T", K, "Temperature for stream")

        for phase_i in self.property_package.phase_names:

            exec("self.x_{}=createParameter('x_{}',dimless,'Molar fraction for {} phase')".format(phase_i))
            exec("self.w_{}=createParameter('w_{}',dimless,'Mass fraction for {} phase')".format(phase_i))

        self.T = self.createParameter("T", K, "Temperature for stream")

        self.mdot_out = self.createVariable("mdot_out",kg/s, "Mass flux from stream", is_exposed=True, type="output")
        self.ndot_out = self.createVariable("ndot_out",mol/s, "Molar flux from stream",is_exposed=True, type="output")
        self.P_out = self.createParameter("P", Pa, "Pressure from stream",is_exposed=True, type="output")
        self.H_out = self.createParameter("H", J/mol, "Molar enthalpy from stream",is_exposed=True, type="output")
        self.T_out = self.createParameter("T", K, "Temperature from stream",is_exposed=True, type="output")

    def DeclareParameters(self):

        #try to set values if the property_package was defined
        if self.property_package is not None:

            if self.mdot.is_specified is True and self.ndot.is_specified is not True:

                self.ndot.setValue( self.mdot.value/(self.property_package["*"].MW*1e-3) )

            if self.mdot.is_specified is not True and self.ndot.is_specified is True:

                self.mdot.setValue( self.ndot.value*self.property_package["*"].MW*1e-3 )

        #Recalculate property_package if T and P where provided

        if self.T.is_specified is True and self.P.is_specified is False:

            self.property_package.calculate(T=self.T.value)

        if self.T.is_specified is False and self.P.is_specified is True:

            self.property_package.calculate(P=self.P.value)

        if self.T.is_specified is True and self.P.is_specified is True:

            self.property_package.calculate(T=self.T.value, P=self.P.value)

    def DeclareEquations(self):

        #Create equations for output of streams using parameter values

        self.createEquation("mass_flux", self.mdot_out.description, self.mdot_out() - self.mdot() )
        self.createEquation("molar_flux", self.ndot_out.description, self.ndot_out() - self.ndot() )
        self.createEquation("pressure_output", self.P_out.description, self.P_out() - self.P() )
        self.createEquation("enthalpy_output", self.H_out.description, self.H_out() - self.H())
        self.createEquation("temperature_output", self.T_out.description, self.T_out() - self.T())

class Mixer(model.Model):
    """
    Model for a mixer of material streams

    *INPUTS: ndot_in, mdot_in, H_in, P_in
    *OUTPUTS: mdot_out, mdot_out, H_out, P_out
    *PARAMETERS: -

    *REQUIRES: -
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

        self.H_in =  self.createVariable("H_in", J/mol, "molar enthalpy for output stream", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out =  self.createVariable("H_out", J/mol, "molar enthalpy for output stream", latex_text="H_{out}", is_exposed=True, type='output')

        _energy_balance = self.ndot_out()*self.H_out() - self.ndot_in()*self.H_in()

        self.createEquation("energy_balance","Energy balance", _energy_balance)

class Tee(Mixer):

    """
    Model for a tee (separation in multiple streams from one initial one) of material streams
    """

    def __init__(self, name, description="Tee model", property_package=None):

        super().__init__(name, description, property_package)


class Tank(model.Model):


    def __init__(self, name, description="Tank", property_package=None):

        """
        Defines a generic tank

        *INPUTS: ndot_in, mdot_in, h_in, P_in
        *OUTPUTS: mdot_out, mdot_out, h_out, P_out
        *PARAMETERS: area_sec, Q

        *REQUIRES: PropertyPackage
        """

        super().__init__(name, description, property_package)

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

        self.H_in  = self.createVariable("H_in", J/mol, "molar enthalpy input", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "molar enthalpy output", latex_text="H_{out}", is_exposed=True, type='output')
        self.E = self.createVariable("E", J, "Internal energy", latex_text="E")

        self.Q = self.createParameter("Q", J, "Heat rate", latex_text="Q", value=0.)

        self.E.distributeOnDomain(self.time_domain)

        _energy_balance = self.E.Diff(self.t) == self.n_dot_in()*self.H_in() - self.n_dot_out()*self.H_out() + self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        self.level = self.createVariable("level", m, "liquid level", latex_text="L")
        self.area_sec = self.createParameter("area_sec", m**2, "squared section area", latex_text="{A}_{sec}")

        self.level.distributeOnDomain(self.time_domain)

        _level_balance = self.level.Diff(self.t) == (1./(self.property_package["*"].rho*self.area_sec()))*(self.mdot_in()-self.mdot_out())

        self.createEquation("_level_balance", "Liquid level balance", _level_balance)

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

class Heater(model.Model):

    def __init__(self, name, description="Heater", property_package=None):

        """
        Defines a generic heater

        *INPUTS: ndot_in, mdot_in, h_in, P_in
        *OUTPUTS: mdot_out, mdot_out, h_out, P_out
        *PARAMETERS:  Q, Delta_P

        *REQUIRES: PropertyPackage
        """

        super().__init__(name, description, property_package)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        _molar_conservation = self. self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        _mass_conservation = self. self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        self.H_in  = self.createVariable("H_in", J/mol, "molar enthalpy input", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "molar enthalpy output", latex_text="H_{out}", is_exposed=True, type='output')

        self.Q = self.createParameter("Q", J, "Heat rate", latex_text="Q", value=0.)

        _energy_balance = self.n_dot_out()*self.H_out() - self.n_dot_in()*self.H_in() - self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        self.P_In = self.createVariable("P_In", Pa, "p_in")
        self.P_Out = self.createVariable("P_Out", Pa, "p_out")
        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")

        _mechanical_equilibrium = self.P_out() - self.P_in() + self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)


class Cooler(model.Model):

    def __init__(self, name, description="Heater", property_package=None):

        """
        Defines a generic cooler

        *INPUTS: ndot_in, mdot_in, h_in, P_in
        *OUTPUTS: mdot_out, mdot_out, h_out, P_out
        *PARAMETERS:  Q, Delta_P

        *REQUIRES: PropertyPackage
        """

        super().__init__(name, description, property_package)

        self.ndot_in  = self.createVariable("ndot_in", mol/s, "molar input flux", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')
        self.ndot_out = self.createVariable("ndot_out", mol/s, "molar output flux", latex_text="\\dot{n}_{out}", is_exposed=True, type='output')

        _molar_conservation = self. self.ndot_in() - self.ndot_out()

        self.createEquation("molar_conservation", "Molar consevation", _molar_conservation)

        self.mdot_in  = self.createVariable("mdot_in", kg/s, "mass input flux", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')
        self.mdot_out = self.createVariable("mdot_out", kg/s, "mass output flux", latex_text="\\dot{m}_{out}", is_exposed=True, type='output')

        _mass_conservation = self. self.mdot_in() - self.mdot_out()

        self.createEquation("mass_conservation", "Mass conservation", _mass_conservation)

        self.H_in  = self.createVariable("H_in", J/mol, "molar enthalpy input", latex_text="H_{in}", is_exposed=True, type='input')
        self.H_out = self.createVariable("H_out", J/mol, "molar enthalpy output", latex_text="H_{out}", is_exposed=True, type='output')

        self.Q = self.createParameter("Q", J, "Heat rate", latex_text="Q", value=0.)

        _energy_balance = self.n_dot_out()*self.H_out() - self.n_dot_in()*self.H_in() + self.Q()

        self.createEquation("energy_balance", "Energy balance", _energy_balance)

        self.P_In = self.createVariable("P_In", Pa, "p_in")
        self.P_Out = self.createVariable("P_Out", Pa, "p_out")
        self.Delta_P = self.createParameter("Delta_P", Pa, "pressure drop", latex_text="{\\Delta P}")

        _mechanical_equilibrium = self.P_out() - self.P_in() + self.Delta_P()

        self.createEquation("mechanical_equilibrium", "Mechanical Equilibrium", _mechanical_equilibrium)

class Flash:

    pass

class DistillationColumn:

    pass