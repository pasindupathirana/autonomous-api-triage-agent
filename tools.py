import json
import os
from vector_store import semantic_search_runbook

def fetch_error_logs(service_name: str = "") -> str:
    """Fetches recent error logs (HTTP 4xx/5xx) for API services from the telemetry log store.
    Args:
        service_name: Optional name of the target service (e.g., 'payment-gateway', 'user-auth', 'order-api').
    """
    file_path = "server_logs.json"
    if not os.path.exists(file_path):
        return "Log file not found."
    
    with open(file_path, "r", encoding="utf-8") as f:
        logs = json.load(f)
    
    errors = [
        log for log in logs 
        if log.get("status_code", 200) >= 400 
        and (not service_name or service_name.lower() in log.get("service", "").lower())
    ]
    
    if not errors:
        return f"No errors found for service: {service_name}" if service_name else "No errors found."
    return json.dumps(errors, indent=2)


def check_service_health(service_name: str) -> str:
    """Checks real-time operational status, latency, and endpoints of a backend microservice.
    Args:
        service_name: Name of the target microservice (e.g., 'payment-gateway', 'user-auth', 'order-api').
    """
    health_registry = {
        "payment-gateway": {"status": "DEGRADED", "latency": "5200ms", "upstream_target": "core-banking.internal:8443"},
        "user-auth": {"status": "HEALTHY", "latency": "45ms", "upstream_target": "auth-service.internal:9443"},
        "order-api": {"status": "DEGRADED", "latency": "3800ms", "upstream_target": "orders-db.internal:5432"}
    }
    
    target = health_registry.get(service_name.lower().strip())
    if not target:
        return f"Service '{service_name}' not recognized in health registry."
    return json.dumps(target, indent=2)


def search_runbook_rag(incident_symptoms: str) -> str:
    """Executes a semantic vector search (RAG) across incident runbooks in ChromaDB.
    Args:
        incident_symptoms: Natural language description of symptoms, error messages, or failure patterns.
    """
    return semantic_search_runbook(incident_symptoms, n_results=1)

def apply_remediation(action_type: str, service_name: str) -> str:
    """Simulates executing an automated remediation policy on an upstream service or gateway.
    Args:
        action_type: Remediation action to execute (e.g., 'increase_timeout', 'restart_pool', 'scale_rate_limit').
        service_name: Name of the service targeted (e.g., 'payment-gateway', 'order-api', 'user-auth').
    """
    remediation_map = {
        "increase_timeout": f"Successfully updated endpoint timeout from 5000ms to 10000ms on '{service_name}'.",
        "restart_pool": f"Successfully recycled idle DB pool workers and reset connections for '{service_name}'.",
        "scale_rate_limit": f"Successfully scaled burst rate quota by +50% for '{service_name}'.",
        "refresh_token_cache": f"Successfully flushed expired JWT tokens from key cache for '{service_name}'."
    }
    
    result = remediation_map.get(
        action_type.lower().strip(), 
        f"Executed manual generic mitigation '{action_type}' on '{service_name}'."
    )
    return result