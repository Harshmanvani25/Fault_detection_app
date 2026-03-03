
"""
shot_area.py
Used to get path on which shot data exists
Converted from MATLAB version
"""

import os


def shot_area(shot_no):

    # --------------------------------------------
    # Minimum valid shot number check
    # --------------------------------------------
    if int(shot_no) < 12946:
        print('Valid shot no. is 12946 & above. Use apps for old shots')
        return '', -1, 0

    # --------------------------------------------
    # LINUX (Raspberry Pi) ROOT PATH
    # --------------------------------------------
    home_new = '/home/minsha/adserver_mount/adityadata/data/aditya/'
    home_pxi = '/home/minsha/adserver_mount/adityadata/data/pxi/'

    deli_style = '/'
    OS_ID = 2

    shot_no = str(int(shot_no)).strip()

    dir_name = home_new + 'sht' + shot_no + deli_style

    print("Checking directory:", dir_name)

    # --------------------------------------------
    # MATLAB EXACT LOGIC
    # --------------------------------------------
    if os.path.isdir(dir_name):
        status = 1

    else:
        pxidir_name = home_pxi + 'sht' + shot_no + deli_style

        if os.path.isdir(pxidir_name):
            status = 2   # PXI exists but logchan may not be in aditya
        else:
            status = 0
            print(f'Shot no. {shot_no} is not exist')

    return dir_name, status, OS_ID
