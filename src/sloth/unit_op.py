# unit_op.py

"""
Define a generic Unit_op with support for ports
"""

from .core.error_definitions import *
from .core.equation_operators import *
from .core.template_units import *
from .core.domain import *

from .unit_op_library import MaterialStream

class UnitOp:

    """
    Defines the UnitOp class, that holds the capabilities for: acessing ports (inputs, outputs) from the UnitOp objects; Predefine streams for input and output, allowing to the port to be passed directly to other UnitOps
    """

    def __init__(self, n_inputs=0, n_outputs=0, model=None, ports={'inlets':{},'outlets':{}}):

        self.n_inputs = n_inputs

        self.n_outputs = n_outputs

        self.model = model

        self.ports = ports

        self.property_package = model.property_package

        self._intlets = []

        self._outlets = []

    def __getitem__(self, id):

        return self.ports[id]

    def _totalizeInlets(self):

        """
        Function for totalization of inlets, assuming that all those are MaterialStreams from the UnitOp library
        """

        #Creation of variables (P_in, T_in, mdot_in, ndot_in, H_in) if they were not defined previously for the model

        if not hasattr(self.model, 'P_in'):

            self.model.P_in = self.model.createVariable("P_in", Pa, "p_in", "Pressure from the totalized input stream for "+self.model.name, latex_text="{P}_{in}", is_exposed=True, type='input')

        if not hasattr(self.model, 'T_in'):

            self.model.T_in = self.model.createVariable("T_in", K, "T_in", "Temperature from the totalized input stream for "+self.model.name, latex_text="{T}_{in}", is_exposed=True, type='input')

        if not hasattr(self.model, 'mdot_in'):

            self.model.mdot_in = self.model.createVariable("mdot_in", kg/s, "mdot_in", "Mass flux from the totalized input stream for "+self.model.name, latex_text="\\dot{m}_{in}", is_exposed=True, type='input')

        if not hasattr(self.model, 'ndot_in'):

            self.model.ndot_in = self.model.createVariable("ndot_in", mol/s, "ndot_in", "Molar flux from the totalized input stream for "+self.model.name, latex_text="\\dot{n}_{in}", is_exposed=True, type='input')

        if not hasattr(self.model, 'H_in'):

            self.model.H_in = self.model.createVariable("H_in", J/mol, "H_in", "Molar enthalpy for the totalized input stream for "+self.model.name, latex_text="{H}_{in}", is_exposed=True, type='input')

        #Incorporate the inlets for further reference to its parameters
        try:

            _ = [self.model.incorporateFromExternalModel(stream, incorporate_equations=False, rewrite_name=False) for stream in self._inlets]

        except:

            raise Exception("Inlets were not declared for current UnitOp object.")

        #Now, create the equations for the totalization

        if len(self.ports['inlets']) > 0 :

            try:

                P_from_inputs = [stream.P() for stream in self._inlets]

                _ = [self.model.createEquation("eq_P_"+stream.P.name, "", stream.P() - stream.P.value) for stream in self._inlets]

            except:

                raise AbsentRequiredObjectError("(list of inlet streams with 'P' object defined)")

            try:

                T_from_inputs = [stream.T() for stream in self._inlets]

                _ = [self.model.createEquation("eq_T_"+stream.T.name, "", stream.T() - stream.T.value) for stream in self._inlets]

            except:

                raise AbsentRequiredObjectError("(list of inlet streams with 'T' object defined)")

            try:

                mdot_from_inputs = [stream.mdot() for stream in self._inlets]

                _ = [self.model.createEquation("eq_mdot_"+stream.mdot.name, "", stream.mdot() - stream.mdot.value) for stream in self._inlets]

            except:

                raise AbsentRequiredObjectError("(list of inlet streams with 'mdot' object defined)")

            try:

                ndot_from_inputs = [stream.ndot() for stream in self._inlets]

                _ = [self.model.createEquation("eq_ndot_"+stream.mdot.name, "", stream.ndot() - stream.ndot.value) for stream in self._inlets]

            except:

                raise AbsentRequiredObjectError("(list of inlet streams with 'ndot' object defined)")


            #Pressure totalization

            self.model.tot_P = self.model.createEquation("totalization_P", "Totalization eq. for pressure for "+self.model.name, self.model.P_in() - Min(*P_from_inputs))

            #Temperature totalization

            self.model.tot_T = self.model.createEquation("totalization_T", "Totalization eq. for temperature for "+self.model.name, self.model.T_in() - Min(*T_from_inputs))

            #Mass flux totalization
            #print("\n\n==>model.__dict__", self.model.__dict__)
            #print("\n\n==>model.P_in(): ", self.model.P_in().__dict__)
            #print("\n\n==>model.ndot_in(): ", self.model.ndot_in().__dict__)
            #print("\n\n==>model.mdot_in(): ", self.model.mdot_in().__dict__)

            self.model.tot_mdot = self.model.createEquation("totalization_mdot", "Totalization eq. for mass flux for "+self.model.name, self.model.mdot_in() - Sum(*mdot_from_inputs))

            #Molar flux totalization

            self.model.tot_ndot = self.model.createEquation("totalization_ndot", "Totalization eq. for molar flux for "+self.model.name, self.model.ndot_in() - Sum(*ndot_from_inputs))

            #Create the new property package combining the ones from the input

            mdots_ = []

            ndots_ = []

            #self.model.property_package = self.model._inlets[0].property_package

            #mdots_.append(self.model._inlets[0].mdot.value)

            #ndots_.append(self.model._inlets[0].ndot.value)

            #print("\n\nmodel pp: ",self.model.property_package.__dict__)

            #print("\n\nself.model ports: ",self.ports)

            #print("\n\nself.model inlets: ",self.model._inlets)

            # _ = [print("\n\t",stream.property_package.__dict__) for stream in self.model._inlets]

            for stream in self._inlets:

                #print("\n\nstream",stream.name,"property_package: ",stream.property_package.__dict__)

                self.model.property_package.addPropertyPackage(stream.property_package)

            for i, phase_i in enumerate(self.model.property_package.phase_names):

                exec("self.model.z_{} = self.model.createVariable('z_{}',dimless,'Molar fraction for {} phase for {}', latex_text='z_{}', is_exposed=True, type='output')".format(phase_i, phase_i, phase_i, self.model.name, phase_i))

                exec("self.model.w_{} = self.model.createVariable('w_{}',dimless,'Mass fraction for {} phase for {}', latex_text='z_{}', is_exposed=True, type='output')".format(phase_i, phase_i, phase_i, self.model.name, phase_i))

            zs_ = []

            ws_ = []

            for phase_i in self.model.property_package.phase_names:

                mdot_phase_i = 0.

                ndot_phase_i = 0.

                all_mdot = 0.

                all_ndot = 0.

                for stream in self._inlets:

                    all_mdot += stream.mdot.value

                    all_ndot += stream.ndot.value

                    for stream_phase_i in stream.property_package.phase_names:

                        if stream_phase_i == phase_i:

                            mdot_phase_i += eval("stream.mdot()*stream.w_{}()".format(stream_phase_i))

                            ndot_phase_i += eval("stream.ndot()*stream.z_{}()".format(stream_phase_i))

                #As the symbolic_object of an Parameter is in fact its value, the value from the EquationNode object could be extracted used this attribute

                ws_.append(mdot_phase_i.symbolic_object/all_mdot)

                zs_.append(ndot_phase_i.symbolic_object/all_ndot)

                exec("self.model.molar_conservation_phase_{} = self.model.createEquation('molar_conservation_phase_{}_inlet','Molar conservation for phase {} from inlets',self.model.z_{}()*self.model.ndot_in() - ndot_phase_i)".format(phase_i, phase_i, phase_i, phase_i))

                exec("self.model.mass_conservation_phase_{} = self.model.createEquation('mass_conservation_phase_{}_inlet','Mass conservation for phase {} from inlets',self.model.w_{}()*self.model.mdot_in() - mdot_phase_i)".format(phase_i, phase_i, phase_i, phase_i))

            """
            for stream in self._inlets:

                mdots_.append(stream.mdot.value)

                ndots_.append(stream.ndot.value)

            if all(mdots_i is None for mdots_i in mdots_):

                mdots_ = None

            if all(ndots_i is None for ndots_i in ndots_):

                ndots_ = None
            """

            T_mix_ = min([stream.T.value for stream in self._inlets])

            P_mix_ = min([stream.P.value for stream in self._inlets])

            #print("\n\n=>mdots = ",mdots_)

            #print("\n\n=>ndots = ",ndots_)

            #If needed, resolve the mixture

            #print("\n\n\t\t----> I have calculated that ws = ", ws_, "and zs = ", zs_)

            self.model.property_package.resolve_mixture(ws=ws_, zs=zs_, T=T_mix_, P=P_mix_)

            self.property_package = self.model.property_package

    def _totalizeOutlets(self):

        """
        Generic function for totalization of outlets, assuming that all those are MaterialStreams from the UnitOp library
        """

        if len(self._outlets) > 1:

            #Should divide mass flow etc

            pass

        if len(self._outlets) == 1:

            #Will conserve all variables directly

            if isinstance(self._outlets[0], MaterialStream):

                self.model.incorporateFromExternalModel(self._outlets[0], incorporate_equations=False, rewrite_name=False)

                self.model.createEquation("tot_P_out", "Tot. of pressure for outlet stream "+self._outlets[0].name, self._outlets[0].P() - self.model.P_in())

                self.model.createEquation("tot_T_out", "Tot. of temperature for outlet stream "+self._outlets[0].name, self._outlets[0].T() - self.model.T_in())

                self.model.createEquation("tot_H_out", "Tot. of molar enthalpy for outlet stream "+self._outlets[0].name, self._outlets[0].H() - self.model.H_in())

                self.model.createEquation("tot_ndot_out", "Tot. of molar flux for outlet stream "+self._outlets[0].name, self._outlets[0].ndot() - self.model.ndot_in())

                self.model.createEquation("tot_mdot_out", "Tot. of mass flux for outlet stream "+self._outlets[0].name, self._outlets[0].mdot() - self.model.mdot_in())

                for phase_i in self.model.property_package.phase_names:

                    exec("self.model.createEquation('molar_conservation_phase_{}_outlet', 'Molar conservation for phase {} for outlet', self._outlets[0].z_{}()-self.model.z_{}())".format(phase_i, phase_i, phase_i, phase_i))

                    exec("self.model.createEquation('mass_conservation_phase_{}_outlet', 'Mass conservation for phase {} for outlet', self._outlets[0].w_{}()-self.model.w_{}())".format(phase_i, phase_i, phase_i, phase_i))

                    exec("self._outlets[0].createEquation('molar_conservation_phase_{}_outlet', 'Molar conservation for phase {} for outlet', self._outlets[0].z_{}()-self.model.z_{}())".format(phase_i, phase_i, phase_i, phase_i))

                    exec("self._outlets[0].createEquation('mass_conservation_phase_{}_outlet', 'Mass conservation for phase {}for outlet', self._outlets[0].w_{}()-self.model.w_{}())".format(phase_i, phase_i, phase_i, phase_i))

                self._outlets[0].property_package = self.model.property_package

            else:

                raise UnexpectedValueError("MaterialStream", type(self._outlets[0]))

    def resolve(self):

        self.model.DeclareConstants()

        self.model.DeclareParameters()

        self.model.DeclareVariables()

        if len(self._inlets)>0:

            self._totalizeInlets()

        if len(self._outlets)>0:

            self._totalizeOutlets()

        self.model.DeclareEquations()

        if len(self.model.variables) == 0 and self.model.ignore_variable_warning is False:

            print("Warning: No variables were declared.")

        if len(self.model.equations) == 0 and self.model.ignore_equation_warning is False:

            print("Warning: No equations were declared.")

    def _setInlets(self, inlets, inlet_name='in'):

        '''
        try:
            _inlets = self.ports['inlets'][inlet_name]
        except:
            _inlets = []
        '''

        _inlets = []

        if isinstance(inlets, list):

            _ = [_inlets.append(i) for i in inlets]

            self.n_inputs += len(inlets)

        else:

            _inlets.append(inlets)

            self.n_inputs += 1

        self.ports['inlets'][inlet_name] = _inlets

        self._inlets = _inlets

        #self.ports['inlets'].update({inlet_name: _inlets})

        #_ = [self._inlets.extend(self.ports['inlets'][in_]) for in_ in list(self.ports['inlets'].keys())]

    def _setOutlets(self, outlets, outlet_name='out'):

        _outlets = []

        if isinstance(outlets, list):

            _ = [_outlets.append(i) for i in outlets]

            self.n_outputs += len(outlets)

        else:

            _outlets.append(outlets)

            self.n_outputs += 1

        self.ports['outlets'][outlet_name] = _outlets

        self._outlets = _outlets