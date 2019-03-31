"""
Defines Plotter class
"""
from .core.error_definitions import *
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Plotter:

    """
    Defines Plotter class. Responsible for plotting results into 2D or 3D graphics
    """

    def __init__(self, simulation=None):

        """
        Instantiate Plotter

        :ivar Simulation simulation:
            Simulation for which the plotting activity is performed. Defaults to None
        """

        self.simulation = simulation

        self.plots = {}

    def _setSimulation(self, simulation):

        """
        Set the simulation for the current Plotter object.

        :param Simulation simulation:
            Simulation for which the plotting activity is performed
        """

        self.simulation = simulation

    def plotTimeSeries(self, x_data, y_data, set_style='darkgrid', x_label='time', y_label='output', labels=None, linewidth=2.5, markers=None, grid=False, save_file=None, show_plot=True, data=None, legend=False):

        #y_data=sim.domain[('t_M1',['Preys(u)','Predators(v)'])],

        if isinstance(x_data, tuple) and data is not None:

            try:
                x_data = data[x_data]

            except:

                raise ValueError("Improper value for x_data or y_data. \n\tThey should be either a direct reference for simulation data or reference for domain values.")

        if isinstance(y_data, tuple) and data is not None:

            try:
                y_data = data[y_data]

            except:


                raise ValueError("Improper value for x_data or y_data. \n\tThey should be either a direct reference for simulation data or reference for domain values.")

        if markers is not None:

            for i in range(len(x_data)):
                for j in range(len(y_data)):

                    plt.plot(x_data[i].reshape(-1),
                             y_data[j].reshape(-1),
                             marker=markers[j],
                             label=labels[j],
                             linewidth=linewidth
                        )


                    plt.xlim(min(x_data[i].reshape(-1)),max(x_data[i].reshape(-1)))

        else:

            for i in range(len(x_data)):
                for j in range(len(y_data)):

                    plt.plot(x_data[i].reshape(-1),
                             y_data[j].reshape(-1),
                             label=labels[j],
                             linewidth=linewidth
                        )

                    plt.xlim(min(x_data[i].reshape(-1)),max(x_data[i].reshape(-1)))
        plt.xlabel(x_label)

        plt.ylabel(y_label)

        plt.grid(grid)

        if legend is not False:

            plt.legend()

        if save_file is not None:

            plt.savefig(save_file,  bbox_inches="tight")

        if show_plot is not False:

            plt.show()

        plt.clf()
