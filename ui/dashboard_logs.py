# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:29:47 2026

@author: Harsh
"""

# ui/dashboard_logs.py

import customtkinter as ctk
import time


class LogsPanel:

    def __init__(self, parent, accent="#3A86FF"):

        self.frame = ctk.CTkFrame(parent, corner_radius=15)
        self.frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="System Logs",
            font=("Arial", 16, "bold"),
            text_color=accent
        )
        title.pack(side="left", padx=10, pady=10)

        clear_button = ctk.CTkButton(
            header,
            text="Clear Logs",
            width=100,
            fg_color="#555555",
            hover_color="#444444",
            command=self.clear
        )
        clear_button.pack(side="right", padx=10)

        self.log_box = ctk.CTkTextbox(
            self.frame,
            fg_color=("#F8F8F8", "#121212")
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_box.configure(state="disabled")

    # ==================================================
    # PUBLIC API
    # ==================================================

    def log(self, level, message):

        color = {
            "INFO": "#2ecc71",
            "WARNING": "#f1c40f",
            "ERROR": "#e74c3c"
        }.get(level, "white")
    
        self.log_box.configure(state="normal")
    
        self.log_box.insert("end", f"[{level}] {message}\n")
    
        self.log_box.tag_add(level, "end-2l", "end-1l")
        self.log_box.tag_config(level, foreground=color)
    
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def clear(self):

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")