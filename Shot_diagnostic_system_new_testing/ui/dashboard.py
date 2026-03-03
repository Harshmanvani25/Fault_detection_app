# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 17:54:42 2026

@author: Harsh
"""

# ui/dashboard.py

import customtkinter as ctk
import os
import time
from tkinter import filedialog
from services.process_manager import ProcessManager
history = []


def launch_dashboard():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Shot Diagnostic System")
    # root.state("zoomed")

    process_manager = ProcessManager()
    result_queue = None

    # =========================
    # MAIN FRAME
    # =========================

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    left_panel = ctk.CTkFrame(main_frame)
    left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right_panel = ctk.CTkFrame(main_frame)
    right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # =========================
    # LEFT PANEL
    # =========================

    title_label = ctk.CTkLabel(
        left_panel,
        text="Shot Diagnostic System",
        font=("Arial", 26, "bold")
    )
    title_label.pack(pady=20)

    def on_run():
        nonlocal result_queue
    
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Excel Files", "*.xlsx")]
        )
    
        if not file_paths:
            return
    
        run_button.configure(state="disabled")
        stop_button.configure(state="normal")
    
        log(f"Selected {len(file_paths)} file(s)")
    
        result_queue = process_manager.start_worker(file_paths)
    
        progress.set(0)
        progress_label.configure(text="Progress: 0%")
    
        log("Worker started.")
    
    run_button = ctk.CTkButton(
        left_panel,
        text="Run Diagnosis",
        height=50,
        font=("Arial", 18, "bold"),
        command=on_run
    )
    run_button.pack(pady=20)

    def on_stop():
        process_manager.stop_worker()
    
        progress.set(0)
        progress_label.configure(text="Progress: 0%")
    
        run_button.configure(state="normal")
        stop_button.configure(state="disabled")
    
        log("Execution stopped.")
    
    stop_button = ctk.CTkButton(
        left_panel,
        text="Stop Execution",
        height=45,
        font=("Arial", 16, "bold"),
        fg_color="#c0392b",
        hover_color="#992d22",
        command=on_stop
    )
    stop_button.pack(pady=10)

    progress = ctk.CTkProgressBar(left_panel, width=300)
    progress.set(0)
    progress.pack(pady=20)

    progress_label = ctk.CTkLabel(left_panel, text="Progress: 0%")
    progress_label.pack()

    active_shot_label = ctk.CTkLabel(
        right_panel,
        text="Active Shot: -",
        font=("Arial", 14, "bold")
    )
    active_shot_label.pack(pady=(10,5))
    # =========================
    # RIGHT PANEL
    # =========================

    result_label = ctk.CTkLabel(
        right_panel,
        text="Result: -",
        font=("Arial", 22, "bold")
    )
    result_label.pack(pady=30)
    timer_label = ctk.CTkLabel(
        right_panel,
        text="Execution Time: -",
        font=("Arial", 12)
    )
    timer_label.pack(pady=(0,10))

    log_box = ctk.CTkTextbox(right_panel)
    log_box.pack(fill="both", expand=True, padx=10, pady=10)

    log_box.insert("end", "System Initialized...\n")
    log_box.configure(state="disabled")
    def log(message):
        log_box.configure(state="normal")
        log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        log_box.see("end")
        log_box.configure(state="disabled")
    def check_queue():
        nonlocal result_queue
    
        if result_queue is None:
            root.after(200, check_queue)
            return
    
        try:
            while not result_queue.empty():
                msg = result_queue.get()
    
                msg_type = msg[0]
    
                # ---------------- Progress ----------------
                if msg_type == "progress":
                    percent = msg[1]
                    progress.set(percent / 100)
                    progress_label.configure(text=f"Progress: {percent}%")
    
                # ---------------- Active Shot ----------------
                elif msg_type == "active_shot":
                    shot = msg[1]
                    active_shot_label.configure(text=f"Active Shot: {shot}")
                    log(f"Processing {shot}")
    
                # ---------------- File Result ----------------
                elif msg_type == "file_result":
                    shot, fault, exec_time = msg[1], msg[2], msg[3]
                    timer_label.configure(text=f"Execution Time: {exec_time:.2f}s")
                    history.append({
                        "shot": shot,
                        "result": fault,
                        "time": exec_time
                    })
                    if str(fault).upper() == "NORMAL":
                        result_label.configure(
                            text=f"Result: {fault}",
                            text_color="#2ecc71"
                        )
                    else:
                        result_label.configure(
                            text=f"Result: {fault}",
                            text_color="#e74c3c"
                        )
    
                    log(f"{shot} → {fault} ({exec_time:.2f}s)")
    
                # ---------------- Batch Complete ----------------
                elif msg_type == "batch_complete":
                    stats = msg[1]
    
                    log("===== Batch Complete =====")
                    log(f"Total: {stats['total']}")
                    log(f"Normal: {stats['normal']}")
                    log(f"Fault: {stats['fault']}")
                    log(f"Time: {stats['total_time']:.2f}s")
    
                    progress.set(1)
                    progress_label.configure(text="Progress: 100%")
                    run_button.configure(state="normal")
                    stop_button.configure(state="disabled")
    
                # ---------------- Error ----------------
                elif msg_type == "error":
                    log(f"ERROR: {msg[1]}")
                    run_button.configure(state="normal")
                    stop_button.configure(state="disabled")
    
        except Exception as e:
            log(f"Queue error: {e}")
    
        root.after(200, check_queue)
        
    root.after(200, check_queue)
    def on_closing():
        process_manager.stop_worker()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()