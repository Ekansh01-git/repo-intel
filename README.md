# Repo-Intel: Semantic Codebase Intelligence Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Vector DB: ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-blueviolet.svg)](https://www.trychroma.com/)
[![LLM: Gemini](https://img.shields.io/badge/LLM-Gemini--3.8--Flash-orange.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AST-powered semantic search and codebase intelligence tool that extracts code symbols, builds local vector embeddings, and answers complex structural questions using LLM Retrieval-Augmented Generation (RAG).

## Features
- **AST Symbol Extraction:** Employs Python's Abstract Syntax Tree parser to extract complete function and class boundaries rather than naive character chunking.
- **Local Vector Storage:** Uses ChromaDB for low-latency, persistent vector indexing of source trees.
- **Context-Aware Code RAG:** Retrieves targeted syntax nodes and leverages `gemini-3.8-flash` to synthesize architectural explanations with file and module citations.

## Quickstart

### 1. Setup Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt