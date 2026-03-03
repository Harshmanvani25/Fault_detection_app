# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 18:22:19 2026

@author: Harsh
"""

# ui/dashboard_server.py

import customtkinter as ctk

from services.mount_manager import mount_server, unmount_server, is_mounted
from ui.credential_popup import CredentialPopup


def build_server_card(parent, root, log_callback, status_callback):

    server_state = {"connected": False}

    server_card = ctk.CTkFrame(parent, corner_radius=12)
    server_card.pack(anchor="w", padx=60, pady=(10, 5))

    server_indicator = ctk.CTkLabel(
        server_card,
        text="● Server: Disconnected",
        font=("Arial", 14, "bold"),
        text_color="#e74c3c"
    )
    server_indicator.grid(row=0, column=0, padx=15, pady=10)

    connect_button = ctk.CTkButton(
        server_card,
        text="Connect",
        width=90,
        command=lambda: handle_connect(
            root,
            server_state,
            server_indicator,
            connect_button,
            disconnect_button,
            log_callback
        )
    )
    connect_button.grid(row=0, column=1, padx=5)

    disconnect_button = ctk.CTkButton(
        server_card,
        text="Disconnect",
        width=90,
        fg_color="#c0392b",
        hover_color="#992d22",
        state="disabled",
        command=lambda: handle_disconnect(
            server_state,
            server_indicator,
            connect_button,
            disconnect_button,
            log_callback
        )
    )
    disconnect_button.grid(row=0, column=2, padx=5)

    
    

    return server_state


def handle_connect(root, server_state, indicator, connect_btn, disconnect_btn, log_callback):

    if is_mounted():
        indicator.configure(text="● Server: Connected", text_color="#2ecc71")
        connect_btn.configure(state="disabled")
        disconnect_btn.configure(state="normal")
        server_state["connected"] = True
        log_callback("INFO", "Server already mounted.")
        return

    def attempt_mount(host, username, password):
        success, message = mount_server(host, username, password)

        if success:
            indicator.configure(text="● Server: Connected", text_color="#2ecc71")
            connect_btn.configure(state="disabled")
            disconnect_btn.configure(state="normal")
            server_state["connected"] = True
            log_callback("INFO", message)
        else:
            log_callback("ERROR", message)

    CredentialPopup(root, attempt_mount)


def handle_disconnect(server_state, indicator, connect_btn, disconnect_btn, log_callback):

    success, message = unmount_server()

    if success:
        indicator.configure(text="● Server: Disconnected", text_color="#e74c3c")
        connect_btn.configure(state="normal")
        disconnect_btn.configure(state="disabled")
        server_state["connected"] = False
        log_callback("INFO", message)
    else:
        log_callback("ERROR", message)