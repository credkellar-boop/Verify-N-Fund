import csv
import os
from datetime import datetime

LOG_FILE = "config/audit_log.csv"

def initialize_audit_log():
    """Ensures the audit log database file exists with the proper compliance headers."""
    if not os.path.exists(LOG_FILE):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Teller_ID", "Action_Type", "Risk_Score", "System_Status", "System_Action"])

def log_transaction(teller_id: str, action_type: str, risk_score: int, status: str, action: str):
    """Appends a new compliance verification event to the audit trail ledger."""
    initialize_audit_log()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, teller_id, action_type, risk_score, status, action])
