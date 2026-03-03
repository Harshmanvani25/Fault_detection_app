import sys
import os

def resource_path(relative_path):
    """
    Works for:
    - Normal Python execution
    - PyInstaller one-file executable
    """

    if hasattr(sys, "_MEIPASS"):
        # Running inside PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in normal Python
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Move up one level to project root
        base_path = os.path.abspath(os.path.join(base_path, ".."))

    return os.path.join(base_path, relative_path)