# SmartRFP — AI Document Processing System (RAG + Live Pricing + Human-in-the-Loop)

An end-to-end, runnable implementation of the SmartRFP architecture and PRD:
upload an RFP → parse requirements → two agents run in parallel (RAG retrieval +
live pricing) → synthesize a draft with flags → a human approves/edits/rejects →
export to **DOCX / PDF / TXT**.

Built with **Streamlit + Groq + SQLite** (instead of OpenAI + PostgreSQL).

---

## 1. What you get

| Page | What it does |
|------|--------------|
| **Upload** | File upload (PDF/DOCX/TXT) + client details + **one "Generate Response" button** that runs the whole pipeline |
| **Dashboard** | Metric cards + a table of all RFPs, filterable by **reviewer role** (Junior / Senior / Supervisor / SME) and status; "Open" any row |
| **Review** | Full RFP details — draft sections, sources, **compliance / hallucination / missing-info flags**, requirements, pricing table, audit log — with **Approve / Edit inline / Send back / Reject** (the human gate) |
| **Export** | Appears after approval → **Download DOCX / PDF / TXT** (real files) |
| **Settings** | Groq status, knowledge base management, delete RFPs |

---

## 2. How to run (7 steps)

> ⚠️ **Keep the folder structure intact.** Always unzip the provided `smartrfp.zip`
> and run from the unzipped `smartrfp/` folder. Do **not** copy the `.py` files out
> into a single flat folder — `agents/` and `utils/` are Python packages, and
> flattening them causes `ModuleNotFoundError: No module named 'utils'`.

```bash
# 1. Go into the project folder (the one containing app.py)
cd smartrfp

# 2. (recommended) create a virtual environment
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (optional but recommended) add your Groq key
cp .env.example .env          # Windows: copy .env.example .env
#   then open .env and paste your key into GROQ_API_KEY=...

# 5. Launch the FastAPI server
uvicorn backend.main:app --reload

#6. Launch the app
streamlit run app.py

#7. Launch Prometheus Scraping:
(Download Prometheus ZIP, copy the files OTHER THAN the .yml into this following folder)
cd monitoring\prometheus
.\prometheus.exe --config.file=prometheus.yml
```

Streamlit App: http://localhost:8501
FastAPI Swagger Dashboard: http://127.0.0.1:8000/docs
Prometheus Metrics: http://localhost:8000/metrics
Grafana Dashboard: http://localhost:9090/

> **No Groq key?** The app still runs in **demo mode** — it produces deterministic,
> source-grounded drafts so you can see the full flow. Add a key any time for real
> LLM-written drafts; nothing else changes.

> Groq rotates models. The default is `openai/gpt-oss-20b`. If you get a
> "model not found" error, open `.env`, set `GROQ_MODEL` to a current model from
> https://console.groq.com/docs/models (e.g. `openai/gpt-oss-120b`).

---

## 3. Try it end-to-end (no UI) — proves the backend works

```bash
python test_pipeline.py
```

This creates a sample RFP, runs the pipeline, prints requirements / draft sections /
flags / pricing, and writes `exports/acme_test.{txt,docx,pdf}`.

---

## 4. Project structure

