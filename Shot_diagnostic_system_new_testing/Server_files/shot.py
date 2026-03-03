

"""
Converted from shot.m
Written by V. K. Panchal
"""

import os
import numpy as np
from Server_files import p_global
from Server_files.shot_area import shot_area


def shot(sno=None):

    # -------------------------------------------------
    # MATLAB behavior:
    # If no argument → load latest shot from shot.num
    # -------------------------------------------------
    if sno is None or sno == '':

        latest_file = '/home/minsha/adserver_mount/adityadata/data/aditya/shot.num'

        if os.path.exists(latest_file):
            with open(latest_file, 'r') as f:
                shot_no = f.read().strip()
        else:
            print("shot.num file not found")
            return

    else:
        shot_no = str(int(sno)).strip()

    # Store globally (like MATLAB global)
    p_global.shot_no = shot_no

    # -------------------------------------------------
    # Get directory, status, OS_ID
    # -------------------------------------------------
    dir_name, shot_return_status, OS_ID = shot_area(shot_no)

    p_global.dir_name = dir_name
    p_global.shot_return_status = shot_return_status
    p_global.OS_ID = OS_ID

    # -------------------------------------------------
    # Initialize log_struct
    # -------------------------------------------------
    p_global.log_struct = []

    # -------------------------------------------------
    # If shot invalid → stop (MATLAB behavior)
    # -------------------------------------------------
    if shot_return_status != 1:
        return

    # -------------------------------------------------
    # Read logchan.info
    # -------------------------------------------------
    file_name = os.path.join(dir_name, 'logchan.info')

    if not os.path.exists(file_name):
        p_global.shot_return_status = 0
        print(f'logchan bin. info. file for shot {shot_no} is not exist')
        return

    with open(file_name, 'rb') as fid:

        while True:

            data = fid.read(2)
            if not data:
                break

            log_no = np.frombuffer(data, dtype=np.int16)[0]
            mod_type = np.fromfile(fid, dtype=np.int16, count=1)[0]
            mod_no = np.fromfile(fid, dtype=np.int16, count=1)[0]
            chan_no = np.fromfile(fid, dtype=np.int16, count=1)[0]

            chan_label = np.fromfile(fid, dtype='S1', count=9)
            chan_label = b''.join(chan_label).decode(errors='ignore')

            data_sign = np.fromfile(fid, dtype=np.int16, count=1)[0]
            calib_factor = np.fromfile(fid, dtype=np.float32, count=1)[0]

            p_global.log_struct.append({
                'log_no': log_no,
                'mod_type': mod_type,
                'mod_no': mod_no,
                'chan_no': chan_no,
                'chan_label': chan_label,
                'data_sign': data_sign,
                'calib_factor': calib_factor
            })

    # Debug (optional)
    print("DEBUG:")
    print("shot_no:", p_global.shot_no)
    print("dir_name:", p_global.dir_name)
    print("status:", p_global.shot_return_status)
    print("OS_ID:", p_global.OS_ID)
    print("Total channels loaded:", len(p_global.log_struct))
