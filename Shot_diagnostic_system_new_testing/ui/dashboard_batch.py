# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:28:23 2026

@author: Harsh
"""

# ui/dashboard_batch.py

import customtkinter as ctk


class BatchPanel:
    def clear(self):
        self.info_label.configure(text="No batch running")
        self.total = 0
        self.normal = 0
        self.fault = 0

    def __init__(self, parent, accent="#3A86FF"):

        self.accent = accent

        self.total = 0
        self.normal = 0
        self.fault = 0

        self.card = ctk.CTkFrame(parent, corner_radius=15)
        self.card.pack(fill="x", padx=20, pady=(0, 10))

        title = ctk.CTkLabel(
            self.card,
            text="Batch Summary",
            font=("Arial", 16, "bold"),
            text_color=self.accent
        )
        title.pack(pady=(10, 5))

        self.info_label = ctk.CTkLabel(
            self.card,
            text="No batch running",
            font=("Arial", 13)
        )
        self.info_label.pack(pady=(0, 10))

    # ==================================================
    # PUBLIC API
    # ==================================================

    def reset(self, total_files):

        self.total = total_files
        self.normal = 0
        self.fault = 0

        self.info_label.configure(text="Batch Running...")

    def update_result(self, fault):

        if str(fault).upper() == "NORMAL":
            self.normal += 1
        else:
            self.fault += 1

    def complete(self):

        self.info_label.configure(
            text=f"Total: {self.total} | Normal: {self.normal} | Fault: {self.fault}"
        )