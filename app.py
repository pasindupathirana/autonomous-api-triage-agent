import streamlit as st
from agent import run_triage_agent_with_trace

st.set_page_config(
    page_title="Autonomous API Incident Triage Agent",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Autonomous API Incident Triage Agent")
st.caption("Agentic ReAct Engine + Vector Semantic Search (ChromaDB RAG) + Execution Traces")

st.markdown("""
This autonomous agent identifies microservice degradations, inspects live telemetry, 
queries an embedded vector database for playbooks, and compiles root-cause post-mortems.
""")

# Sample incident options
st.subheader("Select or Enter an Incident Query")
preset_options = [
    "Downstream database errors are happening on order-api. Investigate the failure and give me the fix.",
    "Payment gateway is failing with 502 errors. Investigate cause and suggest fix.",
    "User authentication is failing with 401 errors. What is the issue?",
    "We are seeing 429 rate limit errors on payment-gateway. How do we mitigate this?"
]

selected_preset = st.selectbox("Quick Presets:", preset_options)
custom_query = st.text_input("Or enter a custom incident description:", value=selected_preset)

if st.button("Run Autonomous Triage", type="primary"):
    with st.spinner("Agent running autonomous reasoning, inspecting telemetry, and querying ChromaDB..."):
        try:
            report, steps = run_triage_agent_with_trace(custom_query)
            
            # Display step-by-step intermediate execution traces
            if steps:
                with st.expander("🔍 View Agent Execution Trace & Autonomous Decisions", expanded=True):
                    for i, step in enumerate(steps, start=1):
                        st.markdown(f"**Step {i}: {step['action']}**")
                        st.json({"parameters": step["input"]})
                        st.markdown("**Tool Output:**")
                        st.code(str(step["output"]), language="json")
                        st.markdown("---")
            
            st.success("Investigation & Post-Mortem Complete!")
            st.markdown("### Final Triage Post-Mortem")
            st.markdown(report)
            
        except Exception as e:
            st.error(f"Error executing agentic workflow: {str(e)}")

with st.sidebar:
    st.header("System Architecture")
    st.markdown("""
    - **Foundation Model:** Gemini 3.6 Flash
    - **Reasoning Framework:** ReAct (Reasoning + Action)
    - **Knowledge Retrieval:** Semantic RAG via ChromaDB
    - **Observability:** Step-by-Step Tool Trace Rendering
    
    ---
    **Autonomous Tool Registry:**
    * `fetch_error_logs`: Telemetry log filtering
    * `check_service_health`: Live latency & endpoint inspection
    * `search_runbook_rag`: Vector similarity search on engineering playbooks
    """)