```
SmartRFP/
├── app.py                  # Main Streamlit application and UI entry point
├── pipeline.py             # Orchestrates the end-to-end AI workflow
├── llm.py                  # Wrapper for Groq/OpenAI LLM calls
├── database.py             # SQLite repository used by the Streamlit application
├── config.py               # Root configuration shared by the application
├── evaluation.py           # Computes proposal quality and RAG evaluation metrics
├── metrics.py              # Prometheus/LangSmith runtime metrics and counters
├── requirements.txt        # Python package dependencies
├── state.py                # Streamlit session state management
├── guardrails.py           # Input/output validation and AI safety guardrails
│
├── agents/
│   ├── extractor.py        # Extracts requirements from uploaded RFP
│   ├── rag_agent.py        # Retrieves relevant past knowledge/content
│   ├── pricing_agent.py    # Generates pricing/cost information
│   └── draft_generator.py  # Produces proposal draft using LLM
│
├── ui/
│   ├── api.py              # HTTP client for communicating with the FastAPI backend
│   ├── dashboard.py        # Dashboard displaying RFPs, metrics and project status
│   ├── export.py           # UI for exporting generated proposals
│   ├── help_pg.py          # Help and user documentation page
│   ├── llm_eval.py         # Displays LLM and RAG evaluation metrics
│   ├── resource_cost.py    # Displays pricing and resource cost estimates
│   ├── review.py           # Human review, approval and regeneration interface
│   ├── settings.py         # Application configuration and environment settings page
│   ├── upload.py           # RFP upload page and analysis workflow
│   └── ui_utils.py         # Shared UI components, styling and helper functions
│
├── backend/
│   ├── config.py           # FastAPI configuration and environment settings
│   ├── crud.py             # SQLAlchemy CRUD operations for database access
│   ├── database.py         # SQLAlchemy engine, sessions and database connection
│   ├── main.py             # FastAPI application entry point and route registration
│   ├── models.py           # SQLAlchemy ORM models representing database tables
│   ├── schemas.py          # Pydantic request and response schemas
│   ├── services.py         # Business logic connecting API endpoints to the pipeline
│   ├── __init__.py         # Marks backend as a Python package
│   └── routes/
│       ├── dashboard.py    # Dashboard-related API endpoints
│       ├── export.py       # Proposal export API endpoints
│       ├── health.py       # Health check endpoint for service monitoring
│       ├── pricing.py      # Pricing retrieval API endpoints
│       ├── regenerate.py   # Endpoint to rerun the proposal generation pipeline
│       ├── review.py       # Human review and approval API endpoints
│       ├── upload.py       # RFP upload and analysis API endpoint
│       └── __init__.py     # Marks routes as a Python package
│── monitoring/
│   └── prometheus/
│       └── prometheus.yml  # Attches Prometheus to the project
├── utils/
│   ├── exporter.py         # PDF/DOCX export
│   └── file_handler.py     # File upload/parsing
│
├── exports/                # Generated PDF and DOCX proposal outputs
│
├── smartrfp.db             # SQLite database
│
├── tests/                  # Automated test suite
├── conftest.py             # Shared pytest fixtures and test configuration
│
├── unit/
│   ├── test_file_handler.py    # Unit tests for document parsing utilities
│   ├── test_database.py        # Unit tests for database operations
│   ├── test_extractor.py       # Unit tests for requirement extraction
│   ├── test_rag.py             # Unit tests for RAG retrieval
│   ├── test_pricing.py         # Unit tests for pricing agent
│   ├── test_draft.py           # Unit tests for proposal draft generation
│   ├── test_llm.py             # Unit tests for LLM wrapper
│   └── test_exporter.py        # Unit tests for export functionality
│
├── integration/
│   ├── test_pipeline.py            # Integration tests for the complete pipeline
│   ├── test_rag_database.py        # Tests interaction between RAG and database
│   ├── test_pipeline_database.py   # Tests pipeline persistence to the database
│   ├── test_draft_rag.py           # Tests draft generation using RAG context
│   └── test_export_pipeline.py     # Tests exporting generated proposals
│
└── e2e/
    ├── test_demo_pipeline.py   # End-to-end demo workflow test
    ├── test_real_pipeline.py   # End-to-end workflow using real documents
    └── test_ragas.py           # End-to-end evaluation using RAGAS metrics

pip install git+https://github.com/explodinggradients/ragas.git
```

The SQLite file `smartrfp.db` is created automatically on first launch.

---

## 5. How it maps to your architecture & PRD

| Your design | This project |
|-------------|--------------|
| Frontend (Streamlit) | `app.py` |
| Backend / business logic | `pipeline.py`, `database.py` |
| LLM (OpenAI → **Groq**) | `llm.py` |
| Orchestration (LangChain/LangGraph) | `pipeline.py` (`ThreadPoolExecutor` runs the two agents in parallel) |
| Agent 1 — RAG retrieval | `agents/rag_agent.py` |
| Agent 2 — Live web/pricing | `agents/pricing_agent.py` |
| Draft Generator (F4) | `agents/draft_generator.py` |
| Human-in-the-loop review | Review page in `app.py` |
| Vector DB (pgvector/FAISS) | TF-IDF retrieval (see note below) |
| Database (PostgreSQL → **SQLite**) | `database.py` |
| Export & audit trail (F6) | `utils/exporter.py` + `audit_log` table |

### Note on the "Vector DB"
Groq has no embeddings endpoint, and to keep the project **zero-setup** the RAG
agent uses **TF-IDF + cosine similarity** (scikit-learn) for relevance search.
It behaves the same way (retrieve the most relevant internal docs per requirement)
with no model downloads. To upgrade to true semantic embeddings, swap
`TfidfVectorizer` in `agents/rag_agent.py` for `sentence-transformers`
(`all-MiniLM-L6-v2`) — the function signature stays the same.

---

## 6. Safety behaviours from the PRD
- **Hallucination flag** — a draft claim (e.g. an SLA %) not found in any source is flagged.
- **Compliance flag** — compliance/data-residency content is flagged for SME confirmation.
- **Missing-info marker** — a requirement with no internal match is flagged, not faked.
- **Stale pricing** — pricing older than the current quarter is marked "STALE" and excluded from the total.
- **No export without approval** — the Export page blocks download until a human approves.
- **Audit trail** — every action (upload, parse, edit, approve, reject) is logged per RFP.

---

## 7. Troubleshooting
- **`ModuleNotFoundError: No module named 'utils'` (or `'agents'`)** → you're running
  from a folder where the `utils/` and `agents/` subfolders are missing or got
  flattened. Unzip `smartrfp.zip` fresh and run `streamlit run app.py` from inside
  the resulting `smartrfp/` folder so the package folders sit next to `app.py`.
- **`'source' is not recognized…` (Windows)** → use `venv\Scripts\activate`, not
  `source venv/bin/activate` (that's macOS/Linux syntax).
- **`streamlit: command not found`** → activate your venv, or run `python -m streamlit run app.py`.
- **Groq "model not found"** → update `GROQ_MODEL` in `.env` (see §2).
- **Legacy `.doc` upload fails** → convert to `.docx`, `.pdf`, or `.txt` first.
- **Want a clean slate** → delete `smartrfp.db` and restart.
```
