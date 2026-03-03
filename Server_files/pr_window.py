
# pr_window.py
# Exact MATLAB-style window positioning
# Converted without changing logic

import matplotlib.pyplot as plt
from Server_files import p_global

def pr_window(no_row=None, no_col=None):

    # MATLAB default handling
    if no_row is None:
        no_row = 1
        no_col = 1

    if no_col is None:
        no_col = 1

    if no_row == 0 or no_col == 0:
        no_row = 1
        no_col = 1

    if no_col > 2:
        no_col = 2

    # Clear previous axes if needed (MATLAB checks children)
    # We do not auto-clear figure to preserve behavior

    p_global.H_AX1 = []

    # -------------------------------
    # MATLAB positioning constants
    # -------------------------------
    X1_POS_MAIN = 0.1000
    X2_POS_MAIN = 0.8200
    Y1_POS_MAIN = 0.1000
    Y2_POS_MAIN = 0.9100

    x1 = X1_POS_MAIN
    x2 = X2_POS_MAIN
    y1 = Y1_POS_MAIN
    y2 = Y2_POS_MAIN

    x1_diff = x2 / no_col
    temp_x1 = x1
    temp_x2 = x1_diff

    y1_diff = (y2 - y1) / no_row

    window_counter = 1

    fig = plt.gcf()

    # --------------------------------
    # EXACT MATLAB double loop logic
    # --------------------------------
    for j in range(1, no_col + 1):

        temp_y1 = y2 - y1_diff

        for i in range(1, no_row + 1):

            set_ax = [temp_x1, temp_y1, temp_x2, y1_diff]

            ax = fig.add_axes(set_ax)  # EXACT manual positioning

            ax.set_box_aspect(None)
            ax.set_xticklabels([])
            ax.set_frame_on(True)

            # Right side Y axis for second column
            if j == 2:
                ax.yaxis.set_label_position("right")
                ax.yaxis.tick_right()

            # Bottom X ticks only for last row
            if i == no_row:
                ax.tick_params(labelbottom=True)

            p_global.H_AX1.append(ax)

            temp_y1 = temp_y1 - y1_diff
            window_counter += 1

        temp_x1 = temp_x1 + x1_diff

    p_global.WINDOW_COUNTER = window_counter - 1
    p_global.H_PL1 = [None] * (window_counter - 1)


    return
# ===============================
# MATLAB Global Variables
# ===============================

# Plotting globals
H_AX1 = []
H_PL1 = []
WINDOW_COUNTER = 0
color_index = 0

# Axis control globals
startx = None
endx = None
starty = None
endy = None
x = None
color_set = None
