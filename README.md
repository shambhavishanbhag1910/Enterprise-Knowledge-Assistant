# Enterprise Knowledge Assistant

An Enterprise Grade AI Powered Knowledge Assistant built using **Retrieval Augmented Generation (RAG)**, **Qdrant**, **Sentence Transformers**, **FastAPI**, and **Langfuse**.

The solution enables organizations to search, retrieve, and generate answers from enterprise documents such as policies, SOPs, manuals, procurement documents, technical specifications, compliance documents, and knowledge repositories.

---

## Project Objective

The primary objective of this project is to build an end to end Enterprise Knowledge Assistant capable of:

- Ingesting enterprise documents
- Generating embeddings using Sentence Transformers
- Storing vectors in Qdrant
- Retrieving relevant document chunks
- Generating contextual answers using LLMs
- Providing source citations
- Evaluating RAG performance
- Monitoring AI interactions through observability tools
- Supporting future Agentic AI capabilities

---

## Current Features

### FastAPI Backend

- Health check endpoint
- Chat API endpoint
- Evaluation API endpoint
- Observability status endpoint

### Retrieval Augmented Generation (RAG)

- Semantic search using vector embeddings
- Qdrant vector database integration
- Prompt construction
- LLM based answer generation
- Source attribution

### Evaluation Framework

- Golden question dataset evaluation
- Source matching validation
- Keyword based answer validation
- Overall answer scoring

### Observability

- Langfuse integration
- Retrieval tracing
- Prompt tracing
- LLM generation tracing

---

## Technology Stack

| Layer | Technology |
|---------|------------|
| Backend | FastAPI |
| Vector Database | Qdrant |
| Embedding Model | Sentence Transformers |
| LLM Provider | Groq / OpenAI Compatible |
| Observability | Langfuse |
| Containerization | Docker |
| Evaluation | Custom Evaluation Framework |
| Future Workflow Engine | n8n |
| Future Agent Framework | CrewAI |
| Future Tool Layer | MCP |

---

## High Level Architecture

```text
+------------------+
|      User        |
+--------+---------+
         |
         v
+------------------+
|  FastAPI Backend |
+--------+---------+
         |
         v
+------------------+
|   RAG Service    |
+--------+---------+
         |
         +----------------------+
         |                      |
         v                      v
+----------------+      +----------------+
| Qdrant Search  |      | Prompt Builder |
+----------------+      +----------------+
         |                      |
         +----------+-----------+
                    |
                    v
         +----------------------+
         |      LLM Layer       |
         +----------------------+
                    |
                    v
         +----------------------+
         | Answer + Sources     |
         +----------------------+

Supporting Services

- Langfuse
- Evaluation Engine
- Docker Infrastructure
- Future Agent Layer
- Future MCP Tools
```

---

## Project Structure

```text
Enterprise-Knowledge-Assistant/

├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   └── app/
│       ├── api/
│       │   ├── chat.py
│       │   ├── evaluation.py
│       │   ├── observability.py
│       │   └── schemas.py
│       │
│       ├── generation/
│       │   ├── rag_service.py
│       │   ├── llm_client.py
│       │   └── prompt_builder.py
│       │
│       ├── retrieval/
│       │   ├── embedding_model.py
│       │   ├── search_chunks.py
│       │   └── vector_store.py
│       │
│       ├── evaluation/
│       │   └── evaluate_rag.py
│       │
│       └── observability/
│           └── langfuse_client.py
│
├── infra/
│   └── docker-compose.yml
│
├── data/
│   └── golden_questions/
│
├── reports/
│   └── evaluation/
│
└── README.md
```

---

## Available APIs

### Health Check

```http
GET /health
```

Response

```json
{
  "status": "ok"
}
```

### Chat Endpoint

```http
POST /api/chat
```

Request

```json
{
  "question": "Who approves purchase orders above 50000 dollars?",
  "top_k": 5
}
```

