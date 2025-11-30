#!/usr/bin/env python3
"""
Sub-Task 1: Initialize logging configuration
"""

import logging

# Setup logger
logging.basicConfig(
    filename='process_log.txt',
    filemode='w',  # Overwrite previous log
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Logging initialized successfully.")
print("✅ Logging configuration completed. Check process_log.txt.")
