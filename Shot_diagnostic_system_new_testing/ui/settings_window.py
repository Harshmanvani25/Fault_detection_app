# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:04:24 2026

@author: Harsh
"""

# ui/settings_window.py

import customtkinter as ctk
from config import load_config, save_config
from tkinter import filedialog
import os
import glob
from tkinter import messagebox

def open_settings(root, execution_panel):
   
    settings_window = ctk.CTkToplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("650x650")
    
    # ---- SAFE MODAL PATTERN (RPi Fix) ----
    settings_window.transient(root)
    settings_window.update_idletasks()
    
    # Center on parent window
    x = root.winfo_x() + (root.winfo_width() // 2) - 275
    y = root.winfo_y() + (root.winfo_height() // 2) - 225
    settings_window.geometry(f"+{x}+{y}")
    
    settings_window.lift()
    
    # Safe grab (delayed for RPi)
    settings_window.after(100, settings_window.grab_set)
    # ---------------------------------------
    # settings_window.grab_set()   # modal window
    # settings_window.after(100, settings_window.grab_set)
    title = ctk.CTkLabel(
        settings_window,
        text="Application Settings",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    # -----------------------------
    # Server Folder Setting
    # -----------------------------
    
    config = load_config()
    
    server_label_title = ctk.CTkLabel(
        settings_window,
        text="Server File Folder:",
        font=("Arial", 16, "bold")
    )
    server_label_title.pack(pady=(20, 5))
    
    server_path_label = ctk.CTkLabel(
        settings_window,
        text=config.get("server_folder", "Not Set"),
        wraplength=400
    )
    server_path_label.pack(pady=5)
    
    
    def choose_server_folder():
        if execution_panel.is_processing():
            messagebox.showwarning(
                "Processing Running",
                "Cannot change folder while processing is running."
            )
            return
        folder = filedialog.askdirectory()
        if folder:
            config["server_folder"] = folder
            save_config(config)
            server_path_label.configure(text=folder)
            load_excel_files()   # 🔥 refresh file list immediately
    
    change_button = ctk.CTkButton(
        settings_window,
        text="Change Folder",
        command=choose_server_folder
    )
    change_button.pack(pady=15)
    
    # ----------------------------------
    # Excel File Management Section
    # ----------------------------------
    
    separator = ctk.CTkLabel(settings_window, text="-"*50)
    separator.pack(pady=10)
    
    file_title = ctk.CTkLabel(
        settings_window,
        text="Excel Files in Server Folder",
        font=("Arial", 16, "bold")
    )
    file_title.pack(pady=(5, 5))
    
    file_frame = ctk.CTkScrollableFrame(settings_window, height=250)
    file_frame.pack(fill="both", expand=True, padx=20, pady=5)
    
    file_vars = {}
    
    def load_excel_files():
        # Clear existing widgets
        for widget in file_frame.winfo_children():
            widget.destroy()
    
        file_vars.clear()
    
        folder = config.get("server_folder", "")
        if not os.path.exists(folder):
            return
    
        excel_files = glob.glob(os.path.join(folder, "*.xlsx"))
    
        if not excel_files:
            ctk.CTkLabel(
                file_frame,
                text="No Excel files found."
            ).pack(pady=10)
            return
    
        for file_path in excel_files:
            file_name = os.path.basename(file_path)
            var = ctk.BooleanVar()
            file_vars[file_path] = var
    
            ctk.CTkCheckBox(
                file_frame,
                text=file_name,
                variable=var
            ).pack(anchor="w", padx=10, pady=2)
    
    def delete_selected_files():
        if execution_panel.is_processing():
            messagebox.showwarning(
                "Processing Running",
                "Cannot modify files while processing is running."
            )
            return
        selected_files = [path for path, var in file_vars.items() if var.get()]
    
        if not selected_files:
            messagebox.showwarning("Delete Files", "No files selected.")
            return
    
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {len(selected_files)} selected file(s)?"
        )
        if not confirm:
            return
    
        for file_path in selected_files:
            try:
                os.remove(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete:\n{file_path}\n{str(e)}")
    
        load_excel_files()
    
    def delete_all_files():
        messagebox.showwarning(
            "Processing Running",
            "Cannot modify files while processing is running."
        )
        return
        folder = config.get("server_folder", "")
        excel_files = glob.glob(os.path.join(folder, "*.xlsx"))
    
        if not excel_files:
            messagebox.showinfo("Delete Files", "No Excel files to delete.")
            return
    
        confirm = messagebox.askyesno(
            "Confirm Delete All",
            f"Delete ALL {len(excel_files)} Excel file(s)?"
        )
        if not confirm:
            return
    
        for file_path in excel_files:
            try:
                os.remove(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete:\n{file_path}\n{str(e)}")
    
        load_excel_files()
    
    button_frame = ctk.CTkFrame(settings_window)
    button_frame.pack(pady=10)
    
    delete_selected_btn = ctk.CTkButton(
        button_frame,
        text="Delete Selected",
        fg_color="#c0392b",
        hover_color="#992d22",
        command=delete_selected_files
    )
    delete_selected_btn.grid(row=0, column=0, padx=10)
    
    delete_all_btn = ctk.CTkButton(
        button_frame,
        text="Delete All",
        fg_color="#e67e22",
        hover_color="#ca6f1e",
        command=delete_all_files
    )
    delete_all_btn.grid(row=0, column=1, padx=10)
    
    # Initial load
    load_excel_files()