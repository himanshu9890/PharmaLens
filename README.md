# PharmaLens

Open-source AI-powered pharma BD intelligence platform. Search, score, and profile clinical trial licensing opportunities from public data.

**Current phase:** Phase 1 — Foundation MVP  
**License:** MIT

---

## Quick Start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

---

## Local Development

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env   # edit DATABASE_URL and REDIS_URL to point to local services
uvicorn backend.main:app --reload
```

Requires PostgreSQL 16 with pgvector and Redis 7 running locally.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api/*` to `http://localhost:8000` automatically.

---

## Architecture

```
ClinicalTrials.gov (free API)
        ↓
FastAPI backend (Python)
  ├── Redis cache (24h TTL)
  ├── PostgreSQL (trials table)
  └── /api/v1/trials endpoints
        ↓
React + TypeScript frontend
  ├── Search form with MeSH autocomplete
  ├── Sortable results table
  ├── Trial detail slide-in panel
  └── CSV export
```

## Phased Roadmap

| Phase | Status | Description |
|---|---|---|
| 1 — Foundation MVP | **In progress** | ClinicalTrials.gov search, results table, trial detail |
| 2 — Data Enrichment | Planned | WHO ICTRP, PubMed, OpenFDA, ChEMBL connectors + rule-based scoring |
| 3 — BD Intelligence | Planned | Composite AI scoring, KOL sentiment, watchlists, alerts |
| 4 — AI Analysis | Planned | Claude API integration, NL search, PDF reports, competitive charts |

## Data Sources (Phase 1)

- [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/api/v2/) — free, no auth required
- [NLM MeSH API](https://id.nlm.nih.gov/mesh) — MeSH term autocomplete

## Contributing

Issues and PRs welcome. See the full roadmap in `pharmalens_roadmap.md` for context on what's coming next. Good first issues: adding new filter fields, improving the MeSH term mapping, UI polish.
