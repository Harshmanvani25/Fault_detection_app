# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 14:44:29 2026

@author: Harsh
"""

# services/mount_manager.py


import subprocess
import os
import platform

MOUNT_POINT = os.path.expanduser("~/adserver_mount")
IS_LINUX = platform.system() == "Linux"


def is_mounted():
    if not IS_LINUX:
        return False

    try:
        result = subprocess.run(
            ["mount"],
            capture_output=True,
            text=True
        )
        return MOUNT_POINT in result.stdout
    except Exception:
        return False


def mount_server(host, username, password):
    if not IS_LINUX:
        return False, "Mounting is supported only on Linux systems."

    try:
        if is_mounted():
            return True, "Server already mounted."

        os.makedirs(MOUNT_POINT, exist_ok=True)

        cmd = [
            "sshfs",
            f"{username}@{host}:/",
            MOUNT_POINT,
            "-o", "password_stdin",
            "-o", "StrictHostKeyChecking=no"
        ]

        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(password + "\n")

        if process.returncode == 0:
            return True, "Server mounted successfully."
        else:
            return False, stderr.strip()

    except Exception as e:
        return False, str(e)


def unmount_server():
    if not IS_LINUX:
        return False, "Unmounting is supported only on Linux systems."

    try:
        if not is_mounted():
            return True, "Server already disconnected."

        result = subprocess.run(
            ["fusermount", "-u", MOUNT_POINT],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return True, "Server disconnected successfully."
        else:
            return False, result.stderr.strip()

    except Exception as e:
        return False, str(e)