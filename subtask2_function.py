#!/usr/bin/env python3
"""
Sub-Task 2: Define a process function and test it in the main process.
"""

import logging
import time

# Setup logging again (to ensure fresh run)
logging.basicConfig(
    filename='process_log.txt',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Dummy function
def system_process(task_name):
    logging.info(f"{task_name} started")
    time.sleep(2)
    logging.info(f"{task_name} ended")

# Test the function (no multiprocessing yet)
if __name__ == "__main__":
    print("Running system_process() once...")
    system_process("Test-Process")
    print("✅ Task completed. Check process_log.txt.")
