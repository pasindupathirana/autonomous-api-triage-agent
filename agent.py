import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from tools import fetch_error_logs, check_service_health, search_runbook_rag

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are an expert Autonomous Site Reliability & API Incident Triage Agent.
Your role is to investigate system errors, review telemetry logs, verify upstream health, 
and perform semantic RAG searches on incident playbooks to generate a clear Root Cause Analysis (RCA).

Investigation Workflow:
1. Identify the target service or error signatures mentioned.
2. Call `fetch_error_logs` to retrieve specific failure entries.
3. Call `check_service_health` to evaluate backend latency and degradation.
4. Call `search_runbook_rag` using descriptive symptom summaries to find remediation steps.
5. Synthesize your findings into a clean post-mortem containing:
   - Incident Summary
   - Root Cause Analysis (RCA)
   - Diagnostic Evidence (latencies, status codes, endpoints)
   - Recommended Remediation Steps
"""

# Tool dispatcher dictionary
TOOL_DISPATCHER = {
    "fetch_error_logs": fetch_error_logs,
    "check_service_health": check_service_health,
    "search_runbook_rag": search_runbook_rag,
}

def run_triage_agent_with_trace(user_query: str, max_retries: int = 3):
    """Executes manual multi-turn agentic loop to capture intermediate thoughts & tool calls."""
    tools_declaration = [fetch_error_logs, check_service_health, search_runbook_rag]
    execution_steps = []
    
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=tools_declaration,
            temperature=0.2,
        ),
    )
    
    current_input = user_query
    for attempt in range(max_retries):
        try:
            # Multi-turn loop
            while True:
                response = chat.send_message(current_input)
                
                # If Gemini decides to call tools
                if response.function_calls:
                    for call in response.function_calls:
                        func_name = call.name
                        func_args = dict(call.args) if call.args else {}
                        
                        execution_steps.append({
                            "action": f"Invoking Tool: `{func_name}`",
                            "input": func_args
                        })
                        
                        # Execute the target Python function
                        tool_func = TOOL_DISPATCHER.get(func_name)
                        if tool_func:
                            tool_result = tool_func(**func_args)
                        else:
                            tool_result = f"Error: Tool {func_name} not recognized."
                        
                        execution_steps[-1]["output"] = tool_result
                        
                        # Return tool execution output back to the model
                        current_input = types.Part.from_function_response(
                            name=func_name,
                            response={"result": tool_result}
                        )
                else:
                    # Final synthesis reached
                    return response.text, execution_steps
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = 3 * (attempt + 1)
                time.sleep(wait_time)
            else:
                raise e
                
    return "Failed to complete investigation due to API rate limits.", execution_steps