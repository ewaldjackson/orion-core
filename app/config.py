import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present (local dev)
load_dotenv()

# Repo root: .../orion-core/app/config.py -> parents[1] = orion-core/
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# --- Storage (Primary) ---
CHROMA_PATH = os.getenv("CHROMA_PATH", str(DATA_DIR / "chroma"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "orion_core")

# --- Storage (Sandbox / Auto-Ingest Testing) ---
CHROMA_SANDBOX_PATH = os.getenv("CHROMA_SANDBOX_PATH", str(DATA_DIR / "chroma_sandbox"))
SANDBOX_COLLECTION_NAME = os.getenv("SANDBOX_COLLECTION_NAME", "orion_ingest_sandbox")

# --- Ingestion Tracking / Preview ---
STATE_PATH = os.getenv("STATE_PATH", str(DATA_DIR / "state.json"))
INGEST_PREVIEW_DIR = os.getenv("INGEST_PREVIEW_DIR", str(DATA_DIR / "ingest_preview"))

# --- Chunking ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# --- Embeddings (lock these to avoid mismatches) ---
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")  # openai | local | other
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1536"))

# --- Retrieval ---
TOP_K = int(os.getenv("TOP_K", "5"))

# --- Decision Engine ---
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))

# --- Auto-Ingest Limits (Flood Protection) ---
MAX_PAGES_PER_RUN = int(os.getenv("MAX_PAGES_PER_RUN", "15"))
MIN_TEXT_CHARS = int(os.getenv("MIN_TEXT_CHARS", "800"))
MAX_TEXT_CHARS = int(os.getenv("MAX_TEXT_CHARS", "80000"))

# --- Network Politeness ---
REQUEST_TIMEOUT_SEC = int(os.getenv("REQUEST_TIMEOUT_SEC", "20"))
REQUEST_DELAY_SEC = float(os.getenv("REQUEST_DELAY_SEC", "1.0"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "OrionCoreIngestBot/0.1 (contact: admin@local)"
)
