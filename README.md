# Orion Core

A **decision-first** AI backend (RAG + confidence + gated generation).

Orion Core is not a “chat with your docs” demo. It is a backend engine that separates:
- **Evidence retrieval**
- **Confidence + decisioning**
- **Generation**
so the system can explicitly decide when it should answer vs. when it should refuse or fallback.

---

## Why Orion Exists

Most RAG projects do this:

`retrieve → stuff context → generate → hope`

Orion does this:

`retrieve → score evidence → decide → generate (only if warranted)`

This makes Orion usable as a long-term platform layer where uncertainty is first-class.

---

## Core Output Contract

Every request returns a structured decision payload:

```json
{
  "answer": "...",
  "confidence": 0.0,
  "decision": "TRUST_CONTEXT",
  "sources": []
}



Decision states:

TRUST_CONTEXT — evidence is sufficient to answer from retrieved context

NEED_FALLBACK — evidence is weak; fallback path should be used

INSUFFICIENT_DATA — no meaningful evidence retrieved


Runtime Flow (MVP)

Ingest

folder → chunk → embed → persist (Chroma)

Retrieve

query → top_k chunks (+ scores + metadata)

Decide (Core)

aggregate retrieval scores → confidence

produce decision

Generate (Gated)

only runs when decision == TRUST_CONTEXT

Fallback Hook

interface exists in MVP (stub)

becomes real in later phases (web, tools, agents)


Architecture: Modules
app/
  ingestion/     # folder ingest, chunking, embeddings
  retrieval/     # vector search + scoring + fallback hook
  llm/           # generation wrapper + prompt templates
  schemas/       # request/response contracts
  utils/         # logging + helpers

data/chroma/     # persisted vector store
tests/           # test scaffold (ingest/retrieve/score)
scripts/         # dev + ingestion helpers


Orion is designed to be:

LLM-agnostic

Vector-store agnostic

deployable to local, VM, or container/serverless


What Makes This Stand Out

Orion’s differentiator is the Decision Engine.

Instead of trusting the model, Orion exposes reliability as data:

score evidence

quantify confidence

decide what to do next

This is the foundation for future layers (multi-agent validation, tool use, orchestration).


Status

Architecture and MVP scope locked in.
Implementation begins with ingestion → retrieval → decision engine.

See ARCHITECTURE.md for the deeper spec.
