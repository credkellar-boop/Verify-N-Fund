import streamlit as st
from gemini_agent import query_verify_agent, scan_check_image

st.set_page_config(page_title="Verify-N-Fund Dashboard", page_icon="🏦", layout="centered")

st.title("🏦 Verify-N-Fund")
st.subheader("Automated Check Verification & AI Scanner")
st.info("🔒 **System Guardrails Active:** Protected by enterprise compliance rules.")

# Create tabs to keep the interface extremely organized for busy tellers
tab1, tab2 = st.tabs(["📸 Scan Check Image", "❓ Ask a Question"])

with tab1:
    st.markdown("### High-Speed Vision Scanner")
    st.write("Upload or snap a photo of the check to instantly extract details and run compliance rules.")
    
    # File uploader accepts webcam snapshots or file uploads from phone/computer
    uploaded_check = st.file_uploader("Upload check image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_check is not None:
        # Show a preview thumbnail to the teller
        st.image(uploaded_check, caption="Uploaded Check Preview", use_container_width=True)
        
        if st.button("Run Instant Vision Scan", type="primary"):
            with st.spinner("Gemini AI is reading check data points..."):
                scan_results = scan_check_image(uploaded_check)
                st.markdown("### 📋 Extracted Scan Results")
                st.success("Analysis Complete")
                st.write(scan_results)
# Import the new risk calculation function at the top of src/app.py
from verifier import evaluate_check_risk

# ... (Keep your existing code up to the 'uploaded_check' button processing) ...

        if st.button("Run Instant Vision Scan", type="primary"):
            with st.spinner("Gemini AI is reading check data points..."):
                scan_results = scan_check_image(uploaded_check)
                
                # --- NEW: Run the programmatic risk engine ---
                risk_analysis = evaluate_check_risk(scan_results)
                
                st.markdown("---")
                st.markdown("### 🛡️ Automated Risk Assessment Matrix")
                
                # Display status with custom color coding
                if risk_analysis["score"] >= 50:
                    st.error(f"**System Status:** {risk_analysis['status']} (Score: {risk_analysis['score']}/100)")
                elif risk_analysis["score"] >= 20:
                    st.warning(f"**System Status:** {risk_analysis['status']} (Score: {risk_analysis['score']}/100)")
                else:
                    st.success(f"**System Status:** {risk_analysis['status']} (Score: {risk_analysis['score']}/100)")
                
                # Display Next Steps instructions for the busy teller
                st.info(f"**Required Next Steps:** {risk_analysis['instructions']}")
                
                if risk_analysis["flags"]:
                    st.markdown("**Triggered Risk Flags:**")
                    for flag in risk_analysis["flags"]:
                        st.markdown(f"- 🚩 {flag}")
                        
                st.markdown("---")
                st.markdown("### 📋 Raw Extracted Scan Results")
                st.write(scan_results)

with tab2:
    st.markdown("### Teller Knowledge Base")
    user_query = st.text_input(
        "Enter verification question:",
        placeholder="e.g., What is the holding period for a out-of-state check over $5,000?"
    )
    
    if st.button("Run Rule Check"):
        if user_query.strip() != "":
            with st.spinner("Checking compliance protocols..."):
                ai_response = query_verify_agent(user_query)
                st.markdown("### 📋 System Response")
                st.write(ai_response)
