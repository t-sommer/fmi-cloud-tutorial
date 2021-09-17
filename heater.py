""" Example of a library to be used in the Jupyter Notebook """

from fmpy import *


def simulate_heater(TAmb=293.15, stop_time=100):
    """ Helper function with a fixed set of parameters """

    result = simulate_fmu('Heater.fmu', stop_time=stop_time, start_values={'TAmb': TAmb})

    plot_result(result)
