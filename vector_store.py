import os
import chromadb

# Initialize local persistent storage for vectors
client = chromadb.PersistentClient(path="./chroma_db")

# Create or retrieve runbook collection
collection = client.get_or_create_collection(name="engineering_runbooks")

RUNBOOK_DOCUMENTS = [
    {
        "id": "doc_502",
        "text": "Incident HTTP 502 Bad Gateway: Upstream connection timeout to backend service. Root cause: The backend microservice (core-banking) took longer than 5000ms or dropped the TCP handshake. Remediation: Increase gateway endpoint timeout from 5s to 10s. Check backend CPU/Memory saturation.",
        "metadata": {"error_code": "502", "service": "payment-gateway"}
    },
    {
        "id": "doc_429",
        "text": "Incident HTTP 429 Too Many Requests: Rate limit exceeded. Root cause: Client exceeded subscription quota or burst throttling limit. Remediation: Identify client ID from analytics, temporarily scale tier policy, and enforce exponential backoff retry.",
        "metadata": {"error_code": "429", "service": "payment-gateway"}
    },
    {
        "id": "doc_401",
        "text": "Incident HTTP 401 Unauthorized: JWT token expired or invalid signature. Root cause: Bearer token duration elapsed or signing key rotated. Remediation: Verify token issuer URL and key ID against Identity Server. Request client to refresh OAuth token.",
        "metadata": {"error_code": "401", "service": "user-auth"}
    },
    {
        "id": "doc_503",
        "text": "Incident HTTP 503 Service Unavailable: Database connection pool exhausted. Root cause: Microservice backend exhausted all active database connections. Remediation: Restart idle worker connections, increase max_connections parameter, check for slow unindexed queries.",
        "metadata": {"error_code": "503", "service": "order-api"}
    }
]

def index_runbooks():
    """Populates the vector store with runbook embeddings."""
    existing_count = collection.count()
    if existing_count == len(RUNBOOK_DOCUMENTS):
        return
    
    ids = [doc["id"] for doc in RUNBOOK_DOCUMENTS]
    documents = [doc["text"] for doc in RUNBOOK_DOCUMENTS]
    metadatas = [doc["metadata"] for doc in RUNBOOK_DOCUMENTS]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

def semantic_search_runbook(query: str, n_results: int = 1) -> str:
    """Performs semantic similarity search over engineering runbooks."""
    index_runbooks()
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    if results and results["documents"]:
        return "\n---\n".join(results["documents"][0])
    return f"No relevant documentation found for '{query}'."

if __name__ == "__main__":
    print("Indexing documents into ChromaDB...")
    index_runbooks()
    test_query = "database connection failure and timeouts"
    print(f"\nTesting Semantic Search for: '{test_query}'")
    match = semantic_search_runbook(test_query)
    print("\nResult Retrieved:\n", match)