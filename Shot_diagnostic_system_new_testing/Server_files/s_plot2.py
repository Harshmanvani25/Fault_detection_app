# s_plot.py
# Exact MATLAB equivalent
# No logic changed

import matplotlib.pyplot as plt
import numpy as np
from Server_files import p_global
from Server_files.save_data import save_data


def s_plot2(wno, Data1=None, Data2=None, ColorSetting=None):

    # -----------------------------
    # Argument validation
    # -----------------------------
    if Data1 is None:
        print('Usage : s_plot(window_no,logical_channel_number[,Color]')
        print('            --- or ---')
        print('        s_plot(window_no,X_data,Y_data[,Color]')
        return

    log_chan = 0
    Label = ''
    top_t = ''
    s1 = {'chan_label': '', 'top_t': ''}

    # -----------------------------
    # Logical channel handling
    # -----------------------------
    if Data2 is not None and isinstance(Data2, str):
        ColorSetting = Data2
        Data1, Data2, s1 = save_data(Data1)

    elif Data2 is None:
        log_chan = Data1
        Data1, Data2, s1 = save_data(Data1)

    if len(Data1) == 0 or len(Data2) == 0:
        return

    if ColorSetting is None:
        Label = s1.get('chan_label', '')
        top_t = s1.get('top_t', '')

    # -----------------------------
    # IP max printing (5–7)
    # -----------------------------
    if (log_chan >= 5) and (log_chan <= 7):
        print(f"Max {Label} = {np.max(Data2)}")

    # -----------------------------
    # Window validation
    # -----------------------------
    if wno > p_global.WINDOW_COUNTER:
        print('First define no. of. window using pr_window(n[,m])')
        print('n - any number, 1 <= m <= 2')
        return

    # -----------------------------
    # Color handling (MATLAB order)
    # -----------------------------
    COLOR_ORDER = ['r', 'g', 'b', 'y', 'm', 'c']

    if not hasattr(p_global, 'color_index') or p_global.color_index is None:
        p_global.color_index = 0

    if wno == 1:
        p_global.color_index += 1

    if p_global.color_index > 6 or p_global.color_index < 1:
        p_global.color_index = 1

    if ColorSetting is None:
        ColorSetting = COLOR_ORDER[p_global.color_index - 1]

    # -----------------------------
    # Axis selection
    # -----------------------------
    ax = p_global.H_AX1[wno - 1]

    x_limit = ax.get_xlim()
    y_limit = ax.get_ylim()

    # -----------------------------
    # Axis range logic (MATLAB exact)
    # -----------------------------
    startx = getattr(p_global, 'startx', None)
    endx   = getattr(p_global, 'endx', None)
    starty = getattr(p_global, 'starty', None)
    endy   = getattr(p_global, 'endy', None)

    # X min
    if startx is None:
        minx = np.min(Data1)
        if minx > x_limit[0]:
            minx = x_limit[0]
        minx = -10
    else:
        minx = startx

    # X max
    if endx is None:
        maxx = np.max(Data1)
        if maxx < x_limit[1]:
            maxx = x_limit[1]
        maxx = 100
    else:
        maxx = endx

    # Y min
    if starty is None:
        miny = np.min(Data2)
        if miny > y_limit[0]:
            miny = y_limit[0]
    else:
        miny = starty

    # Y max
    if endy is None:
        maxy = np.max(Data2)
        if maxy < y_limit[1]:
            maxy = y_limit[1]
    else:
        maxy = endy

    # -----------------------------
    # Plotting (exact)
    # -----------------------------
    p_global.H_PL1[wno - 1] = ax.plot(Data1, Data2, ColorSetting)[0]
    ax.set_ylabel(Label)

    if wno == 1:
        ax.set_title(top_t)

    if wno == p_global.WINDOW_COUNTER:
        ax.set_xlabel('Time(ms)')

    ax.set_xlim([minx, maxx])
    ax.set_ylim([miny, maxy])

    return