Response

```json
{
  "question": "Who approves purchase orders above 50000 dollars?",
  "answer": "Generated answer",
  "sources": [],
  "retrieved_chunks": []
}
```

### Evaluation Endpoint

```http
POST /api/evaluate
```

Runs evaluation against the golden dataset.

### Observability Endpoint

```http
GET /api/observability/status
```

Returns Langfuse configuration and authentication status.

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/shambhavishanbhag1910/Enterprise-Knowledge-Assistant.git

cd Enterprise-Knowledge-Assistant

git checkout DEV
```

### Create Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac**

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=enterprise_documents

GROQ_API_KEY=YOUR_GROQ_API_KEY

LANGFUSE_PUBLIC_KEY=YOUR_PUBLIC_KEY
LANGFUSE_SECRET_KEY=YOUR_SECRET_KEY
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Start Infrastructure

```bash
cd infra
docker compose up -d
```

Services started:

- Qdrant
- Ollama

### Run Backend

```bash
uvicorn backend.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Evaluation Framework

Current evaluation metrics:

- Keyword Match Score
- Source Match Score
- Answer Presence Score
- Overall Score

Evaluation reports generated:

```text
reports/evaluation/rag_eval_results.json

reports/evaluation/rag_eval_summary.json
```

---

## Development Roadmap

### Phase 1 – Core RAG Completion

- Document Upload API
- PDF, DOCX, TXT and CSV Ingestion
- Chunking Pipeline
- Embedding Generation
- Metadata Management
- MinIO Integration
- PostgreSQL Integration

### Phase 2 – User Interface

- React Frontend
- Streamlit Frontend
- Chat Interface
- Upload Interface
- Document Library
- Source Viewer

### Phase 3 – Advanced Retrieval

- Hybrid Search
- Metadata Filtering
- Reranking
- Context Compression
- Conversation Memory

### Phase 4 – Agentic AI

- Agent Routing
- Tool Calling
- Multi Step Reasoning
- CrewAI Integration

### Phase 5 – MCP Integration

- MCP Server
- Search Tools
- Document Tools
- Enterprise Tool Integration

### Phase 6 – Automation

- n8n Workflows
- Scheduled Ingestion
- Scheduled Evaluation
- Automated Reports

### Phase 7 – Governance and Observability

- Authentication
- RBAC
- Audit Logs
- OpenTelemetry
- Cost Tracking
- Usage Monitoring

### Phase 8 – Deployment

- Docker Images
- GitHub Actions
- CI/CD Pipeline
- AWS Deployment
- Azure Deployment
- Monitoring Dashboard

---

## Primary Scope Checklist

| Capability | Status |
|------------|---------|
| FastAPI Backend | ✅ Implemented |
| RAG Pipeline | ✅ Implemented |
| Qdrant Integration | ✅ Implemented |
| Langfuse Observability | ✅ Implemented |
| Evaluation Framework | ✅ Implemented |
| Document Upload | 🚧 Planned |
| Frontend | 🚧 Planned |
| RAGAS Evaluation | 🚧 Planned |
| Agentic RAG | 🚧 Planned |
| MCP | 🚧 Planned |
| CrewAI | 🚧 Planned |
| n8n | 🚧 Planned |
| CI/CD | 🚧 Planned |
| AWS Deployment | 🚧 Planned |
| Azure Deployment | 🚧 Planned |

---

## Future Vision

The long term vision of this project is to evolve from a traditional RAG application into a complete Enterprise AI Platform featuring:

- Enterprise Knowledge Search
- Agentic AI Workflows
- Multi Agent Collaboration
- MCP Tool Ecosystem
- Automated Evaluation
- Enterprise Governance
- Production Observability
- Cloud Native Deployment

---

## Contributors

- Shambhavi Shanbhag
- Project Contributors

---

## License

This project is intended for educational, research, and enterprise AI experimentation purposes.