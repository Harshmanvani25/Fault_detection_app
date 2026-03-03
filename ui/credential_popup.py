# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 14:45:46 2026

@author: Harsh
"""

# ui/credential_popup.py

import customtkinter as ctk


class CredentialPopup(ctk.CTkToplevel):
    def __init__(self, root, callback):
        super().__init__(root)

        self.callback = callback

        self.title("Server Login")
        self.geometry("420x380")   # Increased height
        self.resizable(False, False)

        # ---- SAFE MODAL PATTERN (RPi Fix) ----
        self.transient(root)
        self.update_idletasks()

        # Center on parent window
        x = root.winfo_x() + (root.winfo_width() // 2) - 210
        y = root.winfo_y() + (root.winfo_height() // 2) - 190
        self.geometry(f"+{x}+{y}")

        self.lift()

        # Safe grab (delayed for RPi stability)
        self.after(100, self.grab_set)
        # ---------------------------------------

        # -----------------------------
        # Host Entry
        # -----------------------------
        ctk.CTkLabel(self, text="Host").pack(pady=(20, 5))
        self.host_entry = ctk.CTkEntry(self, width=250)
        self.host_entry.pack(pady=5)
        self.host_entry.insert(0, "adserver")  # Default value

        # -----------------------------
        # Username Entry
        # -----------------------------
        ctk.CTkLabel(self, text="Username").pack(pady=(10, 5))
        self.user_entry = ctk.CTkEntry(self, width=250)
        self.user_entry.pack(pady=5)

        # -----------------------------
        # Password Entry
        # -----------------------------
        ctk.CTkLabel(self, text="Password").pack(pady=(10, 5))
        self.pass_entry = ctk.CTkEntry(self, show="*", width=250)
        self.pass_entry.pack(pady=5)

        # -----------------------------
        # Connect Button
        # -----------------------------
        ctk.CTkButton(
            self,
            text="Connect",
            width=150,
            command=self._submit
        ).pack(pady=25)

    def _submit(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()

        # Send credentials to mount manager
        self.callback(host, user, password)

        # Close popup
        self.destroy()