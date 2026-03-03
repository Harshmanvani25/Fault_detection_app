# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:27:14 2026

@author: Harsh
"""

# ui/dashboard_results.py

import customtkinter as ctk
import time
from ui.history_manager import open_history_window
# from ui.plotter import plot_signal
from ui.plot_window import PlotWindow

class ResultsPanel:

    def __init__(self, parent, root, accent="#3A86FF"):

        self.root = root
        self.accent = accent
        self.history_data = []

        self.card = ctk.CTkFrame(parent, corner_radius=15)
        self.card.pack(fill="x", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            self.card,
            text="Diagnosis Result",
            font=("Arial", 18, "bold"),
            text_color=self.accent
        )
        title.pack(pady=(15, 5))

        self.active_shot_label = ctk.CTkLabel(
            self.card,
            text="Active Shot: -",
            font=("Arial", 14, "bold"),
            text_color=self.accent
        )
        self.active_shot_label.pack(pady=(0, 5))

        self.result_label = ctk.CTkLabel(
            self.card,
            text="Result: -",
            font=("Arial", 22, "bold")
        )
        self.result_label.pack(pady=5)

        self.timer_label = ctk.CTkLabel(
            self.card,
            text="Execution Time: -",
            font=("Arial", 12)
        )
        self.timer_label.pack(pady=(0, 10))

        action_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        action_frame.pack(pady=(5, 15))

        self.history_button = ctk.CTkButton(
            action_frame,
            text="View History",
            width=150,
            command=self._open_history
        )
        self.history_button.grid(row=0, column=0, padx=10)
        self.plot_button = ctk.CTkButton(
            action_frame,
            text="Plot Signal",
            width=150,
            command=self.handle_plot_signal
        )
        self.plot_button.grid(row=0, column=1, padx=10)

    def handle_plot_signal(self):

        if not hasattr(self, "shot_number"):
            return
    
        if not hasattr(self, "time_array") or not hasattr(self, "signal_array"):
            return
    
        self.plot_window = PlotWindow(
            shot=self.shot_number,
            diagnostic="HAlpha",
            time_data=self.time_array,
            signal_data=self.signal_array
        )
    
        self.plot_window.show()

    # ==================================================
    # PUBLIC API (Dashboard Uses Only These)
    # ==================================================

    def set_active_shot(self, shot):
        self.active_shot_label.configure(
            text=f"Active Shot: {shot}",
            text_color="#f39c12"
        )

    def set_result(self, shot, fault, exec_time):

        if str(fault).upper() == "NORMAL":
            self.result_label.configure(text=f"Result: {fault}", text_color="#2ecc71")
        else:
            self.result_label.configure(text=f"Result: {fault}", text_color="#e74c3c")

        self.timer_label.configure(text=f"Execution Time: {exec_time:.2f} sec")

        self.history_data.append({
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "shot": shot,
            "result": fault
        })
    def store_signal_data(self, shot, time_array, signal_array):
        self.shot_number = shot
        self.time_array = time_array
        self.signal_array = signal_array
    def reset(self):
        self.result_label.configure(text="Result: -")
        self.timer_label.configure(text="Execution Time: -")
        self.active_shot_label.configure(text="Active Shot: -")
    
    # ==================================================
    # INTERNAL
    # ==================================================

    def _open_history(self):
        open_history_window(self.root, self.history_data, self.accent)