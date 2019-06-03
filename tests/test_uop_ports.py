#test_uop_ports.py

from pathlib import Path
import sys

root_dir = Path(Path.cwd()).parent

sys.path.append(str(root_dir))#+'/src/')

import pytest

from src.sloth.model import Model
from src.sloth.problem import Problem
from src.sloth.simulation import Simulation
from src.sloth.core.property_package import PropertyPackage
from src.sloth.core.equation_operators import *
from src.sloth.core.template_units import *
from src.sloth.core.domain import *

from src.sloth.unit_op_library import MaterialStream
from src.sloth.unit_op import UnitOp

"""
Create a homogeneous property package containing only water
"""

def pp_hexane():
    """
    Create a property package
    """

    return PropertyPackage(phases=1, phase_names=['hexane'])

def pp_toluene():
    """
    Create a property package
    """

    return PropertyPackage(phases=1, phase_names=['toluene'])

def pp_water():
    """
    Create a property package
    """

    return PropertyPackage(phases=1, phase_names=['water'])

"""
Create a simple stream for model tests
"""

@pytest.fixture
def water_material_stream():

    """
    Create a homogeneous material_stream model
    """

    class material_stream(MaterialStream):

        def __init__(self, name, description, pp = pp_water):

            super().__init__(name, description, property_package=pp())

            self.mdot.setValue(100.)

            self.T.setValue(350.)

            self.P.setValue(101325.)

            self.property_package.resolve_mixture(T=self.T.value, P=self.P.value)

            self.H.setValue(self.property_package["*"].H)

    return material_stream

@pytest.fixture
def toluene_material_stream():

    """
    Create a homogeneous material_stream model
    """

    class material_stream(MaterialStream):

        def __init__(self, name, description, pp = pp_toluene):

            super().__init__(name, description, property_package=pp())

            self.mdot.setValue(100.)

            self.T.setValue(350.)

            self.P.setValue(101325)

            self.property_package.resolve_mixture(T=self.T.value, P=self.P.value)

            self.H.setValue(self.property_package["*"].H)

    return material_stream

@pytest.fixture
def water_toluene_material_stream():

    """
    Create a homogeneous material_stream model
    """

    pp_ = pp_water()

    pp_.addPropertyPackage(pp_toluene())

    class material_stream(MaterialStream):

        def __init__(self, name, description, pp=None):

            super().__init__(name, description, property_package=pp_)

            self.mdot.setValue(100.)

            self.T.setValue(350.)

            self.P.setValue(101325)

            self.H.setValue(0.)

            print("===> property_package = ",self.property_package)

    return material_stream

