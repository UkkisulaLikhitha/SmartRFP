# ===========================================================================
#  backend/config.py
#  >>> THIS FILE BELONGS IN THE backend/ FOLDER.
#  >>> DO NOT put this file in the project root. The root has its OWN config.py.
# ===========================================================================
"""
backend/config.py
=================
Single source of truth for configuration. Reads from .env (via python-dotenv)
and exposes everything BOTH the FastAPI backend and the Streamlit frontend need.

The frontend imports a thin root-level `config.py` shim that re-exports the
constants below, so there is only one place to change settings.
"""
import os
from dotenv import load_dotenv, find_dotenv

# Locate and load the .env (remembering where we looked, for the Settings page)
_ENV_FILE = find_dotenv(usecwd=True)
ENV_SEARCHED = [
    (os.path.join(os.getcwd(), ".env"), os.path.exists(os.path.join(os.getcwd(), ".env"))),
    (_ENV_FILE or "(none found)", bool(_ENV_FILE)),
]
if _ENV_FILE:
    load_dotenv(_ENV_FILE)
else:
    load_dotenv()


def _bundled_sqlite_url() -> str:
    """Absolute sqlite URL to the smartrfp.db that ships next to the project."""
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
    return "sqlite:///" + os.path.join(here, "smartrfp.db").replace("\\", "/")


class Settings:

    # ---- Database -------------------------------------------------------- #
    # If DATABASE_URL is unset, fall back to the bundled SQLite file so the
    # app always runs (handy for a presentation when Postgres isn't up).
    DATABASE_URL = os.getenv("DATABASE_URL") or _bundled_sqlite_url()

    # ---- LLM (Groq) ------------------------------------------------------ #
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    # ---- Retrieval (RAG) ------------------------------------------------- #
    # Number of knowledge-base chunks the RAG agent retrieves per query.
    RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))

    # ---- Other providers / tracing -------------------------------------- #
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "SmartRFP")

    # ---- App / UI constants (used by the Streamlit frontend) ------------ #
    APP_NAME = "SmartRFP"
    SUPPORTED_TYPES = ["pdf", "docx", "txt"]
    MAX_UPLOAD_MB = 50
    REVIEWER_ROLES = ["Junior", "Senior", "Supervisor", "SME", "Bid Manager"]

    # Where the .env was found (shown on the Settings page)
    ENV_FILE = _ENV_FILE or ""
    ENV_SEARCHED = ENV_SEARCHED


settings = Settings()
