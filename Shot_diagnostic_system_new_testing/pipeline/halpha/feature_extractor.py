# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:33:58 2026

@author: Harsh
"""

import pandas as pd
import numpy as np
import pywt


# =================================================
# PARAMETERS (LOCKED – MUST MATCH TRAINING)
# =================================================

SHEET_NAME = "HAlpha"

START_TIME = 0.0
TOTAL_SAMPLES = 1500

WINDOW_SIZE = 100
HOP_SIZE = 80

RMS_FEATURE_SAMPLES = 700

WAVELET = "bior2.2"
LEVEL = 4


# =================================================
# BASIC DSP UTILITIES
# =================================================

def rms(x):
    return np.sqrt(np.mean(x**2))


def extract_wavelet_trend(signal, wavelet, level):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    A_L = coeffs[0]
    Ds = coeffs[1:]

    coeffs_trend = [A_L] + [np.zeros_like(d) for d in Ds]
    trend = pywt.waverec(coeffs_trend, wavelet)

    return trend[:len(signal)]


def compute_ader(signal):
    """
    Approximation–Detail Energy Ratio (ADER)
    """
    coeffs = pywt.wavedec(signal, WAVELET, level=LEVEL)

    A_L = coeffs[0]
    Ds = coeffs[1:]

    energy_A = np.sum(A_L ** 2)
    energy_D = np.sum([np.sum(d ** 2) for d in Ds])

    return energy_A / (energy_D + 1e-12)


def zero_crossing_rate(x):
    """
    Zero Crossing Rate on raw signal
    """
    return np.mean(np.diff(np.sign(x)) != 0)


# =================================================
# RMS FEATURE (EXACT LOGIC – DO NOT MODIFY)
# =================================================

def compute_rms_ratio_feature_exact(file_path):
    #df = pd.read_excel(file_path, sheet_name=SHEET_NAME)
    df = load_halpha_data(file_path)
    time_excel = df.iloc[:, 0].values
    #signal_full = df.iloc[:, 1].values
    signal_full = df.iloc[:, 1].values.copy()
    zero_index = np.argmin(np.abs(time_excel))

    end_index = min(zero_index + RMS_FEATURE_SAMPLES, len(signal_full))
    signal = signal_full[zero_index:end_index]

    trend = extract_wavelet_trend(signal, WAVELET, LEVEL)
    noise = signal - trend

    rms_feature_windows = []
    N = len(signal)

    for start in range(0, N - WINDOW_SIZE + 1, HOP_SIZE):
        sig_w = signal[start:start + WINDOW_SIZE]
        noise_w = noise[start:start + WINDOW_SIZE]

        rms_feat = rms(noise_w) / (rms(sig_w) + 1e-12)
        rms_feature_windows.append(rms_feat)

    return np.mean(rms_feature_windows)


# =================================================
# MAIN FEATURE EXTRACTION FUNCTION (USED BY GUI)
# =================================================
def load_halpha_data(file_path):
    """
    Supports:
    1) Multi-sheet format (sheet name = HAlpha)
    2) Single-sheet multi-column format
    """

    xls = pd.ExcelFile(file_path)

    # --------------------------------------
    # CASE 1: Multi-sheet format
    # --------------------------------------
    for sheet in xls.sheet_names:
        if sheet.strip().lower() == "halpha":
            df = pd.read_excel(file_path, sheet_name=sheet, header=None)

            if isinstance(df.iloc[0, 0], str):
                df = df.iloc[1:].reset_index(drop=True)

            df.columns = ["Time_ms", "Signal"]
            return df

    # --------------------------------------
    # CASE 2: Single-sheet multi-column format
    # --------------------------------------
    df = pd.read_excel(file_path)
    time_candidates = []
    halpha_candidates = []

    for col in df.columns:
        col_lower = str(col).lower()

        if "time" in col_lower:
            time_candidates.append(col)

        if "halpha" in col_lower:
            halpha_candidates.append(col)

    if len(halpha_candidates) == 0:
        raise ValueError("HAlpha diagnostic not found in Excel file.")

    if len(halpha_candidates) > 1:
        raise ValueError(
            f"Multiple HAlpha-like columns found: {halpha_candidates}. "
            "Please ensure only one HAlpha column exists."
        )

    if len(time_candidates) == 0:
        raise ValueError("Time column not found in Excel file.")

    # Use first time column
    time_col = time_candidates[0]
    halpha_col = halpha_candidates[0]
    

    if halpha_col is None:
        raise ValueError("HAlpha diagnostic not found in Excel file.")

    if time_col is None:
        raise ValueError("Time column not found in Excel file.")

    df = df[[time_col, halpha_col]].copy()
    df.columns = ["Time_ms", "Signal"]

    return df

# def extract_features_from_excel(file_path):
def extract_features_from_excel(file_path, progress_callback=None):
    """
    Returns
    -------
    np.array of shape (1, 4)

    [ mean_mean,
      rms_ratio_mean,
      ader,
      zcr_raw ]
    """
    # -----------------------------
    # LOAD EXCEL (ROBUST FORMAT SUPPORT)
    # -----------------------------
    try:
        df = load_halpha_data(file_path)
    except Exception as e:
        raise ValueError(str(e))

    if progress_callback:
        progress_callback(25)

    df.sort_values("Time_ms", inplace=True)
    df.reset_index(drop=True, inplace=True)

    if progress_callback:
        progress_callback(30)

    
    # -----------------------------
    # HEADER CLEANING
    # -----------------------------
    #if isinstance(df.iloc[0, 0], str):
     #   df = df.iloc[1:].reset_index(drop=True)

    #df.columns = ["Time_ms", "Signal"]
    df.sort_values("Time_ms", inplace=True)
    df.reset_index(drop=True, inplace=True)
    if progress_callback:
        progress_callback(30)
    # -----------------------------
    # FIND START INDEX (0 ms)
    # -----------------------------
    time_array = df["Time_ms"].values
    start_idx = np.argmin(np.abs(time_array - START_TIME))

    if start_idx + TOTAL_SAMPLES > len(df):
        raise ValueError("Not enough samples after 0 ms")

    #signal = df.iloc[
     #   start_idx:start_idx + TOTAL_SAMPLES, 1
   # ].values
    signal = df.iloc[start_idx:start_idx + TOTAL_SAMPLES, 1].values.copy()
    if progress_callback:
        progress_callback(40)
    # =================================================
    # FEATURE 1: mean_mean
    # =================================================
    window_means = []

    for start in range(0, TOTAL_SAMPLES - WINDOW_SIZE + 1, HOP_SIZE):
        sig_w = signal[start:start + WINDOW_SIZE]
        window_means.append(np.mean(sig_w))

    mean_mean = np.mean(window_means)
    if progress_callback:
        progress_callback(65)
    # =================================================
    # FEATURE 2: RMS Ratio Mean
    # =================================================
    rms_ratio_mean = compute_rms_ratio_feature_exact(file_path)
    if progress_callback:
        progress_callback(75)
    # =================================================
    # FEATURE 3: ADER
    # =================================================
    ader = compute_ader(signal)
    if progress_callback:
        progress_callback(82)
    # =================================================
    # FEATURE 4: ZCR (RAW)
    # =================================================
    zcr_raw = zero_crossing_rate(signal)

    # =================================================
    # RETURN FEATURE VECTOR (SHAPE = 1 x 4)
    # =================================================
    return np.array([[mean_mean,
                      rms_ratio_mean,
                      ader,
                      zcr_raw]])
