# -*- coding: utf-8 -*-
"""
save_data.py
Converted from save_data.m
Original Written/modified by V. K. Panchal  23-Feb-2017
Python conversion without changing functionality
"""

import os
import numpy as np
from Server_files import p_global
from Server_files.msdur import msdur
from Server_files.nsavpeak import npltpeak


def save_data(Logical_Channel_No):

    # =============================================================
    # MATLAB GLOBAL VARIABLES (Access through p_global)
    # =============================================================
    shot_no = p_global.shot_no
    shot_return_status = p_global.shot_return_status
    log_struct = p_global.log_struct
    dir_name = p_global.dir_name
    OS_ID = p_global.OS_ID
    module_string = p_global.module_string
    head_string = p_global.head_string
    data_string = p_global.data_string

    X_Data = np.array([])
    Y_Data = np.array([])
    ret_struct = {}

    # =============================================================
    # SHOT VALIDATION (Same as MATLAB)
    # =============================================================
    if shot_no is None or len(str(shot_no)) == 0:
        print('First define valid shot no. using shot(shot_no)')
        return X_Data, Y_Data, ret_struct

    if shot_return_status is None:
        print('First define valid shot no. using shot(shot_no)')
        return X_Data, Y_Data, ret_struct

    if shot_return_status < 0:
        return X_Data, Y_Data, ret_struct

    if shot_return_status != 1:
        print('First select valid shot no. using --->> shot(shot_no)')
        return X_Data, Y_Data, ret_struct

    # =============================================================
    # INPUT VALIDATION
    # =============================================================
    if Logical_Channel_No is None:
        print(' Give like --> [Out_X,Out_Y]=save_data(Logical_Channel_No); ')
        print(' Shot no. should be selected using `shot(shot_no)` before ')
        print(' giving this function ')
        return X_Data, Y_Data, ret_struct

    TempCh = Logical_Channel_No
    Calibration_ON = np.sign(TempCh)
    TempCh = abs(TempCh)

    # =============================================================
    # FIND LOGICAL CHANNEL
    # =============================================================
    index_of_log_ch = [
        i for i, s in enumerate(log_struct)
        if s['log_no'] == TempCh
    ]

    if len(index_of_log_ch) == 0:
        if TempCh < 700:
            print(f'Logical channel {Logical_Channel_No} data is not found for shot {shot_no}')
        return X_Data, Y_Data, ret_struct

    I = index_of_log_ch[0]
    ret_struct = log_struct[I].copy()
    # =============================================================
    # ONLY PHYSICAL CHANNELS (<700)
    # =============================================================
    if TempCh < 700:

        vltime = 0

        vltime_filename = os.path.join(dir_name, 'vltime.dat')
        if os.path.exists(vltime_filename):
            try:
                vltime = np.loadtxt(vltime_filename)
            except:
                vltime = 0

        # ---------------------------------------------------------
        # ipfact.set reading
        # ---------------------------------------------------------
        ipfact_file = os.path.join(dir_name, 'ipfact.set')

        if os.path.exists(ipfact_file):
            try:
                factor_ip = np.loadtxt(ipfact_file)
                fact_ip6 = factor_ip[1]
                fact_ip5 = factor_ip[3]
                fact_ip7 = factor_ip[5]
            except:
                fact_ip5 = -8.73
                fact_ip6 = -8.91
                fact_ip7 = 31.84
        else:
            fact_ip5 = -8.73
            fact_ip6 = -8.91
            fact_ip7 = 31.84

        t_dir_name = dir_name

        # ---------------------------------------------------------
        # PXI MODULE
        # ---------------------------------------------------------
        #if log_struct[I]['mod_type'] == 9:

         #   pxidir_name = dir_name.replace('aditya', 'pxi/aditya data/sht')

        #    if not os.path.isdir(pxidir_name):
        #        pxidir_name = dir_name.replace('aditya', 'pxi')

         #   t_dir_name = pxidir_name
        # ---------------- PXI -------------------
        if log_struct[I]['mod_type'] == 9:

            # Replace /aditya/ with /pxi/
            pxidir_name = dir_name.replace('/aditya/', '/pxi/')

            if os.path.isdir(pxidir_name):
                t_dir_name = pxidir_name
            else:
                print(f'Shot {shot_no} : PXI directory not found')
                return X_Data, Y_Data, ret_struct

        # ---------------------------------------------------------
        # SBC MODULE
        # ---------------------------------------------------------
        
        if log_struct[I]['mod_type'] == 10:

            # Exact Linux SBC64 storage path
            sbcdir_name = dir_name.replace(
                '/data/aditya/',
                '/mdsdata/rach_sbc/sbc64/'
            )

            t_dir_name = sbcdir_name

        # ---------------------------------------------------------
        # HEADER & DATA FILE NAMES
        # ---------------------------------------------------------
        HeaderFile = os.path.join(
            t_dir_name,
            f"{head_string[log_struct[I]['mod_type']-1]}{log_struct[I]['mod_no']}.bin"
        )

        DataFile = os.path.join(
            t_dir_name,
            f"{data_string[log_struct[I]['mod_type']-1]}{log_struct[I]['chan_no']}.bin"
        )

        TLogChanNo = TempCh
        TModuleNam = module_string[log_struct[I]['mod_type']-1]
        TModuleChanNo = log_struct[I]['chan_no']
        TChanLabel = log_struct[I]['chan_label']
        TSignFactor = log_struct[I]['data_sign']
        TCalibFactor = log_struct[I]['calib_factor']

        mod_type = log_struct[I]['mod_type']
        # =============================================================
        # HEADER FILE READING (Exact MATLAB Logic)
        # =============================================================

        if not os.path.exists(HeaderFile):
            print(f'Shot {shot_no} : Header file for {TModuleNam} Module {log_struct[I]["mod_no"]} not found')
            return X_Data, Y_Data, ret_struct

        with open(HeaderFile, 'rb') as fid:

            # ---------------------------------------------------------
            # MODULE TYPE 1 : 8212_32
            # ---------------------------------------------------------
            if mod_type == 1:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.int32, count=1)[0]

                if ModuleFreq == 200:
                    ModuleFreq = 0.2

                PreTrigSamp  = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                NoOfChannels = np.fromfile(fid, dtype=np.int32, count=1)[0]

            # ---------------------------------------------------------
            # MODULE TYPE 2 : 8212_8
            # ---------------------------------------------------------
            elif mod_type == 2:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.float32, count=1)[0]
                PreTrigSamp  = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                NoOfChannels = np.fromfile(fid, dtype=np.int32, count=1)[0]

            # ---------------------------------------------------------
            # MODULE TYPE 3 : CA5548
            # ---------------------------------------------------------
            elif mod_type == 3:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.int16, count=1)[0]
                PreTrigSamp  = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                NoOfChannels = np.fromfile(fid, dtype=np.int16, count=1)[0]

                if ModuleFreq == 0:
                    ModuleFreq = 0.5

                if ModuleFreq == 999:
                    print(f'Shot {shot_no} : INCAA Module {log_struct[I]["mod_no"]}, external clock was set')
                    ModuleFreq = float(input('Enter freq. : '))

            # ---------------------------------------------------------
            # MODULE TYPE 4 : 8210
            # ---------------------------------------------------------
            elif mod_type == 4:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.int16, count=1)[0]
                PreTrigSamp  = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                NoOfChannels = np.fromfile(fid, dtype=np.int32, count=1)[0]

            # ---------------------------------------------------------
            # MODULE TYPE 5 & 6 : IPRMOD_B / IPRMOD_U
            # ---------------------------------------------------------
            elif mod_type == 5 or mod_type == 6:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.float32, count=1)[0]
                PreTrigSamp  = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                BitResolution = np.fromfile(fid, dtype=np.int16, count=1)[0]
                NoOfChannels  = np.fromfile(fid, dtype=np.int16, count=1)[0]

            # ---------------------------------------------------------
            # MODULE TYPE 7 : VMEVTR812 (BIG ENDIAN)
            # ---------------------------------------------------------
            elif mod_type == 7:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype='>f4', count=1)[0]
                V_Offset  = np.fromfile(fid, dtype='>f4', count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype='>f4', count=1)[0]
                PreTrigSamp  = np.fromfile(fid, dtype='>i4', count=1)[0]
                PostTrigSamp = np.fromfile(fid, dtype='>i4', count=1)[0]
                NoOfChannels = np.fromfile(fid, dtype='>i2', count=1)[0]

            # ---------------------------------------------------------
            # MODULE TYPE 8 : VMEALPHI (Always error in MATLAB)
            # ---------------------------------------------------------
            elif mod_type == 8:

                print(f'Shot {shot_no} : Header file for {TModuleNam} Module {log_struct[I]["mod_no"]} not found')
                return X_Data, Y_Data, ret_struct

            # ---------------------------------------------------------
            # MODULE TYPE 9 : PXI
            # ---------------------------------------------------------
            elif mod_type == 9:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.float32, count=1)[0]
                PreTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                TotalSamp   = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = TotalSamp - PreTrigSamp
                NoOfChannels = np.fromfile(fid, dtype=np.int16, count=1)[0]

                Shot_No = Shot_No[1:7]

                try:
                    shot_int = int(b''.join(Shot_No).decode().strip())
                except:
                    shot_int = 0

                if 29906 <= shot_int <= 30150:
                    V_Scale = 0.000305176

                NoOfChannels = 8
                Shot_Date = Shot_Date[1:24]

            # ---------------------------------------------------------
            # MODULE TYPE 10 : SBC64
            # ---------------------------------------------------------
            elif mod_type == 10:

                Shot_No   = np.fromfile(fid, dtype='S1', count=7)
                Shot_Date = np.fromfile(fid, dtype='S1', count=24)
                V_Scale   = np.fromfile(fid, dtype=np.float32, count=1)[0]
                V_Offset  = np.fromfile(fid, dtype=np.float32, count=1)[0]
                ModuleFreq = np.fromfile(fid, dtype=np.float32, count=1)[0]
                PreTrigSamp = np.fromfile(fid, dtype=np.int32, count=1)[0]
                TotalSamp   = np.fromfile(fid, dtype=np.int32, count=1)[0]
                PostTrigSamp = TotalSamp - PreTrigSamp
                NoOfChannels = np.fromfile(fid, dtype=np.int16, count=1)[0]

                NoOfChannels = 64
                Shot_No = Shot_No[1:7]
                Shot_Date = Shot_Date[1:24]
        # =============================================================
        # DATA FILE READING (Exact MATLAB Behaviour)
        # =============================================================

        if not os.path.exists(DataFile):
            print(f'Shot {shot_no} : Data file for logical channel {log_struct[I]["log_no"]} not found')
            return X_Data, Y_Data, ret_struct

        # -------------------------------------------------------------
        # MODULE TYPE 1–4  (short)
        # -------------------------------------------------------------
        if 1 <= mod_type <= 4:

            if OS_ID == 1:
                fid = open(DataFile, 'rb')
            else:
                fid = open(DataFile, 'rb')

            ch = np.fromfile(fid, dtype=np.int16)
            Y_Data = (ch * V_Scale) + V_Offset
            fid.close()

        # -------------------------------------------------------------
        # MODULE TYPE 5–6 (BitResolution dependent)
        # -------------------------------------------------------------
        elif mod_type == 5 or mod_type == 6:

            if OS_ID == 1:
                fid = open(DataFile, 'rb')
            else:
                fid = open(DataFile, 'rb')

            if BitResolution == 8:
                # MATLAB: fread(fid,'uchar')
                ch = np.fromfile(fid, dtype=np.uint8)
            else:
                ch = np.fromfile(fid, dtype=np.int16)

            # MATLAB multiplies by 2
            Y_Data = ((ch * V_Scale) + V_Offset) * 2
            fid.close()

        # -------------------------------------------------------------
        # MODULE TYPE 7 (BIG ENDIAN SHORT)
        # -------------------------------------------------------------
        elif mod_type == 7:

            if OS_ID == 1:
                fid = open(DataFile, 'rb')
            else:
                fid = open(DataFile, 'rb')

            ch = np.fromfile(fid, dtype='>i2')
            Y_Data = (ch * V_Scale) + V_Offset
            fid.close()

        # -------------------------------------------------------------
        # MODULE TYPE 9–10 (short)
        # -------------------------------------------------------------
        elif mod_type == 9 or mod_type == 10:

            if OS_ID == 1:
                fid = open(DataFile, 'rb')
            else:
                fid = open(DataFile, 'rb')

            ch = np.fromfile(fid, dtype=np.int16)
            Y_Data = (ch * V_Scale) + V_Offset
            fid.close()

        else:
            print(f'Shot {shot_no} : Data file for logical channel {log_struct[I]["log_no"]} not found')
            return X_Data, Y_Data, ret_struct
        # =============================================================
        # DATA PROCESSING (Exact MATLAB Behaviour)
        # =============================================================

        # MATLAB:
        # Shot_Date=setstr(Shot_Date);
        # Shot_No = sprintf('%6s',Shot_No(1:6));

        Shot_Date = b''.join(Shot_Date).decode(errors='ignore')
        Shot_No = b''.join(Shot_No).decode(errors='ignore')

        Shot_No = Shot_No[:6].rjust(6)

        # MATLAB:
        # Top_Title=strcat({'Shot: '},Shot_No,{'  '},Shot_Date(1:23));
        Top_Title = f"Shot: {Shot_No}  {Shot_Date[:23]}"

        # MATLAB:
        # DeltaTime=1/ModuleFreq;
        DeltaTime = 1.0 / ModuleFreq

        # MATLAB:
        # X_Data=(((-PreTrigSamp+1):1:PostTrigSamp)/ModuleFreq)-vltime;
        X_Data = (np.arange(-PreTrigSamp + 1, PostTrigSamp + 1) / ModuleFreq) - vltime

        # MATLAB:
        # X_Data=X_Data';
        X_Data = X_Data.reshape(-1, 1)

        # Store in return structure
        ret_struct = log_struct[I].copy()
        ret_struct['freq'] = ModuleFreq
        ret_struct['top_t'] = Top_Title
        ret_struct['ModuleName'] = module_string[mod_type - 1]

        # -------------------------------------------------------------
        # SIGN CORRECTION
        # MATLAB: Y_Data = Y_Data * TSignFactor;
        # -------------------------------------------------------------
        Y_Data = Y_Data * TSignFactor

        # -------------------------------------------------------------
        # IP CHANNEL 5 & 6 (Integration)
        # -------------------------------------------------------------
        if (Calibration_ON == 1) and (TLogChanNo == 5 or TLogChanNo == 6):

            # MATLAB:
            # if (str2num(Shot_No) > 29905)
            #    PreTrigSamp=180;
            if int(Shot_No.strip()) > 29905:
                PreTrigSamp = 180

            # MATLAB:
            # IP_Offset=mean(Y_Data(1:PreTrigSamp));
            IP_Offset = np.mean(Y_Data[0:PreTrigSamp])

            # MATLAB:
            # IP56_Data=Y_Data-IP_Offset;
            IP56_Data = Y_Data - IP_Offset

            # MATLAB:
            # Y_Data=(cumsum(IP56_Data))*DeltaTime;
            Y_Data = np.cumsum(IP56_Data) * DeltaTime

        # -------------------------------------------------------------
        # IP CHANNEL 7 (No Integration)
        # -------------------------------------------------------------
        if (Calibration_ON == 1) and (TLogChanNo == 7):

            if int(Shot_No.strip()) > 29905:
                PreTrigSamp = 180

            IP_Offset = np.mean(Y_Data[0:PreTrigSamp])
            IP7_Data = Y_Data - IP_Offset
            Y_Data = IP7_Data

            # MATLAB:
            # if ( (str2num(Shot_No) <= 30268) & (str2num(Shot_No) >= 29906) )
            #    TCalibFactor=57.24;
            if 29906 <= int(Shot_No.strip()) <= 30268:
                TCalibFactor = 57.24

        # -------------------------------------------------------------
        # GENERAL CALIBRATION
        # MATLAB:
        # if (Calibration_ON == 1)
        #    Y_Data=Y_Data*TCalibFactor;
        # -------------------------------------------------------------
        if Calibration_ON == 1:
            Y_Data = Y_Data * TCalibFactor
    # =============================================================
    # DENSITY CHANNELS (700–708)
    # MATLAB A1 density processing block
    # =============================================================
    elif (TempCh >= 700) and (TempCh <= 708):

        if len(index_of_log_ch) == 0:
            return X_Data, Y_Data, ret_struct

        dlab = log_struct[index_of_log_ch[0]]['chan_label']
        map_name = 'density'
        data_server = 'adserver'

        # MATLAB:
        # if ((TempCh >= 701) & (TempCh <= 704))
        #    TModuleChanNo=TempCh-380;
        # else
        #    TModuleChanNo=TempCh-376;
        if 701 <= TempCh <= 704:
            TModuleChanNo = TempCh - 380
        else:
            TModuleChanNo = TempCh - 376

        dench = TModuleChanNo

        # MATLAB:
        # [ib0,ib31,s1]=save_data(dench);
        ib0, ib31, s1 = save_data(dench)

        # MATLAB:
        # dench=dench-300;
        dench = dench - 300

        # MATLAB:
        # [xT,yT]=msdur(ib0,ib31,0,2.5);
        xT, yT = msdur(ib0, ib31, 0, 2.5)

        yTmin = np.min(yT)
        yTmax = np.max(yT)

        # MATLAB:
        # if abs(yTmin) > abs(yTmax)
        #    fact_density=sign(yTmax);
        # else
        #    fact_density=sign(yTmin);
        if abs(yTmin) > abs(yTmax):
            fact_density = np.sign(yTmax)
        else:
            fact_density = np.sign(yTmin)

        # MATLAB:
        # ib31=fact_density*ib31;
        ib31 = fact_density * ib31

        # -------------------------------------------------------------
        # Load peak file (exact MATLAB path logic)
        # -------------------------------------------------------------
        if int(shot_no) <= 9999:

            if OS_ID == 1:
                file_name = f"{deli_style}{deli_style}{data_server}{deli_style}{map_name}{deli_style}p{dench}_{shot_no}.dat"
            else:
                file_name = f"{deli_style}{data_server}{deli_style}{map_name}{deli_style}p{dench}_{shot_no}.dat"

        else:

            if OS_ID == 1:
                file_name = f"{deli_style}{deli_style}{data_server}{deli_style}{map_name}{deli_style}p{dench}{shot_no}.dat"
            else:
                file_name = f"{deli_style}{data_server}{deli_style}{map_name}{deli_style}p{dench}{shot_no}.dat"

        if not os.path.exists(file_name):
            print(f"Aditya {shot_no} - No Peak points {dlab}")
            return X_Data, Y_Data, ret_struct

        data = np.loadtxt(file_name)
        pos = data[:, 0]
        peak = data[:, 1]

        # MATLAB:
        # ib31=ib31';
        ib31 = ib31.reshape(-1, 1)

        # MATLAB:
        # [xden,yden]=nsavpeak(pos,peak,ib0,ib31);
        xden, yden = npltpeak(pos, peak, ib0, ib31)

        # MATLAB:
        # yden=yden*1.0e+12;
        yden = yden * 1.0e+12

        # MATLAB:
        # non_zero=find(xden ~= 0);
        non_zero = np.where(xden != 0)[0]

        # MATLAB:
        # X_Data=xden(non_zero);
        # Y_Data=yden(non_zero)';
        X_Data = xden[non_zero]
        Y_Data = yden[non_zero]

        # MATLAB:
        # s1.chan_label=dlab; ret_struct=s1;
        s1['chan_label'] = dlab
        ret_struct = s1
    # =============================================================
    # POSITION DELR (709) & DELY (710)
    # MATLAB Position DELR and DELY block
    # =============================================================
    elif (TempCh == 710) or (TempCh == 709):

        # MATLAB:
        # [lb0,p1]=save_data(-8);
        # [lb0,p2]=save_data(-9);
        # [lb0,p3]=save_data(-10);
        # [lb0,p4]=save_data(-11);
        # [lb0,p8]=save_data(-7);
        lb0, p1, _ = save_data(-8)
        lb0, p2, _ = save_data(-9)
        lb0, p3, _ = save_data(-10)
        lb0, p4, _ = save_data(-11)
        lb0, p8, _ = save_data(-7)

        # MATLAB:
        # lpre=find(lb0==0); lpre=lpre(1);
        #lpre = np.where(lb0 == 0)[0][0]
        zero_idx = np.where(np.isclose(lb0, 0))[0]

        if len(zero_idx) == 0:
            print(f"Shot {shot_no} : No zero time index found")
            return X_Data, Y_Data, ret_struct

        lpre = zero_idx[0]

        # MATLAB offset removal
        v1 = p1 - np.mean(p1[lpre-100:lpre])
        v2 = p2 - np.mean(p2[lpre-100:lpre])
        v3 = p3 - np.mean(p3[lpre-100:lpre])
        v4 = p4 - np.mean(p4[lpre-100:lpre])
        v8 = p8 - np.mean(p8[lpre-100:lpre])

        # MATLAB:
        # v8=v8*2*15920;
        v8 = v8 * 2 * 15920

        # MATLAB:
        # X_Data=lb0;
        X_Data = lb0

        # ---------------------------------------------------------
        # DELY (710) — Vertical displacement (eta)
        # ---------------------------------------------------------
        if TempCh == 710:

            # MATLAB:
            # vc = 0.5*(v1+v2);
            # vd = 0.5*(v3+v4);
            vc = 0.5 * (v1 + v2)
            vd = 0.5 * (v3 + v4)

            # MATLAB:
            # vvert = vc - vd;
            vvert = vc - vd

            # MATLAB:
            # eta = (2.42e+07/1560.0)*vvert./v8;
            eta = (2.42e+07 / 1560.0) * vvert / v8

            # MATLAB:
            # Y_Data=eta*25.0;
            Y_Data = eta * 25.0

        # ---------------------------------------------------------
        # DELR (709) — Radial displacement (zeta)
        # ---------------------------------------------------------
        if TempCh == 709:

            # MATLAB:
            # [lb0,p6]=save_data(-12);
            # [lb0,p7]=save_data(-13);
            lb0, p6, _ = save_data(-12)
            lb0, p7, _ = save_data(-13)

            v6 = p6 - np.mean(p6[lpre-100:lpre])
            v7 = p7 - np.mean(p7[lpre-100:lpre])

            # MATLAB:
            # va = 0.5*(v1+v4);
            # vb = 0.5*(v2+v3);
            va = 0.5 * (v1 + v4)
            vb = 0.5 * (v2 + v3)

            # MATLAB:
            # vrad = vb - va;
            vrad = vb - va

            # MATLAB terms
            term1 = (1.0865e+07 / 1560.0) * vrad / v8
            term2 = (2.2670e+07 / 1560.0) * v7 / v8
            term3 = (9.9630e+05 * 0.01575) * v6 / v8

            # MATLAB:
            # zeta = ( term1 - term2 + term3 - 0.0632 ) * 25.0 ;
            zeta = (term1 - term2 + term3 - 0.0632) * 25.0

            Y_Data = zeta
    return X_Data, Y_Data, ret_struct
