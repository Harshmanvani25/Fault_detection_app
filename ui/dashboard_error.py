# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 11:29:37 2026

@author: Harsh
"""

# ui/dashboard_error.py

import customtkinter as ctk


class ErrorPanel:

    def __init__(self, parent):

        self.card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=("#ffe6e6", "#3a0d0d")
        )

        self.label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 14, "bold"),
            text_color="#e74c3c",
            wraplength=400
        )

        self.label.pack(padx=15, pady=10)

        self.hide()

    def show(self, message):

        self.label.configure(text=f"⚠ {message}")
        self.card.pack(fill="x", padx=20, pady=(0, 10))

    def hide(self):

        self.card.pack_forget()