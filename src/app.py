import streamlit as st
from gemini_agent import query_verify_agent

# Set up page configurations
st.set_page_config(page_title="Verify-N-Fund Dashboard", page_icon="🏦", layout="centered")

# App Header
st.title("🏦 Verify-N-Fund")
st.subheader("Automated Check Verification Assistant")
st.write("Helping currency exchanges and tellers save time securely.")

st.markdown("---")

# Informing users of the guardrails
st.info("🔒 **System Guardrails Active:** This assistant is explicitly trained to handle check cashing, verification rules, compliance, and fraud queries. General off-topic questions will be filtered out.")

# User Input Section
user_query = st.text_input(
    "Enter verification question or check details:",
    placeholder="e.g., How do I verify a out-of-state cashier's check?"
)

# Execution Section
if st.button("Run Verification Check", type="primary"):
    if user_query.strip() == "":
        st.warning("Please type a question or enter check data first.")
    else:
        with st.spinner("Analyzing rules and processing routing logic..."):
            # Call the guarded Gemini agent from our other file
            ai_response = query_verify_agent(user_query)
            
            # Display results
            st.markdown("### 📋 System Response")
            st.write(ai_response)

# Footer
st.markdown("---")
st.caption("Verify-N-Fund Proprietary System Framework • Enterprise Version 1.0")
