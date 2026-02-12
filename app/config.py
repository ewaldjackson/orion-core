import os
from dotenv import load_dotenv

# Load .env if present (local dev)
load_dotenv()

# --- Storage ---
CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "orion_core")

# --- Retrieval ---
TOP_K = int(os.getenv("TOP_K", "5"))

# --- Decision Engine ---
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
