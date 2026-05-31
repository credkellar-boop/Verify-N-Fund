hdef check_routing_status(routing_number: str) -> dict:
    """
    Simulates a connection to a financial institution routing database (e.g., Fedwire/Certegy API).
    """
    # Example check logic
    if len(routing_number) != 9:
        return {"status": "REJECTED", "reason": "Invalid Routing Number Length"}
        
    # Real-world apps would hit an external database endpoint here
    return {"status": "VERIFIED", "routing_bank": "Example National Bank"}
import re

def evaluate_check_risk(extracted_text: str) -> dict:
    """
    Analyzes the text output from Gemini to assign a risk tier 
    and routing instructions for the teller.
    """
    risk_score = 0
    flags = []
    
    # Lowercase everything for consistent matching
    text_lower = extracted_text.lower()
    
    # Rule 1: Check for explicit mismatches caught by the Vision model
    if "mismatch" in text_lower or "does not match" in text_lower:
        risk_score += 40
        flags.append("Amount or MICR mismatch detected by AI.")
        
    # Rule 2: Check for signature presence
    if "no signature" in text_lower or "missing signature" in text_lower:
        risk_score += 30
        flags.append("Missing payor signature.")
        
    # Rule 3: Look for high-risk phrases or anomalies
    if "anomaly" in text_lower or "blurry" in text_lower or "alteration" in text_lower:
        risk_score += 20
        flags.append("Physical check structure anomalies flagged.")

    # Determine Action and Status Based on Risk Score
    if risk_score >= 50:
        status = "❌ HIGH RISK / REJECTED"
        color = "red"
        instructions = "Do not cash. Hand the check back to the customer or route directly to management for fraud review."
    elif risk_score >= 20:
        status = "⚠️ FLAGGED FOR MANUAL REVIEW"
        color = "oranges"
        instructions = "Call the issuing bank directly using the official bank directory to verify funds and account status."
    else:
        status = "✅ LOW RISK / APPROVED TO FUND"
        color = "green"
        instructions = "Check appears authentic. Proceed with standard cashing and payout procedures."
        
    return {
        "score": risk_score,
        "status": status,
        "color": color,
        "flags": flags,
        "instructions": instructions
    }
