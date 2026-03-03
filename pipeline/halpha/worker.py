# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 17:37:36 2026

@author: Harsh
"""

# pipeline/halpha/worker.py



import time
import os
from pipeline.halpha.predictor import predict_halpha_file
from Server_files.m_plot2 import m_plot2
import glob
import matplotlib
from config import load_config

matplotlib.use("Agg")   # <<< CRITICAL
# p_global = {}

# SERVER_FOLDER = r"/home/minsha/hp_rpi/Server_code_python"


def worker_main(mode, payload, result_queue):
    """
    Multiprocessing entry point.
    Runs in separate process.
    NEVER touches UI.
    """

    try:
        if mode == "local":
            file_paths = payload
        
            if isinstance(file_paths, str):
                file_paths = [file_paths]
        
            total_files = len(file_paths)
        
        elif mode == "server":
            total_files = 1

        batch_stats = {
            "total": total_files,
            "processed": 0,
            "normal": 0,
            "fault": 0,
            "total_time": 0.0,
        }

        batch_start_time = time.perf_counter()
        if mode == "local":

            for index, file_path in enumerate(file_paths, start=1):

                # -------------------------
                # Identify Shot
                # -------------------------
                file_name = os.path.basename(file_path)
                shot_name = os.path.splitext(file_name)[0]
    
                result_queue.put(("active_shot", shot_name))
    
                # -------------------------
                # Stage 1 - Loading
                # -------------------------
                result_queue.put(("stage", "Loading File..."))
                # result_queue.put(("progress", 5))
    
                file_start = time.perf_counter()
    
                # -------------------------
                # Stage 2 - Extracting
                # -------------------------
                result_queue.put(("stage", "Extracting Features..."))
                # result_queue.put(("progress", 30))
    
                # -------------------------
                # Stage 3 - Scaling
                # -------------------------
                result_queue.put(("stage", "Scaling Data..."))
                # result_queue.put(("progress", 60))
    
                # -------------------------
                # Stage 4 - Predicting
                # -------------------------
                result_queue.put(("stage", "Running Model..."))
                # result_queue.put(("progress", 85))
    
                def progress_forward(percent):
    
                    # Map percent ranges to stage labels
                    if percent < 20:
                        stage = "Loading File..."
                    elif percent < 50:
                        stage = "Extracting Features..."
                    elif percent < 85:
                        stage = "Scaling Data..."
                    elif percent < 100:
                        stage = "Running Model..."
                    else:
                        stage = "Completed"
                
                    result_queue.put(("stage", stage))
                    result_queue.put(("progress", percent))
                
                fault = predict_halpha_file(
                    file_path,
                    progress_callback=progress_forward
                )
    
                execution_time = time.perf_counter() - file_start
    
                # -------------------------
                # Stage 5 - Completed
                # -------------------------
                result_queue.put(("stage", "Completed"))
                # result_queue.put(("progress", 100))
    
                # -------------------------
                # Update Stats
                # -------------------------
                batch_stats["processed"] += 1
                batch_stats["total_time"] += execution_time
    
                if str(fault).upper() == "NORMAL":
                    batch_stats["normal"] += 1
                else:
                    batch_stats["fault"] += 1
    
                result_queue.put(
                    ("file_result", shot_name, fault, execution_time)
                )
            result_queue.put(("batch_complete", batch_stats))
        elif mode == "server":

            shot = payload["shot"]
            channels = payload["channels"]
        
            # Snapshot existing Excel files
            config = load_config()
            server_folder = config["server_folder"]
            
            result_queue.put(("stage", "Fetching from server..."))

            m_plot2(shot, *channels)
            # 🔥 Get actual shot number after fetching latest
            from Server_files import p_global
            real_shot = p_global.shot_no

            # Send real shot to GUI
            # Send real shot to GUI
            result_queue.put(("active_shot", real_shot))
            
            config = load_config()
            server_folder = config["server_folder"]
            
            expected_file = os.path.join(server_folder, f"{real_shot}.xlsx")
            
            
            # Wait until file exists (or is updated)
            for _ in range(60):
                if os.path.exists(expected_file):
                    break
                time.sleep(0.5)
            
            if not os.path.exists(expected_file):
                raise RuntimeError("Server did not produce Excel file.")
            
            new_file = expected_file
        
            # Active shot
            shot_name = os.path.splitext(os.path.basename(new_file))[0]
            result_queue.put(("active_shot", shot_name))
        
            file_start = time.perf_counter()
        
            def progress_forward(percent):
        
                if percent < 20:
                    stage = "Loading File..."
                elif percent < 50:
                    stage = "Extracting Features..."
                elif percent < 85:
                    stage = "Scaling Data..."
                elif percent < 100:
                    stage = "Running Model..."
                else:
                    stage = "Completed"
        
                result_queue.put(("stage", stage))
                result_queue.put(("progress", percent))
        
            fault = predict_halpha_file(new_file, progress_callback=progress_forward)
        
            execution_time = time.perf_counter() - file_start
        
            batch_stats["processed"] = 1
            batch_stats["total_time"] = execution_time
        
            if str(fault).upper() == "NORMAL":
                batch_stats["normal"] = 1
            else:
                batch_stats["fault"] = 1
        
            result_queue.put(("file_result", shot_name, fault, execution_time))
            result_queue.put(("batch_complete", batch_stats))
    except Exception as e:
        result_queue.put(("error", str(e)))
