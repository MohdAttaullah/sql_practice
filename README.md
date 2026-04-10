# SQL Practice Lab ⚡

**Interactive SQL Practice Platform for Data Engineer Interview Preparation**

A production-grade web-based SQL lab focused on PySpark SQL / Spark SQL style questions. Practice real data engineering scenarios with instant query execution, smart validation, and comprehensive progress tracking.

![Stack](https://img.shields.io/badge/Next.js-14-black) ![Stack](https://img.shields.io/badge/FastAPI-0.111-green) ![Stack](https://img.shields.io/badge/DuckDB-1.0-yellow) ![Questions](https://img.shields.io/badge/Questions-53-blue)

---

## Features

- **53 curated questions** covering joins, window functions, aggregations, deduplication, CDC, SCD, data quality, ETL, and more
- **12 realistic datasets** (orders, customers, products, sellers, employees, transactions, events, inventory, pipeline logs, reconciliation, SCD)
- **SQL Editor** with syntax highlighting (CodeMirror 6)
- **Instant query execution** against DuckDB
- **Smart validation** with diagnostic feedback (wrong aggregation, missing filter, duplicate rows, null issues)
- **PySpark DataFrame API** equivalents for every question
- **Progress tracking** — solved count, accuracy, topic-wise and difficulty-wise performance
- **Bookmarks & Notes** per question
- **Dark mode** professional UI

## Pages

| Page | Description |
|------|-------------|
| Dashboard | Stats overview, recent activity, quick start |
| Question Bank | Filterable list by difficulty, tag, search |
| Practice Workspace | SQL editor + run + validate + output tables |
| Dataset Explorer | Browse all tables, schemas, and data previews |
| Solutions | SQL solutions + PySpark equivalents for all questions |
| Progress Tracker | Charts, topic-wise and difficulty-wise performance |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### 1. Clone and setup

```bash
git clone <repo-url>
cd sql-practice
```

### 2. Start the backend

```bash
cd backend
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload --port 8000
```

The database is automatically seeded on first startup.

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the app

Navigate to **http://localhost:3000**

---

## Docker Setup

```bash
docker-compose up --build
```

This starts both backend (port 8000) and frontend (port 3000).

---

## Architecture

```
Browser (Next.js 14) ──── REST API ──── FastAPI (Python)
                                            │
                                  ┌─────────┴────────┐
                                  │                    │
                            DuckDB (queries)    SQLite (progress)
```

- **Frontend**: Next.js 14 App Router, Tailwind CSS, CodeMirror 6, Recharts, Lucide Icons
- **Backend**: FastAPI with DuckDB for SQL execution and SQLite for progress tracking
- **Query Engine**: DuckDB — supports window functions, CTEs, QUALIFY, and most Spark SQL syntax

## Folder Structure

```
sql-practice/
├── backend/
│   ├── main.py              # FastAPI entrypoint
│   ├── database/
│   │   ├── engine.py         # DuckDB connection manager
│   │   └── seed.py           # Table creation & seeding
│   ├── routers/
│   │   ├── questions.py      # Question bank API
│   │   ├── execute.py        # SQL execution endpoint
│   │   ├── validate.py       # Answer validation
│   │   ├── datasets.py       # Dataset explorer API
│   │   └── progress.py       # Progress tracking API
│   ├── models/
│   │   ├── question.py       # Pydantic models
│   │   └── progress.py       # SQLAlchemy ORM models
│   ├── services/
│   │   └── evaluator.py      # Smart answer comparison engine
│   ├── data/
│   │   ├── questions.json    # 53-question bank
│   │   └── seed_data.py      # Dataset definitions
│   └── tests/
│       ├── test_evaluator.py
│       └── test_execute.py
│
├── frontend/
│   └── src/
│       ├── app/              # Next.js pages
│       ├── components/       # React components
│       └── lib/              # API client & types
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Running Tests

```bash
# Backend tests (22 tests)
python -m pytest backend/tests/ -v

# Frontend build check
cd frontend && npm run build
```

## Question Topics Covered

| Topic | Count | Examples |
|-------|-------|---------|
| Aggregations | 12 | Revenue by seller, Daily GMV, CLV |
| Window Functions | 10 | Running total, Rolling avg, Ranking |
| Joins | 10 | Multi-table, Anti-join, Self-join |
| Data Quality | 6 | Null PKs, Invalid status, Unmatched FKs |
| Deduplication | 5 | Duplicate detection, Dedup with ROW_NUMBER |
| CDC / SCD | 5 | SCD2 history, Point-in-time lookup |
| ETL / Incremental | 5 | Pipeline failure rate, Recon mismatches |
| Ranking | 5 | DENSE_RANK, Top-N per group |
| Date Functions | 5 | MoM growth, Day-of-week analysis |

## Future Enhancements

- [ ] Timer mode for interview simulation
- [ ] Random question mode
- [ ] Mock test mode with scoring
- [ ] AI-powered hints (OpenAI/Gemini integration)
- [ ] User authentication for multi-user support
- [ ] Question submission / custom questions
- [ ] Performance analytics with charts
- [ ] Export progress reports

---

Built for Data Engineers preparing for PySpark / Spark SQL interviews. 🚀
