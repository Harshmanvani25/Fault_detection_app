# ui/dashboard_header.py

import customtkinter as ctk
from ui.settings_window import open_settings


def build_header(root, execution_panel, parent, toggle_theme_callback):

    header = ctk.CTkLabel(
        parent,
        text="SHOT DIAGNOSTIC SYSTEM",
        font=("Arial", 34, "bold"),
        text_color=("#1f4e79", "#00e5ff")
    )
    header.pack(pady=20)

    top_control_frame = ctk.CTkFrame(parent, fg_color="transparent")
    top_control_frame.place(relx=0.98, rely=0.03, anchor="ne")

    

    # ---- Settings Button ----
    settings_button = ctk.CTkButton(
        top_control_frame,
        text="⚙",
        width=35,
        height=35,
        corner_radius=30,
        font=("Arial", 23),
        fg_color="#8e44ad",
        hover_color="#732d91",
        command=lambda: open_settings(root, execution_panel)
    )
    settings_button.pack(side="right", padx=10)

    # ---- Theme Toggle ----
    theme_icon_button = ctk.CTkButton(
        top_control_frame,
        text="🌙",
        width=37,
        height=37,
        corner_radius=30,
        fg_color="#2c3e50",
        hover_color="#34495e",
        font=("Arial", 23),
        command=toggle_theme_callback
    )
    theme_icon_button.pack(side="right", padx=10)
    
    # ---- MODE BADGE (aligned with header buttons) ----
    mode_badge = ctk.CTkLabel(
        top_control_frame,
        text="LOCAL MODE",
        font=("Arial", 12, "bold"),
        corner_radius=30,
        fg_color="#3498db",
        text_color="white",
        padx=15,
        pady=13
    )
    mode_badge.pack(side="right", padx=10)

    # return both so dashboard can update badge
    return theme_icon_button, mode_badge