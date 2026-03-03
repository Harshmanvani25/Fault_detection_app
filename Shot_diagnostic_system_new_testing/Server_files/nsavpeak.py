# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:06:14 2026

@author: Harsh
"""

# nsavpeak.py

import numpy as np

def npltpeak(pos, peak, xdata, ydata):
    global h_shotno

    # Convert to numpy arrays (to mimic MATLAB behavior)
    pos = np.asarray(pos)
    peak = np.asarray(peak)
    xdata = np.asarray(xdata)
    ydata = np.asarray(ydata).copy()

    yl = len(ydata)
    PI = 3.141592

    size_peak = len(pos)
    mid_peak = int((size_peak + 1) / 2)

    sign_phase = np.zeros(size_peak)
    phase_add = np.zeros(size_peak)

    # ----------------------------------------
    # for i=1:2:mid_peak
    # ----------------------------------------
    for i in range(0, mid_peak, 2):
        sign_phase[i] = 1
        phase_add[i] = (i) * PI

    # ----------------------------------------
    # for i=2:2:mid_peak-1
    # ----------------------------------------
    for i in range(1, mid_peak - 1, 2):
        sign_phase[i] = -1
        phase_add[i] = (i + 1) * PI

    # ----------------------------------------
    if (mid_peak % 2) == 0:
        sign_phase[mid_peak - 1] = 1
        phase_add[mid_peak - 1] = phase_add[mid_peak - 2]

    # ----------------------------------------
    for i in range(mid_peak, size_peak - 1, 2):
        sign_phase[i] = -1
        if (mid_peak % 2) == 0:
            phase_add[i] = phase_add[mid_peak - 2] - (i - mid_peak) * PI
        else:
            phase_add[i] = phase_add[mid_peak - 2] - (i - mid_peak + 2) * PI

    # ----------------------------------------
    for i in range(mid_peak - 1, size_peak - 1, 2):
        sign_phase[i] = 1
        phase_add[i] = phase_add[mid_peak - 1] - (i - (mid_peak - 1)) * PI

    # ----------------------------------------
    if ((mid_peak + 1) % 2) == 0:
        for i in range(mid_peak - 1, size_peak - 1):
            sign_phase[i] = (-1) * sign_phase[i]

    dens = np.zeros_like(ydata)
    x = np.zeros_like(xdata)

    # ========================================
    # for ipeak=1:2:size_peak-1
    # ========================================
    for ipeak in range(0, size_peak - 1, 2):

        ilower = int(pos[ipeak] - 1)
        iupper = int(pos[ipeak + 1] - 1)

        ab1 = abs(peak[ipeak] - peak[ipeak + 1]) / 2

        for i in range(ilower, iupper + 1):
            if ydata[i] > peak[ipeak]:
                ydata[i] = peak[ipeak]
            elif ydata[i] < peak[ipeak + 1]:
                ydata[i] = peak[ipeak + 1]

        dens[ilower:iupper + 1] = (
            np.arccos(((ydata[ilower:iupper + 1] - peak[ipeak]) / ab1) + 1)
            * sign_phase[ipeak]
            + phase_add[ipeak]
        )

    # ========================================
    # for ipeak=2:2:size_peak
    # ========================================
    for ipeak in range(1, size_peak - 1, 2):

        ilower = int(pos[ipeak])
        iupper = int(pos[ipeak + 1] - 2)

        ab1 = abs(peak[ipeak] - peak[ipeak + 1]) / 2

        #for i=1:yl
        for i in range(ilower, iupper + 1):
            if ydata[i] < peak[ipeak]:
                ydata[i] = peak[ipeak]
            elif ydata[i] > peak[ipeak + 1]:
                ydata[i] = peak[ipeak + 1]

        dens[ilower:iupper + 1] = (
            np.arccos(((ydata[ilower:iupper + 1] - peak[ipeak + 1]) / ab1) + 1)
            * sign_phase[ipeak]
            + phase_add[ipeak]
        )

    lastpos = len(pos)

    for i in range(int(pos[0] - 1), int(pos[lastpos - 1] - 1)):
        x[i] = xdata[i]

    x = x.reshape(-1, 1)
    y = dens * 0.2368

    #        plot(x,y);

    xresult = x
    yresult = y

    return xresult, yresult

########################## end of plotpeak #################################
