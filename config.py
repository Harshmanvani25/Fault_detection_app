# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 12:04:05 2026

@author: Harsh
"""
#config.py
# config.py

import json
import os

# Create a permanent app folder in user's home directory
BASE_DIR = os.path.join(os.path.expanduser("~"), "ShotDiagnostics")
os.makedirs(BASE_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(BASE_DIR, "app_config.json")

DEFAULT_CONFIG = {
    "server_folder": os.path.expanduser("~/Server_code_python")
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)