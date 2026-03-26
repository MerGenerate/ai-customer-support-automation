# AI Customer Support Automation System

## Overview

This project is a local document-based customer support assistant built with a Retrieval-Augmented Generation pipeline.

It uses:
- FAISS for retrieval
- local embeddings
- LM Studio as the local inference server

The system can answer support questions based on uploaded company documents in a privacy-friendly local environment.

## Features

- PDF-based question answering
- Local inference with LM Studio
- Vector search with FAISS
- Streamlit chat interface
- Privacy-friendly architecture

## Project Structure

```text
ai-customer-support-system/
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── memory.py
│   └── utils.py
├── data/
│   └── faq.pdf
├── ui/
│   └── app.py
├── screenshots/
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore