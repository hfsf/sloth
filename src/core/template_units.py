from .unit import Unit, null_dimension

"""
 ================ Templates for units for easy utilization ================ 
"""


# Primary units

_       = Unit("None",      null_dimension,        "adimensional")
m       = Unit("m",         {'m':1},               "meter")
kg      = Unit("kg",        {'kg':1},              "kilogram")
s       = Unit("s",         {'s':1},               "second")
A       = Unit("A",         {'A':1},               "ampere")
K       = Unit("K",         {'K':1},               "kelvin")
mol     = Unit("mol",       {'mol':1},             "mol")
cd      = Unit("cd",        {'cd':1},              "candela")
_s      = Unit("1/s",       s**(-1),               "per sencond")
_m2     = Unit("1/m^2",     m**(-2),               "per squared meter")
_m3     = Unit("1/m^3",     m**(-3),               "per cubic meter")
m_s     = Unit("m/s",       m/s,                   "meter per second")
m_s2    = Unit("m/s^2",     m/(s**2),              "acceleration")
kg_s    = Unit("kg/s",      kg/s,                  "mass flux")
mol_s   = Unit("mol/s",     mol/s,                 "molar flux")

#Derived units

Force   = Unit("Force",     kg*m_s2,               "Force")
Pa      = Unit("Pa",        Force/(m**2),          "Pascal")
J       = Unit("Joule",     kg*(m_s**2),            "Joule")
#Convenience units

UniversalIdealGasConstant = Unit("R", J*(K**-1)*(mol**-1), "Universal ideal gas constant")

"""
=============================================================================
"""