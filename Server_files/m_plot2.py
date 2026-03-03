# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:47:19 2026

@author: Harsh
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from config import load_config



from Server_files.shot import shot
from Server_files.save_data import save_data
from Server_files.pr_window import pr_window
from Server_files.s_plot2 import s_plot2
from scipy.io import savemat
import pandas as pd

def m_plot2(shot_no, *args):

    shot(shot_no)

    from Server_files import p_global
    shot_no = p_global.shot_no   # ← IMPORTANT FIX

    if len(args) < 1:
        print("Usage: m_plot(shot_no, chan1, chan2, ...)")
        return

    channels = list(args)

  #  plt.figure()
   # pr_window(len(channels))

   # for i, ch in enumerate(channels):
   #     s_plot2(i + 1, ch)
    #plt.show() 


    save_and_report_missing(shot_no, channels)
    
def save_and_report_missing(shot_no, channels):

    config = load_config()
    save_root = config["server_folder"]

    missing = []
    raw = []

    for ch in channels:

        try:
            t, y, s = save_data(ch)

            if (len(t) == 0) or (len(y) == 0) or (len(t) < 2) or np.all(np.isnan(y)):

                missing.append(f'Ch{ch}')
                raw.append({'name': f'Ch{ch}', 'time': [], 'data': []})

            else:
                raw.append({
                    'name': f'Ch{ch}_{s["chan_label"].strip()}',
                    'time': np.array(t).flatten(),
                    'data': np.array(y).flatten()
                })

        except Exception:
            missing.append(f'Ch{ch}')
            raw.append({'name': f'Ch{ch}', 'time': [], 'data': []})

    valid_idx = [i for i, r in enumerate(raw) if len(r['time']) > 0]

    if len(valid_idx) == 0:
        print(f"Shot {shot_no} : No valid diagnostics available")
        return

    tmin = np.inf
    tmax = -np.inf
    dt = raw[valid_idx[0]]['time'][1] - raw[valid_idx[0]]['time'][0]

    for i in valid_idx:
        tmin = min(tmin, np.min(raw[i]['time']))
        tmax = max(tmax, np.max(raw[i]['time']))

    Time = np.arange(tmin, tmax + dt, dt)

    Data = np.full((len(Time), len(raw)), np.nan)

    for i in valid_idx:
        f = interp1d(
            raw[i]['time'],
            raw[i]['data'],
            kind='linear',
            bounds_error=False,
            fill_value=np.nan
        )
        Data[:, i] = f(Time)

    
    if len(missing) > 0:
        print(f"Shot {shot_no} : Missing diagnostics -> {' '.join(missing)}")
        print("Saving available diagnostics only...")


    os.makedirs(save_root, exist_ok=True)
   

    # Save .mat file (MATLAB compatible)
    mat_path = os.path.join(save_root, f"{shot_no}.mat")
    savemat(mat_path, {'Time': Time, 'Data': Data})

    # Save Excel file
    xls_path = os.path.join(save_root, f"{shot_no}.xlsx")

    
    # Prepare column names from raw diagnostics
    column_names = []

    for r in raw:
        column_names.append(r["name"])

    df = pd.DataFrame(Data, columns=column_names)
    df.insert(0, "Time", Time)

    df.to_excel(xls_path, index=False)

    print(f"Shot {shot_no} saved successfully.")

   
