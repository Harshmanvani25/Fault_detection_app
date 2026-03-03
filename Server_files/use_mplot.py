# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:51:41 2026

@author: Harsh
"""

# Batch runner for m_plot2
# Calls m_plot2 for multiple shots

#import numpy as np
from Server_files.m_plot2 import m_plot2

# ================= USER CONFIGURATION =================

mode = 'array'   # 'array' or 'range'

# --------- Array based selection (option 1) ----------
shots_array = [32322]

# --------- Range based selection (option 2) ----------
start_shot = 31102
end_shot   = 40000
steps      = 45

# --------- Diagnostics (Logical Channel Numbers) -----
#channels = [2, 7, 59, 22, 23, 156, 301, 302, 216, 85, 305, 316]
channels = [22]
# ======================================================

# --------- Create the shot list -----------------------
mode = mode.lower()

if mode == 'array':
    shots = shots_array

elif mode == 'range':
    shots = list(range(start_shot, end_shot + 1, steps))

else:
    raise ValueError('Invalid mode. Use "array" or "range".')

# ======================================================

print('Starting batch processing...')

for shot_no in shots:

    print(f"\nProcessing shot {shot_no}")

    try:
        # IMPORTANT:
        # m_plot2 expects individual channel arguments, not list
        m_plot2(shot_no, *channels)

    except Exception as e:
        print(f"Error in shot {shot_no}: {str(e)}")
        continue

print('\nBatch processing completed.')
