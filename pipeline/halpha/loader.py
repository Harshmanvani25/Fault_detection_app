# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:49:56 2026

@author: Harsh
"""

# pipeline/halpha/loader.py
def prepare_halpha_file(original_file_path):
    """
    Always returns an Excel file containing sheet 'HAlpha'
    with two columns:
        Time_ms | Signal

    Supports:
    - HAlpha sheet
    - Any column containing 'halpha'
    """

    import pandas as pd
    import tempfile

    SHEET_NAME = "HAlpha"

    try:
        excel_file = pd.ExcelFile(original_file_path)
    except Exception as e:
        raise ValueError(f"Invalid Excel file: {e}")

    # =====================================
    # CASE 1: Sheet named HAlpha exists
    # =====================================
    for sheet in excel_file.sheet_names:
        if sheet.strip().lower() == "halpha":
            return original_file_path

    # =====================================
    # OTHERWISE LOAD FIRST SHEET
    # =====================================
    df = pd.read_excel(original_file_path)

    # Remove header if present
    if isinstance(df.iloc[0, 0], str):
        df = df.iloc[1:].reset_index(drop=True)

    # =====================================
    # FIND HAlpha COLUMN (FLEXIBLE MATCH)
    # =====================================
    halpha_candidates = []
    time_candidates = []

    for col in df.columns:
        col_lower = str(col).lower()

        if "halpha" in col_lower:
            halpha_candidates.append(col)

        if "time" in col_lower:
            time_candidates.append(col)

    if len(halpha_candidates) == 0:
        raise ValueError(
            "HAlpha diagnostic not found in Excel file. "
            "Prediction requires HAlpha data."
        )

    if len(halpha_candidates) > 1:
        raise ValueError(
            f"Multiple HAlpha-like columns found: {halpha_candidates}. "
            "Please keep only one HAlpha column."
        )

    if len(time_candidates) == 0:
        raise ValueError("Time column not found in Excel file.")

    halpha_col = halpha_candidates[0]
    time_col = time_candidates[0]

    normalized_df = pd.DataFrame({
        "Time_ms": df[time_col],
        "Signal": df[halpha_col]
    })

    # =====================================
    # WRITE TEMP FILE WITH HAlpha SHEET
    # =====================================
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")

    with pd.ExcelWriter(temp_file.name, engine="openpyxl") as writer:
        normalized_df.to_excel(
            writer,
            sheet_name=SHEET_NAME,
            index=False,
            header=False
        )

    return temp_file.name
# def prepare_halpha_file(original_file_path):
    # """
    # Always returns an Excel file containing sheet 'HAlpha'
    # with two columns:
        # Time_ms | Signal

    # Supports:
    # - HAlpha sheet
    # - HAlpha column
    # - Raw 2-column server files
    # """

    # import pandas as pd
    # import tempfile

    # SHEET_NAME = "HAlpha"

    # try:
        # excel_file = pd.ExcelFile(original_file_path)
    # except Exception as e:
        # raise ValueError(f"Invalid Excel file: {e}")

    # # =====================================
    # # CASE 1: Sheet named HAlpha exists
    # # =====================================
    # if SHEET_NAME in excel_file.sheet_names:
        # return original_file_path

    # # =====================================
    # # OTHERWISE LOAD FIRST SHEET
    # # =====================================
    # df = pd.read_excel(original_file_path)

    # # Remove header if present
    # if isinstance(df.iloc[0, 0], str):
        # df = df.iloc[1:].reset_index(drop=True)

    # # =====================================
    # # CASE 2: Column named HAlpha
    # # =====================================
    # columns_lower = [str(c).lower() for c in df.columns]

    # if "halpha" in columns_lower:
        # halpha_col = df.columns[columns_lower.index("halpha")]
        # time_col = df.columns[0]

        # normalized_df = pd.DataFrame({
            # "Time_ms": df[time_col],
            # "Signal": df[halpha_col]
        # })

    
    # # =====================================
    # # CASE 3: Server format (2-column raw)
    # # =====================================
    # "
    # else:
        # raise ValueError(
            # "HAlpha diagnostic not found in Excel file. "
            # "Prediction requires HAlpha data."
        # )
    

    # # =====================================
    # # WRITE TEMP FILE WITH HAlpha SHEET
    # # =====================================
    # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")

    # with pd.ExcelWriter(temp_file.name, engine="openpyxl") as writer:
        # normalized_df.to_excel(
            # writer,
            # sheet_name=SHEET_NAME,
            # index=False,
            # header=False
        # )

    # return temp_file.name
