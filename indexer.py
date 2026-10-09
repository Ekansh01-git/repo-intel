import os
import ast
import chromadb
from rich.console import Console

console = Console()
chroma_client = chromadb.PersistentClient(path="./.code_db")
collection = chroma_client.get_or_create_collection(name="codebase_symbols")

def parse_python_file(file_path: str):
    """Parses a Python file and extracts complete functions, docstrings, and classes using AST."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    symbols = []
    lines = content.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start_line = node.lineno - 1
            end_line = getattr(node, "end_lineno", start_line + 1)
            code_snippet = "\n".join(lines[start_line:end_line])
            docstring = ast.get_docstring(node) or "No docstring provided."
            kind = "Class" if isinstance(node, ast.ClassDef) else "Function"

            symbols.append({
                "name": node.name,
                "type": kind,
                "file": file_path,
                "docstring": docstring,
                "snippet": code_snippet[:600]
            })
    return symbols

def index_directory(target_dir: str):
    console.print(f"[bold cyan]Scanning repository at: {target_dir}[/bold cyan]")
    docs, metadatas, ids = [], [], []
    count = 0

    for root, _, files in os.walk(target_dir):
        if any(ignored in root for ignored in ["venv", ".git", "__pycache__", ".code_db"]):
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                extracted = parse_python_file(path)
                for item in extracted:
                    text_chunk = f"Type: {item['type']} | Name: {item['name']} | File: {item['file']}\nDocstring: {item['docstring']}\nCode:\n{item['snippet']}"
                    docs.append(text_chunk)
                    metadatas.append({"file": item["file"], "name": item["name"], "type": item["type"]})
                    ids.append(f"sym_{count}")
                    count += 1

    if docs:
        collection.upsert(documents=docs, metadatas=metadatas, ids=ids)
        console.print(f"[bold green]Successfully indexed {len(docs)} structural code symbols into ChromaDB vector store![/bold green]")
    else:
        console.print("[yellow]No Python files with valid symbols found to index.[/yellow]")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    index_directory(target)