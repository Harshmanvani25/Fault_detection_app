# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 17:48:20 2026

@author: Harsh
"""
# services/process_manager.py

import multiprocessing
from pipeline.halpha.worker import worker_main


class ProcessManager:
    """
    Handles ML worker process lifecycle.
    """

    def __init__(self):
        self.worker_process = None
        self.result_queue = None

    def start_worker(self, mode, payload):
        """
        Start ML worker process.
        """

        # Always stop existing worker first
        self.stop_worker()

        # Create fresh queue
        self.result_queue = multiprocessing.Queue()

        self.worker_process = multiprocessing.Process(
            target=worker_main,
            args=(mode, payload, self.result_queue)
        )

        self.worker_process.start()

        return self.result_queue

    def stop_worker(self):
        """
        Force terminate worker process.
        """

        if self.worker_process:

            try:
                if self.worker_process.is_alive():
                    self.worker_process.terminate()
                    self.worker_process.join(timeout=2)
            except Exception:
                pass

        # Cleanup references
        self.worker_process = None

        if self.result_queue:
            try:
                self.result_queue.close()
            except Exception:
                pass

            self.result_queue = None

