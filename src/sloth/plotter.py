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

    def setSimulation(self, simulation):

        """
        Set the simulation for the current Plotter object.

        :param Simulation simulation:
            Simulation for which the plotting activity is performed
        """

        self.simulation = simulation

    def plotSimpleLines(self, x_data, y_data, set_style='darkgrid', x_label='time', y_label='output', labels=None, linewidth=2.5, markers=None, grid=False, save_file=None, show_plot=True, data=None, legend=False):

        #TODO: Provide functionality for passing a dataset object (DataFrame) for which the name of the columns will be passed as x_data and y_data arguments

        if markers is not None:

            for i in range(len(x_data)):
                for j in range(len(y_data)):
                    
                    plt.plot(x_data[i].reshape(-1), 
                             y_data[j].reshape(-1), 
                             marker=markers[j], 
                             label=labels[j], 
                             linewidth=linewidth
                        )

        else:

            for i in range(len(x_data)):
                for j in range(len(y_data)):
                    
                    plt.plot(x_data[i].reshape(-1), 
                             y_data[j].reshape(-1), 
                             label=labels[j], 
                             linewidth=linewidth
                        )

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

    def DEPRECATED_plotSimpleLines(self, data, set_style='darkgrid', x_label='time', y_label='output', legend_for_colors=None, legend_for_styles=None, linewidth=2.5, draw_markers=False, grid=False, save_file=None, show_plot=True):

        """
        :param str set_style:

        :param DataFrame data:
            Dataframe to retreve information

        :param list(float), str x_data:

        :param list(float), list(str y_data):

        :param str x_label:

        :param list(str) y_label:

        :param str save_file:

        :param bool show_plot:
        """
    
        sns.set(style=set_style)

        # Load an example dataset with long-form data

        # Plot the responses for different events and regions
        sns.lineplot(data=data, palette="tab10", linewidth=linewidth, hue=legend_for_colors, style=legend_for_styles)

        if show_plot is not False:

            plt.show()
        
        if save_file is not None:

            plt.savefig(save_file,  bbox_inches="tight")

        plt.clf()