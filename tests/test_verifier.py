import pytest
from src.verifier import evaluate_check_risk

def test_low_risk_check():
    """Test that a clean AI extraction results in an approved status."""
    sample_text = "Bank: Chase. Check #1024. Routing: 123456789. Account: 987654321. Status: Amounts match. Signature: Present."
    result = evaluate_check_risk(sample_text)
    
    assert "APPROVED" in result["status"]
    assert result["score"] == 0
    assert len(result["flags"]) == 0

def test_missing_signature():
    """Test that a missing signature flags the check correctly."""
    sample_text = "Bank: Chase. Check #1024. Routing: 123456789. Account: 987654321. Status: Amounts match. Signature: Missing signature detected."
    result = evaluate_check_risk(sample_text)
    
    assert "FLAGGED" in result["status"]
    assert "Missing payor signature." in result["flags"]

def test_high_risk_mismatch():
    """Test that severe anomalies or text mismatches trigger a rejection."""
    sample_text = "Bank: Unknown. Check #1024. Mismatch detected between written text and numeric box. Signature: Missing signature."
    result = evaluate_check_risk(sample_text)
    
    assert "REJECTED" in result["status"]
    assert result["score"] >= 50
