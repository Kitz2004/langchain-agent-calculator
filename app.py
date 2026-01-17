import streamlit as st
from agent import detect_operation, execute_agent

st.set_page_config(page_title="Consent-Based AI Calculator", page_icon="🧮")
st.title("Consent-Based AI Calculator")

# Initialize session state
if "operation" not in st.session_state:
    st.session_state.operation = None
    st.session_state.expression = None
    st.session_state.awaiting_consent = False

query = st.text_input("Ask me:")

if st.button("Submit") and query:
    op, expr = detect_operation(query)
    if op:
        st.session_state.operation = op
        st.session_state.expression = expr
        st.session_state.awaiting_consent = True
    else:
        st.error("Could not detect a valid operation.")

# Ask for consent
if st.session_state.awaiting_consent:
    st.info(
        f"Detected operation: **{st.session_state.operation}**\n\n"
        f"Expression: `{st.session_state.expression}`"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Accept"):
            result = execute_agent(
                st.session_state.operation,
                st.session_state.expression
            )
            st.success(f"Result: {result}")
            st.session_state.awaiting_consent = False

    with col2:
        if st.button("❌ Reject"):
            st.warning("Agent execution cancelled by user.")
            st.session_state.awaiting_consent = False
