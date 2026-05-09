# SHL Assessment Recommendation Agent

## Overview

This project implements a conversational SHL assessment recommendation system using:

- FastAPI
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- FAISS vector search
- Groq LLM integration
- Semantic retrieval

The API can:

- Ask clarification questions
- Recommend SHL assessments
- Compare assessments
- Handle multi-turn conversations
- Refuse off-topic requests
- Generate grounded conversational responses

---

# Public Deployment

Base URL:

```text
https://shl-assessment-agent-production.up.railway.app
```

Swagger Docs:

```text
https://shl-assessment-agent-production.up.railway.app/docs
```

Health Endpoint:

```text
GET /health
```

Chat Endpoint:

```text
POST /chat
```

---

# Features

## Conversational Recommendation System

The system supports:

- clarification questions
- semantic assessment retrieval
- conversational recommendations
- comparison support
- refinement handling
- prompt injection defense

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| LLM | Groq Llama 3.1 8B Instant |
| Deployment | Railway |
| Language | Python |

---

# Retrieval Pipeline

## Data Collection

The SHL catalog was scraped using:

- requests
- BeautifulSoup

Extracted fields include:

- assessment name
- description
- URL
- inferred assessment type

---

## Embeddings

The embedding model used:

```text
all-MiniLM-L6-v2
```

Embeddings are generated for:

- assessment names
- descriptions
- assessment types

---

## Vector Search

FAISS is used for semantic similarity search.

The system retrieves top matching assessments based on:

- role requirements
- technical skills
- communication requirements
- leadership needs
- behavioral signals

---

# LLM Integration

The conversational layer uses:

```text
llama-3.1-8b-instant
```

via the Groq API.

LLM prompts are used for:

- clarification generation
- recommendation explanations
- comparison responses
- conversational grounding

---

# API Schema

## Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring Java developers with coding skills"
    }
  ]
}
```

---

## Response

```json
{
  "reply": "These SHL assessments are suitable for evaluating technical and communication skills.",
  "recommendations": [
    {
      "name": "Technical Skills",
      "url": "https://www.shl.com/...",
      "test_type": "T"
    }
  ],
  "end_of_conversation": true
}
```

---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/Charankumm/shl-assessment-agent.git
cd shl-assessment-agent
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_key_here
```

---

## Run API

```bash
uvicorn app.main:app --reload
```

---

# Deployment

The project is deployed using Railway.

Deployment configuration includes:

- Procfile
- railway.json
- environment variables

---

# Evaluation Approach

The system was evaluated using:

- clarification scenarios
- recommendation relevance
- comparison accuracy
- prompt injection resistance
- grounded conversational quality

Improvements were measured qualitatively through repeated retrieval and conversation testing.

---

# Repository

GitHub Repository:

```text
https://github.com/Charankumm/shl-assessment-agent
```

---

# Author

Charan Kumar
