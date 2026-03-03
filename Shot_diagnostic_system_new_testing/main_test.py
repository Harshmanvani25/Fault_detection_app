import os
import sys
import multiprocessing

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure project root is in sys.path
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import your real launcher
from ui.dashboard_new import launch_dashboard


def main():
    launch_dashboard()

if __name__ == "__main__":
    import multiprocessing

    multiprocessing.set_start_method("spawn", force=True)
    multiprocessing.freeze_support()

    main()
