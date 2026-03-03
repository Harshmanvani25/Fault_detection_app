# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:00:04 2026

@author: Harsh
"""

# ui/history_manager.py

import customtkinter as ctk
from tkinter import messagebox


def clear_history(history_data, window):
    history_data.clear()
    window.destroy()
    messagebox.showinfo("History", "History cleared successfully.")


def open_history_window(root, history_data, accent_color):
    if not history_data:
        messagebox.showinfo("History", "No history available yet.")
        return

    history_window = ctk.CTkToplevel(root)
    history_window.title("Diagnosis History")
    history_window.geometry("650x450")   # slightly larger
    
    # ---- SAFE MODAL PATTERN (RPi Fix) ----
    history_window.transient(root)
    history_window.update_idletasks()
    
    # Center on parent window
    x = root.winfo_x() + (root.winfo_width() // 2) - 325
    y = root.winfo_y() + (root.winfo_height() // 2) - 225
    history_window.geometry(f"+{x}+{y}")
    
    history_window.lift()
    
    # Safe grab (delayed for RPi)
    history_window.after(100, history_window.grab_set)
    # ---------------------------------------

    title = ctk.CTkLabel(
        history_window,
        text="Diagnosis History",
        font=("Arial", 20, "bold"),
        text_color=accent_color
    )
    title.pack(pady=15)

    clear_history_btn = ctk.CTkButton(
        history_window,
        text="Clear History",
        fg_color="#c0392b",
        hover_color="#992d22",
        command=lambda: clear_history(history_data, history_window)
    )
    clear_history_btn.pack(pady=5)

    table_frame = ctk.CTkScrollableFrame(
        history_window,
        fg_color=("white", "#1A1A1A")
    )
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Header Row
    headers = ["Date & Time", "Shot", "Result"]
    for col, header_text in enumerate(headers):
        header_label = ctk.CTkLabel(
            table_frame,
            text=header_text,
            font=("Arial", 14, "bold")
        )
        header_label.grid(row=0, column=col, padx=20, pady=10)

    # Data Rows
    for row_index, item in enumerate(history_data, start=1):

        ctk.CTkLabel(
            table_frame,
            text=item["datetime"]
        ).grid(row=row_index, column=0, padx=20, pady=5)

        ctk.CTkLabel(
            table_frame,
            text=item["shot"]
        ).grid(row=row_index, column=1, padx=20, pady=5)

        result_color = "#27ae60" if item["result"].upper() == "NORMAL" else "#c0392b"

        ctk.CTkLabel(
            table_frame,
            text=item["result"],
            text_color=result_color
        ).grid(row=row_index, column=2, padx=20, pady=5)