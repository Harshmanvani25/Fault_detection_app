# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:26:51 2026

@author: Harsh
"""

# ui/plot_window.py

import matplotlib.pyplot as plt

class PlotWindow:

    def __init__(self, shot, diagnostic, time_data, signal_data):
        self.shot = shot
        self.diagnostic = diagnostic
        self.time_data = time_data
        self.signal_data = signal_data

        self._plot()

    def _plot(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.time_data, self.signal_data)
        plt.title(f"Shot {self.shot} - {self.diagnostic}")
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()