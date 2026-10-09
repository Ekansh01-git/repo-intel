import sys
import chromadb
from google import genai
from rich.console import Console
from rich.panel import Panel

console = Console()
client = genai.Client()
chroma_client = chromadb.PersistentClient(path="./.code_db")

try:
    collection = chroma_client.get_collection(name="codebase_symbols")
except Exception:
    console.print("[red]No index found! Please run 'python indexer.py <path>' first.[/red]")
    sys.exit(1)

SYSTEM_PROMPT = """
You are a Principal Software Architect. 
Answer the user's question about the codebase using ONLY the retrieved symbol contexts below.
Always cite specific file paths, function/class names, and explain the underlying architecture clearly.
"""

def query_repo(question: str):
    console.print(f"\n[bold yellow]Searching codebase index for:[/bold yellow] [italic]{question}[/italic]")

    results = collection.query(query_texts=[question], n_results=3)
    retrieved_docs = results["documents"][0] if results["documents"] else []

    if not retrieved_docs:
        console.print("[red]No relevant symbols found in the index.[/red]")
        return

    context = "\n\n---\n\n".join(retrieved_docs)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {question}"
    )

    console.print(Panel(response.text.strip(), title="Architectural Analysis & Code Trace", border_style="green"))

if __name__ == "__main__":
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Explain the primary modules and execution flow."
    query_repo(user_query)