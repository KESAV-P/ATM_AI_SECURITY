import csv
import os
from datetime import datetime

LOG_FILE = "security_log.csv"

def handle_event(event):
    # Print to console (existing behavior)
    print(
        f"\n🚨 EVENT TRIGGERED\n"
        f"Type     : {event['type']}\n"
        f"Severity : {event['severity']}\n"
        f"Message  : {event['message']}\n"
    )

    # Log to CSV
    file_exists = os.path.isfile(LOG_FILE)
    
    try:
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if new file
            if not file_exists:
                writer.writerow(["Timestamp", "Type", "Severity", "Message"])
            
            # Write event data
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                event['type'],
                event['severity'],
                event['message']
            ])
    except Exception as e:
        print(f"⚠️ Failed to write to log file: {e}")