# logger.py
import datetime
import sys

def log(message):
    """Prints a timestamped log message with emoji and flushes immediately."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] 🔍 DEBUG: {message}", flush=True)
