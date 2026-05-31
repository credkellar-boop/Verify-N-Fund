import pandas as pd
import os

LOG_FILE = "config/audit_log.csv"

def get_analytics_data():
    """Reads the compliance audit log and computes summary metrics for management."""
    if not os.path.exists(LOG_FILE):
        return None
        
    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty:
            return None
            
        # Calculate key business metrics
        total_scans = len(df[df["Action_Type"] == "IMAGE_SCAN_OCR"])
        total_queries = len(df[df["Action_Type"] == "KB_QUERY"])
        
        # Count risk distributions
        high_risk_count = len(df[df["System_Status"].str.contains("HIGH RISK", na=False)])
        review_count = len(df[df["System_Status"].str.contains("MANUAL REVIEW", na=False)])
        approved_count = len(df[df["System_Status"].str.contains("APPROVED", na=False)])
        
        return {
            "df": df,
            "total_scans": total_scans,
            "total_queries": total_queries,
            "high_risk": high_risk_count,
            "review": review_count,
            "approved": approved_count
        }
    except Exception:
        return None
