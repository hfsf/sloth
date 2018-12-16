"""
Defines Plotter class
"""
from .core.error_definitions import *
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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

    def setSimulation(self, simulation):

        """
        Set the simulation for the current Plotter object.

        :param Simulation simulation:
            Simulation for which the plotting activity is performed
        """

        self.simulation = simulation

    def plotLines(self, x_data, y_data, set_style='darkgrid', x_label='time', y_label='output', linewidth=2.5, draw_markers=False, grid=False, save_file=None, show_plot=True, data=None):

        if data is not None and isinstance(x_data, str) and isinstance(y_data, str):

            x_data = data[x_data]

            y_data = data[y_data]

        else:

            raise Exception("Arguments (x_data and y_data) must be a numeric array or the name of the subset of the dataset (data)")

        plt.xlabel(x_label)

        plt.ylabel(y_label)

        plt.plot(x_data, y_data, linewidth=linewidth)

        plt.grid(grid)

        if save_file is not None:

            plt.savefig(save_file,  bbox_inches="tight")

        if show_plot is not False:

            plt.show()

        plt.clf()





