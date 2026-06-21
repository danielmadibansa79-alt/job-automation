import time
import subprocess

print("🚀 Cloud job automation started")

while True:
    print("Running scraper + sheets sync...")

    subprocess.run(["python", "send_to_sheets.py"])

    print("Sleeping for 24 hours...")
    time.sleep(86400)