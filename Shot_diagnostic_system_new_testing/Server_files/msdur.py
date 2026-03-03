# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 16:58:32 2026

@author: Harsh
"""

# msdur.py
# This routine is used to extract the data for the period given
# (in milliseconds) as argument.
#
# Usage:
#   xResult, yResult = msdur(xData, yData, Start_ms, End_ms)
#        OR
#   xResult, yResult = msdur(xData, yData, Just_ms)
#
# Written by V K Panchal
# Python equivalent conversion (no logic change)

import numpy as np


def msdur(xData, yData, Start_ms, End_ms=None):

    # Convert to numpy arrays (to mimic MATLAB behavior)
    xData = np.asarray(xData)
    yData = np.asarray(yData)

    nargin = 3 if End_ms is None else 4
    nargout = 2  # Python always returns 2 values here

    # ------------------------------------------
    # Starting time validation (same logic)
    # ------------------------------------------
    if (nargin == 3) or (nargin == 4):
        if (Start_ms < xData[0]) or (Start_ms > xData[len(xData) - 1]):
            raise ValueError('*** Give proper starting & ending time in Millisecond ***')

    # ------------------------------------------
    # Argument validation
    # ------------------------------------------
    if (nargin < 3) or (nargin > 4):
        print(" type `[X_Out,Y_Out]=msdur(X_In,Y_In,Start_ms,End_ms)`  ")
        print("           ---   OR  ----   ")
        print(" type `[X_Out,Y_Out]=msdur(X_In,Y_In,Just_ms)`  ")
        return None, None

    # ======================================================
    # CASE 1: Only one millisecond (nargin == 3)
    # ======================================================
    elif (nargout == 2) and (nargin == 3):

        Element_no = np.where(xData == Start_ms)[0]

        if len(Element_no) > 0:
            xResult = xData[Element_no]
            yResult = yData[Element_no]
        else:
            xResult = np.array([])
            yResult = np.array([])

        return xResult, yResult

    # ======================================================
    # CASE 2: Start and End time (nargin == 4)
    # ======================================================
    elif (nargout == 2) and (nargin == 4):

        if (End_ms < xData[0]) or (End_ms > xData[len(xData) - 1]):
            raise ValueError('*** Give proper starting & ending time in Millisecond ***')

        TempI = np.where((xData >= Start_ms) & (xData <= End_ms))[0]

        if len(TempI) > 0:
            Element_no1 = TempI[0]
            Element_no2 = TempI[len(TempI) - 1]

            xResult = xData[Element_no1:Element_no2 + 1]
            yResult = yData[Element_no1:Element_no2 + 1]
        else:
            xResult = np.array([])
            yResult = np.array([])

        return xResult, yResult