@pytest.fixture
def water_mixer_uop(water_material_stream):

    class mixer_model(Model):

        def __init__(self, name, description, pp = pp_water):

            super().__init__(name, description, property_package = pp())

            self.P_in = self.createVariable("P_in", Pa, "p_in", "Pressure from the totalized input stream", latex_text="{P}_{in}", is_exposed=True, type='input')

            self. T_in = self.createVariable("T_in", K, "T_in", "Temperature from the totalized input stream", latex_text="{T}_{in}", is_exposed=True, type='input')

            self.H_in = self.createVariable("H_in", J/mol, "H_in", "Enthalpy from the totalized input stream", latex_text="{H}_{in}", is_exposed=True, type='input')

            self.mdot_in = self.createVariable("mdot_in", kg/s, "mdot_in", "Mass flux from the totalized input stream", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')

            self.ndot_in = self.createVariable("ndot_in", mol/s, "ndot_in", "Molar flux from the totalized input stream", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')

    mixer_model =  mixer_model("mixer_model","Mixer model")

    class mixer_uop(UnitOp):

        def __init__(self, model):

            super().__init__(model = model)

            wms1 = water_material_stream("wms1","water material stream")
            wms1()

            wms2 = water_material_stream("wms2","water material stream")
            wms2()

            wms3 = water_material_stream("wms3","water material stream")
            wms3()

            self._setInlets([wms1,wms2], "in_L")

            #self._setOutlets(wms3,"out_L")

    water_mixer_uop = mixer_uop(mixer_model)

    return water_mixer_uop

@pytest.fixture
def water_mixer_uop_(water_material_stream):

    class mixer_model(Model):

        def __init__(self, name, description, pp = pp_water):

            super().__init__(name, description, property_package = pp())

            self.P_in = self.createVariable("P_in", Pa, "p_in", "Pressure from the totalized input stream", latex_text="{P}_{in}", is_exposed=True, type='input')

            self. T_in = self.createVariable("T_in", K, "T_in", "Temperature from the totalized input stream", latex_text="{T}_{in}", is_exposed=True, type='input')

            self.H_in = self.createVariable("H_in", J/mol, "H_in", "Enthalpy from the totalized input stream", latex_text="{H}_{in}", is_exposed=True, type='input')

            self.mdot_in = self.createVariable("mdot_in", kg/s, "mdot_in", "Mass flux from the totalized input stream", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')

            self.ndot_in = self.createVariable("ndot_in", mol/s, "ndot_in", "Molar flux from the totalized input stream", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')

    mixer_model =  mixer_model("mixer_model","Mixer model")

    class mixer_uop_(UnitOp):

        def __init__(self, model):

            super().__init__(model = model)

            wms1 = water_material_stream("wms1","water material stream")
            wms1()

            wms2 = water_material_stream("wms2","water material stream")
            wms2()

            wms3 = water_material_stream("wms3","water material stream")
            wms3()

            self._setInlets([wms1,wms2], "in_L")

            self._setOutlets(wms3,"out_L")

    water_mixer_uop = mixer_uop_(mixer_model)

    return water_mixer_uop

@pytest.fixture
def water_toluene_mixer_uop(water_material_stream, toluene_material_stream, water_toluene_material_stream):

    class mixer_model(Model):

        def __init__(self, name, description, pp = pp_water):

            super().__init__(name, description, property_package = pp())

            self.P_in = self.createVariable("P_in", Pa, "p_in", "Pressure from the totalized input stream", latex_text="{P}_{in}", is_exposed=True, type='input')

            self. T_in = self.createVariable("T_in", K, "T_in", "Temperature from the totalized input stream", latex_text="{T}_{in}", is_exposed=True, type='input')

            self.H_in = self.createVariable("H_in", J/mol, "H_in", "Enthalpy from the totalized input stream", latex_text="{H}_{in}", is_exposed=True, type='input')

            self.mdot_in = self.createVariable("mdot_in", kg/s, "mdot_in", "Mass flux from the totalized input stream", latex_text="\\dot{m}_{in}", is_exposed=True, type='input')

            self.ndot_in = self.createVariable("ndot_in", mol/s, "ndot_in", "Molar flux from the totalized input stream", latex_text="\\dot{n}_{in}", is_exposed=True, type='input')

    mixer_model =  mixer_model("mixer_model","Mixer model")

    class mixer_uop(UnitOp):

        def __init__(self, model):

            super().__init__(model = model)

            wms1 = water_material_stream("wms1","water material stream")
            wms1()

            tms1 = toluene_material_stream("tms1","toluene material stream")
            tms1()

            wtms = water_toluene_material_stream("wtms", "water and toluene material stream")
            wtms()

            self._setInlets([wms1,tms1], "in_L")

            #self._setOutlets(wtms, "out_L")

    water_toluene_mixer_uop = mixer_uop(mixer_model)

    return water_toluene_mixer_uop

def fftest_1phase_model_report(water_mixer_uop):

        mixer_uop = water_mixer_uop

        mixer_uop.resolve()

        mixer_uop.model._infoModelReport_()

        #print("UnitOp __dict__: ",mixer_uop.__dict__)

        #print("Model.parameters[...]__dict__: ",["\n "+p.name+"__dict__ :"+repr(p.__dict__) for p in list(mixer_uop.model.parameters.values())])

        #print("Model pp: ",mixer_uop.property_package.__dict__)

        assert mixer_uop.ports["inlets"]["in_L"][0].z_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][1].z_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][0].w_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][1].w_water.value == 1.

        assert 1 == 2

def fftest_1phase_model_reportII(water_mixer_uop_):

        mixer_uop = water_mixer_uop_

        mixer_uop.resolve()

        mixer_uop.model._infoModelReport_()

        #print("UnitOp __dict__: ",mixer_uop.__dict__)

        #print("Model.parameters[...]__dict__: ",["\n "+p.name+"__dict__ :"+repr(p.__dict__) for p in list(mixer_uop.model.parameters.values())])

        #print("Model pp: ",mixer_uop.property_package.__dict__)

        mixer_uop.ports["outlets"]["out_L"][0]._infoModelReport_()


        assert mixer_uop.ports["inlets"]["in_L"][0].z_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][1].z_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][0].w_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][1].w_water.value == 1.

        assert 1 == 2

def fftest_2phase_model_report(water_toluene_mixer_uop):

        mixer_uop = water_toluene_mixer_uop

        mixer_uop.resolve()

        mixer_uop.model._infoModelReport_()

        #print("UnitOp model __dict__: ",mixer_uop.model.__dict__)

        #print("Model.parameters[...]__dict__: ",["\n "+p.name+"__dict__ :"+repr(p.__dict__) for p in list(mixer_uop.model.parameters.values())])

        print("Model pp: ",mixer_uop.property_package.__dict__)

        assert mixer_uop.ports["inlets"]["in_L"][0].z_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][1].z_toluene.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][0].w_water.value == 1.
        assert mixer_uop.ports["inlets"]["in_L"][1].w_toluene.value == 1.

        assert 1 == 2