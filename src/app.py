import streamlit as st
from gemini_agent import query_verify_agent, scan_check_image
from verifier import evaluate_check_risk
from database import log_transaction
from analytics import get_analytics_data  # <-- NEW

st.set_page_config(page_title="Verify-N-Fund Dashboard", page_icon="🏦", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["teller_id"] = ""
    st.session_state["is_manager"] = False  # <-- NEW

if not st.session_state["authenticated"]:
    st.title("🏦 Verify-N-Fund Access Gateway")
    st.write("Authorized Employee Portal. Please sign in to activate the system.")
    
    teller_input = st.text_input("Teller ID / Employee Code:")
    pin_input = st.text_input("Security PIN / Password:", type="password")
    
    if st.button("Authorize Session", type="primary"):
        # Set manager privileges if login is administrative
        if teller_input.strip().upper() == "ADMIN" and pin_input == "9999":
            st.session_state["authenticated"] = True
            st.session_state["teller_id"] = "Manager_Admin"
            st.session_state["is_manager"] = True
            st.rerun()
        elif teller_input.strip() != "" and pin_input == "1234": 
            st.session_state["authenticated"] = True
            st.session_state["teller_id"] = teller_input
            st.session_state["is_manager"] = False
            st.rerun()
        else:
            st.error("Invalid Employee Credentials. Access Denied.")
    st.stop()

# --- MAIN DASHBOARD ---
st.title("🏦 Verify-N-Fund")
st.caption(f"Active Session: User {st.session_state['teller_id']} | Security Protocol Active")

if st.sidebar.button("Logout / Lock Terminal"):
    st.session_state["authenticated"] = False
    st.session_state["teller_id"] = ""
    st.session_state["is_manager"] = False
    st.rerun()

# Build navigation tabs dynamically based on user role
tabs_list = ["📸 Scan Check Image", "❓ Ask a Question"]
if st.session_state["is_manager"]:
    tabs_list.append("📊 Management Analytics")

tabs = st.tabs(tabs_list)

# --- TAB 1 & TAB 2 LOGIC (Keep exactly as before) ---
with tabs[0]:
    st.markdown("### High-Speed Vision Scanner")
    uploaded_check = st.file_uploader("Upload check image...", type=["jpg", "jpeg", "png"])
    if uploaded_check is not None:
        st.image(uploaded_check, caption="Uploaded Check Preview", use_container_width=True)
        if st.button("Run Instant Vision Scan", type="primary"):
            with st.spinner("Gemini AI is reading check data points..."):
                scan_results = scan_check_image(uploaded_check)
                risk_analysis = evaluate_check_risk(scan_results)
                
                log_transaction(
                    teller_id=st.session_state["teller_id"],
                    action_type="IMAGE_SCAN_OCR",
                    risk_score=risk_analysis["score"],
                    status=risk_analysis["status"],
                    action=risk_analysis["instructions"]
                )
                
                st.markdown("---")
                st.markdown("### 🛡️ Automated Risk Assessment Matrix")
                if risk_analysis["score"] >= 50:
                    st.error(f"**System Status:** {risk_analysis['status']} (Score: {risk_analysis['score']}/100)")
                elif risk_analysis["score"] >= 20:
                    st.warning(f"**System Status:** {risk_analysis['status']} (Score: {risk_analysis['score']}/100)")
                else:
                    st.success(f"**System Status:** {risk_analysis['status']} (Score: {risk_analysis['score']}/100)")
                
                st.info(f"**Required Next Steps:** {risk_analysis['instructions']}")
                st.write(scan_results)

with tabs[1]:
    st.markdown("### Teller Knowledge Base")
    user_query = st.text_input("Enter verification question:", placeholder="e.g., Rules for state tax checks?")
    if st.button("Run Rule Check"):
        if user_query.strip() != "":
            with st.spinner("Checking compliance protocols..."):
                ai_response = query_verify_agent(user_query)
                log_transaction(
                    teller_id=st.session_state["teller_id"],
                    action_type="KB_QUERY",
                    risk_score=0,
                    status="INFO_ONLY",
                    action=f"Queried: {user_query[:30]}..."
                )
                st.markdown("### 📋 System Response")
                st.write(ai_response)

# --- NEW: TAB 3 LOGIC (MANAGEMENT ANALYTICS) ---
if st.session_state["is_manager"]:
    with tabs[2]:
        st.markdown("### 📈 Enterprise Performance & Audit View")
        stats = get_analytics_data()
        
        if stats is None:
            st.info("No transaction log data found yet. Metrics will populate once tellers begin scanning items.")
        else:
            # Display structural operational metrics using columns
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Checks Scanned", stats["total_scans"])
            col2.metric("Flagged Reviews", stats["review"])
            col3.metric("Blocked Frauds", stats["high_risk"])
            
            st.markdown("---")
            st.markdown("#### Detailed Compliance Audit Trail Ledger")
            # Render interactive filterable data table
            st.dataframe(stats["df"], use_container_width=True)
