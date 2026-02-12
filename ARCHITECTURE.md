# Orion Core Architecture

## Identity
Orion Core is a **decision-first AI backend**: retrieval produces evidence, a decision engine determines whether the evidence is sufficient, and generation is gated by confidence.

This project is designed to be:
- **LLM-agnostic** (OpenAI now, swappable later)
- **Storage-agnostic** (Chroma now, swappable later)
- **Deployable anywhere** (local Ubuntu, VM, container, serverless)

---

## Core Runtime Flow (MVP)

1) **Ingestion Layer**
- Load documents (folder ingest)
- Chunk content
- Create embeddings
- Persist into vector store (Chroma)

2) **Retrieval Layer**
- Query embeddings
- Retrieve top_k chunks
- Return structured retrieval results with scores + source metadata

3) **Decision Engine (Core Differentiator)**
- Aggregate retrieval scores into a single confidence value
- Decide one of:
  - `TRUST_CONTEXT`
  - `NEED_FALLBACK`
  - `INSUFFICIENT_DATA`

4) **Generation Layer**
- If decision is `TRUST_CONTEXT`, generate an answer using retrieved context
- If decision is `NEED_FALLBACK`, call fallback hook (stub for MVP)
- If decision is `INSUFFICIENT_DATA`, return “no evidence” response

---

## Output Contract (Non-Negotiable)

Every response must return a structured payload:

```json
{
  "answer": "...",
  "confidence": 0.0,
  "decision": "TRUST_CONTEXT",
  "sources": []
}
Modules
app/ingestion/

ingest.py: folder ingestion orchestration

chunking.py: chunk strategy (size/overlap)

embeddings.py: embedding interface (swappable)

app/retrieval/

retriever.py: vector search + retrieval formatting

scoring.py: confidence aggregation + decision logic

fallback.py: fallback interface (stub for MVP)

app/llm/

generator.py: LLM interface (swappable)

prompt_templates.py: prompt building

app/schemas/

API request/response models

data/chroma/

persistent vector store files


MVP Success Criteria

Ingest works reliably for a folder of docs

Query returns top_k results and scores

Decision engine returns correct decision state

API returns structured output contract every time


**Description**
- Implement request/response schemas for `/query`
- Ensure response always returns: `answer`, `confidence`, `decision`, `sources`
**Acceptance Criteria**
- Contract documented in README + ARCHITECTURE
- Endpoint returns valid JSON even when no data exists

---

### Issue 2 — Ingestion MVP (folder → chunks → vector store)
**Description**
- Implement folder ingest pipeline
- Chunk documents consistently
- Persist to Chroma under `data/chroma/`
**Acceptance Criteria**
- Ingesting same folder twice does not break the system
- Logs show number of docs + chunks ingested

---

### Issue 3 — Retrieval MVP (query → top_k results)
**Description**
- Implement retrieval against Chroma
- Return list of results with:
  - source id/path
  - similarity score
  - chunk text
**Acceptance Criteria**
- Query returns deterministic top_k results
- Includes metadata for each result

---

### Issue 4 — Decision Engine MVP (confidence + decision states)
**Description**
- Implement confidence aggregation over retrieval scores
- Produce 3 decisions:
  - TRUST_CONTEXT
  - NEED_FALLBACK
  - INSUFFICIENT_DATA
**Acceptance Criteria**
- Decision changes correctly with threshold changes
- Confidence value returned in response

---

### Issue 5 — Generation Layer MVP (gated by decision)
**Description**
- Implement generator wrapper (LLM interface)
- Only generate when decision is `TRUST_CONTEXT`
**Acceptance Criteria**
- When `TRUST_CONTEXT`, answer is generated using retrieved chunks
- When not, generator is not called

---

### Issue 6 — Fallback Hook (stub for MVP)
**Description**
- Implement fallback interface that returns:
  - “fallback not implemented” + decision context
**Acceptance Criteria**
- System returns valid response when fallback required

---

### Issue 7 — Developer Run Scripts
**Description**
- Add `scripts/run_dev.sh` to start API
- Add `scripts/ingest_folder.sh` to ingest docs directory
**Acceptance Criteria**
- A new machine can run Orion with 2 commands
