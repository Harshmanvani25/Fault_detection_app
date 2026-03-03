# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:25:23 2026

@author: Harsh
"""

# ui/dashboard_controls.py

import customtkinter as ctk


class ControlPanel:
    def disable(self):
        self.local_radio.configure(state="disabled")
        self.server_radio.configure(state="disabled")
        self.single_radio.configure(state="disabled")
        self.batch_radio.configure(state="disabled")
        self.shot_entry.configure(state="disabled")
        self.channel_entry.configure(state="disabled")
    
    def enable(self):
        self.local_radio.configure(state="normal")
        self.server_radio.configure(state="normal")
        self.single_radio.configure(state="normal")
        self.batch_radio.configure(state="normal")
        self.shot_entry.configure(state="normal")
        self.channel_entry.configure(state="normal")
    def __init__(self, parent):

        self.mode_var = ctk.StringVar(value="local")
        self.local_process_mode = ctk.StringVar(value="single")

        # =========================
        # Data Source Label
        # =========================

        title = ctk.CTkLabel(
            parent,
            text="Data Source",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(10, 5))

        # =========================
        # Mode Radios
        # =========================

        self.local_radio = ctk.CTkRadioButton(
            parent,
            text="Select Local File",
            variable=self.mode_var,
            value="local",
            command=self._toggle_mode
        )
        self.local_radio.pack(pady=5)

        process_mode_frame = ctk.CTkFrame(parent, fg_color="transparent")
        process_mode_frame.pack(pady=(5, 10))

        self.single_radio = ctk.CTkRadioButton(
            process_mode_frame,
            text="Single File",
            variable=self.local_process_mode,
            value="single"
        )
        self.single_radio.grid(row=0, column=0, padx=10)

        self.batch_radio = ctk.CTkRadioButton(
            process_mode_frame,
            text="Batch Files",
            variable=self.local_process_mode,
            value="batch"
        )
        self.batch_radio.grid(row=0, column=1, padx=10)

        self.server_radio = ctk.CTkRadioButton(
            parent,
            text="Fetch From Server",
            variable=self.mode_var,
            value="server",
            command=self._toggle_mode
        )
        self.server_radio.pack(pady=5)

        # =========================
        # Shot Input
        # =========================

        self.shot_label = ctk.CTkLabel(
            parent,
            text="Shot Number (empty = latest)"
        )
        self.shot_label.pack(pady=(15, 5))

        self.shot_entry = ctk.CTkEntry(parent, width=350, height=35)
        self.shot_entry.pack()
        self.shot_entry.configure(state="disabled")

        # =========================
        # Channel Input
        # =========================

        self.channel_label = ctk.CTkLabel(
            parent,
            text="Channel Numbers (space separated)"
        )
        self.channel_label.pack(pady=(15, 5))

        self.channel_entry = ctk.CTkEntry(parent, width=350, height=35)
        self.channel_entry.pack()
        self.channel_entry.configure(state="disabled")

    # ==================================================
    # INTERNAL TOGGLE
    # ==================================================

    def _toggle_mode(self):

        if self.mode_var.get() == "server":

            # Force single mode
            self.local_process_mode.set("single")
        
            self.shot_entry.configure(state="normal")
            self.channel_entry.configure(state="normal")
        
            # Disable local options
            self.single_radio.configure(state="disabled")
            self.batch_radio.configure(state="disabled")

        else:

            self.shot_entry.delete(0, "end")
            self.channel_entry.delete(0, "end")

            self.shot_entry.configure(state="disabled")
            self.channel_entry.configure(state="disabled")

            self.single_radio.configure(state="normal")
            self.batch_radio.configure(state="normal")

    # ==================================================
    # PUBLIC API (Dashboard Uses Only These)
    # ==================================================

    def is_server_mode(self):
        return self.mode_var.get() == "server"

    def is_batch_mode(self):
        return self.local_process_mode.get() == "batch"

    def get_inputs(self):
        """
        Returns:
            shot (str or None)
            channels (list[int])
        """

        if not self.is_server_mode():
            return None, []

        shot_text = self.shot_entry.get().strip()
        channel_text = self.channel_entry.get().strip()

        shot = shot_text if shot_text else None

        channels = []
        if channel_text:
            for ch in channel_text.split():
                if ch.isdigit():
                    channels.append(int(ch))

        return shot, channels