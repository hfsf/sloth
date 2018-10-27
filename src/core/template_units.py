import unit

"""
 ================ Templates for units for easy utilization ================ 
"""

_       = unit.Unit("None",      unit.null_dimension,    "adimensional")
m       = unit.Unit("m",         {'m':1},                "meter")
kg      = unit.Unit("kg",        {'kg':1},               "kilogram")
s       = unit.Unit("s",         {'s':1},                "second")
A       = unit.Unit("A",         {'A':1},                "ampere")
K       = unit.Unit("K",         {'K':1},                "kelvin")
mol     = unit.Unit("mol",       {'mol':1},              "mol")
cd      = unit.Unit("cd",        {'cd':1},               "candela")
_s      = unit.Unit("1/s",       s**(-1),                "per sencond")
_m2     = unit.Unit("1/m^2",     m**(-2),                "per squared meter")
_m3     = unit.Unit("1/m^3",     m**(-3),                "per cubic meter")
m_s     = unit.Unit("m/s",       m/s,                    "meter per second")
m_s2    = unit.Unit("m/s^2",     m/(s**2),               "acceleration")
kg_s    = unit.Unit("kg/s",      kg/s,                   "mass flux")
mol_s   = unit.Unit("mol/s",     mol/s,                  "molar flux")

"""
=============================================================================
"""