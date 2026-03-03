# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 15:55:47 2026

@author: Harsh
"""

# ui/plotter.py
import matplotlib
# matplotlib.use("TkAgg")

def plot_signal():
    import matplotlib.pyplot as plt
    import numpy as np

    # Dummy signal for testing
    x = np.linspace(0, 10, 1000)
    y = np.sin(x)

    plt.figure()
    plt.plot(x, y)
    plt.title("Signal Plot")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()