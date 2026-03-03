# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:09:35 2026

@author: Harsh
"""

# services/server_service.py

import random


def connect_server(root,
                   server_state,
                   server_indicator,
                   connect_button,
                   disconnect_button,
                   log_function):

    server_indicator.configure(text="● Server: Connecting...", text_color="orange")
    root.update()

    server_state["connected"] = True

    server_indicator.configure(
        text="● Server: Connected",
        text_color="#2ecc71"
    )

    connect_button.configure(state="disabled")
    disconnect_button.configure(state="normal")

    log_function("INFO", "Server connected successfully.");


def disconnect_server(server_state,
                      server_indicator,
                      connect_button,
                      disconnect_button,
                      log_function):

    server_state["connected"] = False

    server_indicator.configure(
        text="● Server: Disconnected",
        text_color="#e74c3c"
    )

    connect_button.configure(state="normal")
    disconnect_button.configure(state="disabled")

    log_function("INFO","Server disconnected.");


def check_server_status(root,
                        server_state,
                        server_indicator,
                        update_status_function):

    if not server_state["connected"]:
        root.after(5000, lambda: check_server_status(
            root,
            server_state,
            server_indicator,
            update_status_function
        ))
        return

    health_ok = random.choice([True, True, True, False])

    if health_ok:
        server_indicator.configure(
            text="● Server: Connected",
            text_color="#2ecc71"
        )
    else:
        server_indicator.configure(
            text="● Server: Connection Lost",
            text_color="#e74c3c"
        )
        update_status_function("error")

    root.after(5000, lambda: check_server_status(
        root,
        server_state,
        server_indicator,
        update_status_function
    ))