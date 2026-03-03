# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:35:15 2026

@author: Harsh
"""

# ui/dashboard.py

import customtkinter as ctk
import multiprocessing

from services.process_manager import ProcessManager

from ui.dashboard_header import build_header
from ui.dashboard_server import build_server_card
from ui.dashboard_controls import ControlPanel
from ui.dashboard_execution import ExecutionPanel
from ui.dashboard_results import ResultsPanel
from ui.dashboard_batch import BatchPanel
from ui.dashboard_logs import LogsPanel
from ui.dashboard_error import ErrorPanel

def launch_dashboard():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    
    root.title("Shot Diagnostic System")
    #root.after(200, lambda: root.state("zoomed"))
    # root.state("zoomed")

    process_manager = ProcessManager()
    # ==================================================
    # HEADER (create first so it stays at top)
    # ==================================================
    def toggle_theme():

        current_mode = ctk.get_appearance_mode()
    
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
        # Force focus back to root
        root.after(50, lambda: root.focus_force())

    theme_button, mode_badge = build_header(
        root,
        None,   # temporarily no execution
        root,
        toggle_theme
    )
    # ==================================================
    # HEADER
    # ==================================================

    
    # theme_button, mode_badge = build_header(root, root, toggle_theme)
    # mode_badge = ctk.CTkLabel(
    #     root,
    #     text="LOCAL MODE",
    #     font=("Arial", 12, "bold"),
    #     corner_radius=30,
    #     fg_color="#3498db",
    #     text_color="white",
    #     padx=15,
    #     pady=8
    # )
    # mode_badge.place(relx=0.85, rely=0.03)
    # ==================================================
    # SERVER CARD
    # ==================================================
    
    
    
    def update_status(text):
        status_text.configure(text=text)

    logs_panel = None  # placeholder for log callback

    def log_callback(level, msg):
        if logs_panel:
            logs_panel.log(level, msg)

    server_state = build_server_card(
        root,
        root,
        log_callback,
        update_status
    )

    # ==================================================
    # MAIN FRAME
    # ==================================================

    main_frame = ctk.CTkFrame(root, corner_radius=20)
    main_frame.pack(fill="both", expand=True, padx=60, pady=20)

    left_panel = ctk.CTkFrame(main_frame, corner_radius=15)
    left_panel.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

    right_panel = ctk.CTkFrame(main_frame, corner_radius=15)
    right_panel.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

    # ==================================================
    # CONTROLS
    # ==================================================

    controls = ControlPanel(left_panel)
    def update_mode_badge():
        if controls.is_server_mode():
            mode_badge.configure(text="SERVER MODE", fg_color="#27ae60")
        else:
            mode_badge.configure(text="LOCAL MODE", fg_color="#3498db")

    root.after(500, update_mode_badge)
    
    # ==================================================
    # RESULTS + BATCH
    # ==================================================

    results = ResultsPanel(right_panel, root)
    error_panel = ErrorPanel(left_panel)
    batch = BatchPanel(right_panel)
    # ==================================================
    # EXECUTION
    # ==================================================

    execution = ExecutionPanel(
    left_panel,
    process_manager,
    controls,
    batch,
    results,
    error_panel,
    log_callback
    )
    
    # ==================================================
    # HEADER (Moved below execution creation)
    # ==================================================
    
    # theme_button, mode_badge = build_header(
        # root,
        # execution,     # pass execution panel
        # root,          # parent
        # toggle_theme
    # )
    
    # ==================================================
    # LOGS
    # ==================================================

    logs_panel = LogsPanel(right_panel)

    # ==================================================
    # STATUS BAR
    # ==================================================

    status_bar = ctk.CTkFrame(root, height=35)
    status_bar.pack(fill="x", side="bottom")

    status_text = ctk.CTkLabel(
        status_bar,
        text="System Idle",
        font=("Arial", 12)
    )
    status_text.pack(side="left", padx=20)

    # ==================================================
    # QUEUE HANDLER
    # ==================================================

    def check_queue():

        queue = execution.get_queue()
        update_mode_badge()
        if queue is not None:
            while not queue.empty():
                msg = queue.get()
                msg_type = msg[0]
                if msg_type == "stage":
                    execution.stage_label.configure(text=msg[1])
                
                elif msg_type == "progress":
                    execution.progress.set(msg[1] / 100)
                
                elif msg_type == "active_shot":
                    results.set_active_shot(msg[1])

                elif msg_type == "file_result":
                    status_text.configure(text="Processing...")
                    shot, fault, exec_time = msg[1], msg[2], msg[3]
                    results.set_result(shot, fault, exec_time)
                    batch.update_result(fault)

                elif msg_type == "batch_complete":
                    status_text.configure(text="Batch Completed")
                    batch.complete()
                    execution.enable_run()

                elif msg_type == "error":

                        status_text.configure(text="Error Occurred")
                    
                        # Show error panel
                        error_panel.show(msg[1])
                    
                        # Structured log
                        logs_panel.log("ERROR", msg[1])
                    
                        # Re-enable run
                        execution.enable_run()

        root.after(200, check_queue)

    root.after(200, check_queue)

    # ==================================================
    # CLEAN EXIT
    # ==================================================

    def on_closing():
        process_manager.stop_worker()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
