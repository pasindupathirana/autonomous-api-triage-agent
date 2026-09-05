# ⚡ Autonomous API Incident Triage Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gemini 3.6 Flash](https://img.shields.io/badge/LLM-Gemini%203.6%20Flash-orange.svg)](https://ai.google.dev/)
[![ChromaDB RAG](https://img.shields.io/badge/VectorDB-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![Streamlit UI](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade **Autonomous Site Reliability Engineering (SRE) & API Incident Triage Agent** designed to accelerate Mean Time to Resolution (MTTR) during production microservice degradations.

Built using the **ReAct (Reasoning + Action)** pattern with decoupled tool execution, the agent autonomously correlates live error logs, evaluates upstream service latencies, queries a semantic vector database of engineering playbooks, and exposes an interactive execution trace.

---

## 🏛️ System Architecture

---

## 💡 Key Engineering Highlights

* **Autonomous Multi-Turn Tool Calling:** Rather than using single-prompt generation, the agent orchestrates multi-turn function calls to iteratively gather telemetry data before drawing conclusions.
* **Semantic Runbook Retrieval (Vector RAG):** Eliminates fragile keyword searches. Engineering playbooks are embedded into **ChromaDB** using sentence transformer embeddings, allowing semantic matching (e.g., mapping *"database pool exhausted"* directly to 503 connection errors).
* **Granular UI Observability:** Intermediate tool invocations, parameters, and raw JSON payloads are exposed in an expandable real-time execution trace.
* **Production Resilience:** Implements exponential backoff with retry logic to gracefully mitigate upstream API rate limits (`HTTP 429 RESOURCE_EXHAUSTED`).
* **Human-in-the-Loop (HITL) Guardrail Design:** Actionable remediation proposals (e.g., scaling quotas or adjusting timeouts) are isolated into a structured approval stage to ensure safe production execution.

---

## 📂 Project Structure

```text
api-triage-agent/
│
├── app.py                 # Streamlit web dashboard with interactive execution tracing
├── agent.py               # Core ReAct triage loop with Gemini tool orchestration
├── tools.py               # Tool registry (telemetry parser, health checker, RAG query)
├── vector_store.py        # ChromaDB setup and embedding indexer for runbooks
├── server_logs.json       # Mock distributed microservice telemetry stream
├── runbook.md             # Standard operating incident playbooks (SOPs)
├── requirements.txt       # Pinned project dependencies
├── .env.example           # Template for environment variables
└── README.md              # Technical documentation and architecture specification