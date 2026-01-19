# app.py
import streamlit as st
from agent import detect_intent, execute_agent

st.set_page_config(page_title="Agentic Calculator", page_icon="🧮")
st.title("Agentic Calculator (Human-in-the-loop)")

query = st.text_input("Example: add 5 and 3")

# Session state
if "intent" not in st.session_state:
    st.session_state.intent = None

if "decision" not in st.session_state:
    st.session_state.decision = None

# -----------------------------
# STEP 1: Submit query
# -----------------------------
if st.button("Submit") and query:
    intent = detect_intent(query)

    if intent is None:
        st.error("Could not understand the request. Please rephrase.")
        st.stop()

    st.session_state.intent = intent
    st.session_state.decision = None

# -----------------------------
# STEP 2: Ask for consent
# -----------------------------
if st.session_state.intent and st.session_state.decision is None:
    intent = st.session_state.intent

    st.info(
        f"I detected an **{intent['operation']}** operation\n\n"
        f"Numbers: **{intent['a']}** and **{intent['b']}**\n\n"
        "Do you want me to call the agent?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Accept"):
            st.session_state.decision = "accept"

    with col2:
        if st.button("Reject"):
            st.session_state.decision = "reject"

# -----------------------------
# STEP 3: Execute or stop
# -----------------------------
if st.session_state.decision == "accept":
    result = execute_agent(st.session_state.intent)
    st.success(f"Result: {result}")

elif st.session_state.decision == "reject":
    st.warning("You rejected the agent execution.")
