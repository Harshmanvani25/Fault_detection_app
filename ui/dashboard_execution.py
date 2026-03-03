# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:26:15 2026

@author: Harsh
"""

# ui/dashboard_execution.py

import customtkinter as ctk
from tkinter import filedialog
import os
from services.mount_manager import is_mounted
from tkinter import messagebox

class ExecutionPanel:

    def __init__(self, parent, process_manager, controls, batch_panel, results_panel, error_panel, log_callback):
        self.results = results_panel
        self.parent_batch = batch_panel
        self.process_manager = process_manager
        self.controls = controls
        self.log = log_callback
        self.result_queue = None

        self.run_button = ctk.CTkButton(
            parent,
            text="Run Diagnosis",
            height=55,
            font=("Arial", 18, "bold"),
            command=self._on_run
        )
        self.run_button.pack(pady=20)

        self.stop_button = ctk.CTkButton(
            parent,
            text="Stop Execution",
            height=45,
            fg_color="#c0392b",
            hover_color="#992d22",
            state="disabled",
            command=self._on_stop
        )
        self.stop_button.pack(pady=5)
        self.progress = ctk.CTkProgressBar(parent, width=300)
        self.progress.set(0)
        self.progress.pack(pady=10)
        
        self.stage_label = ctk.CTkLabel(
            parent,
            text="Idle",
            font=("Arial", 14)
        )
        self.stage_label.pack(pady=5)
        self.error_panel = error_panel
    # =============================================
    # RUN
    # =============================================

    def _on_run(self):
    
        # Prevent multiple workers
        if self.result_queue is not None:
            return
    
        # -------- VALIDATION FIRST --------
    
        if self.controls.is_server_mode():
            if not is_mounted():
                messagebox.showerror(
                    "Server Not Connected",
                    "Server is not connected.\nPlease connect to the server before running."
                )
    
                # 🔥 Ensure UI is normal
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.controls.enable()
                return
    
        # ----------------------------------
    
        # Only now change UI state
        self.error_panel.hide()
    
        self.results.result_label.configure(
            text="Processing...",
            text_color="#f39c12"
        )
        self.results.timer_label.configure(text="Execution Time: -")
    
        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.controls.disable()
        self.log("INFO", "Processing started...")
        # ---------------- Local Mode ----------------
        if not self.controls.is_server_mode():
            
            if self.controls.is_batch_mode():
                file_paths = filedialog.askopenfilenames(
                    filetypes=[("Excel Files", "*.xlsx")]
                )
            else:
                path = filedialog.askopenfilename(
                    filetypes=[("Excel Files", "*.xlsx")]
                )
                file_paths = [path] if path else []

            if not file_paths:
                self.controls.enable()
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                return

            self.log("INFO", f"Selected {len(file_paths)} file(s)")
            first_file = file_paths[0]
            shot = os.path.basename(first_file).split(".")[0]
            self.results.set_active_shot(shot)
            self.parent_batch.reset(len(file_paths))
            self.result_queue = self.process_manager.start_worker("local", file_paths)
            self.log("INFO", "Worker started.")

        # ---------------- Server Mode ----------------
        else:
            
            shot, channels = self.controls.get_inputs()

            # ---------------- VALIDATION ----------------
            
            # Channels must exist
            if not channels:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter at least one channel number."
                )
                self.controls.enable()
                self.run_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                return
            
            # Shot validation (optional field)
            if shot:
                if not shot.isdigit():
                    messagebox.showerror(
                        "Invalid Input",
                        "Shot number must contain digits only."
                    )
                    self.controls.enable()
                    self.run_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    return
            
            # Channel validation
            for ch in channels:
                if not str(ch).isdigit():
                    messagebox.showerror(
                        "Invalid Input",
                        "Channel numbers must contain digits only."
                    )
                    self.controls.enable()
                    self.run_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    return
            
            # --------------------------------------------on.configure(state="disabled")
                            
            
            if not shot:
                shot_value = None   # backend will auto-fetch latest
            else:
                shot_value = int(shot)
            
            payload = {
                "shot": shot_value,
                "channels": channels
            }
            
            self.log("INFO", f"Fetching shot {shot} from server")
            
            self.parent_batch.reset(1)
            
            self.result_queue = self.process_manager.start_worker("server", payload)
    # =============================================
    # STOP
    # =============================================

    def _on_stop(self):
        self.error_panel.hide()
        # Stop worker first
        self.process_manager.stop_worker()
    
        # Reset execution UI
        self.stage_label.configure(text="Idle")
        self.progress.set(0)
    
        # Reset result panel
        self.results.set_active_shot("-")
        self.results.result_label.configure(text="Result: -")
        self.results.timer_label.configure(text="Processing Time: -")
    
        # Reset batch panel
        self.parent_batch.clear()
    
        # Re-enable controls
        self.controls.enable()
    
        self.run_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.result_queue = None
    
        self.log("WARNING", "Execution stopped.")
    # =============================================
    # PUBLIC
    # =============================================

    def get_queue(self):
        return self.result_queue

    def enable_run(self):
        self.controls.enable()
        self.result_queue = None
        self.stage_label.configure(text="Idle")
        self.progress.set(0)
        self.run_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
    def set_progress(self, percent):
        self.progress.set(percent / 100)
    
    def set_stage(self, text):
        self.stage_label.configure(text=text)
    def is_processing(self):
        return self.result_queue is not None
