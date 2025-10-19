# Alejandro Garay — AI Solutions Architect (NLP/RAG/Agentic)

**I design, ship, and evaluate end‑to‑end AI systems** with a focus on NLP: retrieval‑augmented generation (RAG), agentic workflows, evaluation harnesses, and production patterns at individual scale. This repo is the **entry point** to my portfolio: code, diagrams, and evidence.

**Last updated:** 2025‑10‑19

---

## At a glance

* **Primary vector:** AI/ML **Solutions Architect** (NLP‑heavy: RAG, agents, finetuning/evals)
* **Differentiator:** symbolic‑linguistic rigor + production patterns (pipelines, orchestration, testing, monitoring) rather than demo‑only prototypes
* **Proof mindset:** every featured project exposes **Quickstart → Metrics → Logs** so reviewers can verify claims in minutes

> Short link to share: `github.com/<your‑org or user>/portfolio`

---

## Hiring signals (pattern → evidence)

| Real‑world pattern                             | What I built                      | Evidence                                                             | First file to open                                                 |
| ---------------------------------------------- | --------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Ingestion → Train → Evaluate → Serve → Monitor | **Model Training Pipeline (MTP)** | CI badge, MLflow runs, deterministic seeds, latency & cost snapshots | `mtp/README.md` → `examples/minimal_run.py`                        |
| RAG with retrieval quality gates               | **Lightweight RAG Service**       | recall@k, precision@k, answer faithfulness, context‑utilization      | `rag-service/README.md` → `scripts/eval_rag.py`                    |
| Post‑hoc guardrails/verification               | **Agentic Reviewer**              | hallucination checks, citation verification, rubric‑based scoring    | `agentic-reviewer/README.md` → `examples/review_demo.ipynb`        |
| Productionized text classification             | **Privacy Case Classifier (PCC)** | F1/accuracy with data slices; confusion matrix; error analysis       | `pcc/README.md` → `notebooks/pcc_demo.ipynb`                       |
| Observability for LLM APIs                     | **Simple Model API (SMA)**        | Prometheus metrics (RPS, P50/P95), structured logs, k6 load test     | `simple-model-api/README.md` → `make loadtest`                     |
| Embedding analysis & migration                 | **Embedding Mapper**              | pairwise shifts, trust‑region plots, retrieval deltas                | `embedding-mapper/README.md` → `examples/compare_embeddings.ipynb` |

---

## Architecture (portfolio map)

```mermaid
flowchart LR
  subgraph Data Layer
    SRC[Raw corpora / CSV / APIs]
    FEAT[Feature/Embedding Store]
  end

  subgraph Build & Train
    EDP[EDP - Enterprise Data Pipeline]
    MTP[MTP - Model Training Pipeline]
    REG[Model Registry]
  end

  subgraph Serving & Apps
    SMA[Simple Model API]
    RAG[RAG Service]
    PCC[PCC Classifier]
    AR[Agentic Reviewer]
  end

  subgraph Observability & Eval
    EVAL[Eval Harness]
    LOGS[Logs/Metrics (Prometheus/Grafana)]
  end

  SRC --> EDP --> MTP --> REG --> SMA
  FEAT <--> RAG
  PCC --> SMA
  SMA --> LOGS
  RAG --> LOGS
  SMA --> AR
  RAG --> AR
  MTP --> EVAL
  RAG --> EVAL
```

* Diagram asset: `/docs/architecture.png` (PNG export); source: `/docs/architecture.mmd` (Mermaid)

---

## Quickstart (10‑minute path)

> One flow to prove reproducibility and observability.

```bash
# 1) Clone and bootstrap
git clone https://github.com/<user>/portfolio && cd portfolio
make dev            # creates venv, installs pinned deps

# 2) Configure
cp .env.example .env # fill in optional keys (none required for local demo)

# 3) Minimal end‑to‑end
make demo           # runs: data → train (MTP) → serve (SMA) → eval → metrics dump

# 4) See metrics & logs
make up-metrics     # launches Grafana/Prometheus locally (docker-compose)

# 5) Run tests & quality gates
make test lint type
```

* Determinism: global seed `42`, `PYTHONHASHSEED=0`, cuDNN deterministic on where relevant.
* Sample data fixtures live under `data/fixtures/` (no external downloads needed).

---

## Evaluation (RAG/LLM + systems)

**Retrieval metrics**

* `recall@k`: fraction of queries where at least one gold doc is in top‑k.
* `precision@k`: fraction of top‑k that are relevant.
* `MRR@k`: mean reciprocal rank of first relevant doc within k.
* `nDCG@k`: graded relevance with position discount.

**Answer‑level metrics**

* **Faithfulness**: proportion of claims grounded in retrieved context (LLM‑ or rule‑based).
* **Context utilization**: % of answer tokens attributable to provided context.
* **Answer correctness**: labeling via gold answers or rubric (exact/partial match).

**Operational**

* **Latency** `P50/P95`, **throughput** `RPS`, **cost/request**, **timeouts/error rate**, and **SLO/error budget** (e.g., `P95 < 800ms`, monthly error budget 0.5%).

Each featured repo ships an `eval/` folder with scripts + JSON logs compatible with the shared dashboard panels in `observability/`.

---

## Observability

* **Stack:** `prometheus`, `grafana`, `opencensus` (exporters), structured JSON logs.
* Dashboards: `/observability/grafana/provisioning/` (panels for latency, RPS, errors, cost).
* Alerts: `/observability/alerts/` (ex: high P95, elevated 5xx, drift detector fired).
* Screenshots for reviewers: `/docs/img/observability_*.png`.

Run locally:

```bash
make up-metrics   # Grafana on http://localhost:3000 (admin/admin locally)
```

---

## Featured projects

### 1) PCC — Privacy Case Classifier

* **Problem**: classify privacy requests/cases into workflow buckets.
* **Pattern**: supervised text classification + error analysis + data slices.
* **Implementation**: `scikit-learn`/`PyTorch` (optionally), Hydra configs, Docker, MLflow runs.
* **Evidence**: macro‑F1 on fixtures; slice metrics (by entity/type); confusion matrix.
* **Start here**: `pcc/notebooks/pcc_demo.ipynb`
* **Status**: In progress — 2025‑10

### 2) MTP — Model Training Pipeline

* **Problem**: reproducible training with experiment tracking & registries.
* **Pattern**: `MLflow` + deterministic training + pinned deps + structured configs.
* **Implementation**: Makefile targets (`make train/eval/register`), CI, Docker multi‑stage.
* **Evidence**: MLflow artifacts, metrics tables, model in `registry/`.
* **Start here**: `mtp/examples/minimal_run.py`
* **Status**: Stable — 2025‑10

### 3) SMA — Simple Model API

* **Problem**: serve models with SLAs and visibility.
* **Pattern**: FastAPI + Prometheus + k6 load test + JSON logs.
* **Implementation**: `docker-compose up`, `/metrics` endpoint, request IDs, middleware timing.
* **Evidence**: P50/P95 latency charts; RPS under load; error rates.
* **Start here**: `simple-model-api/README.md` → `make loadtest`
* **Status**: Stable — 2025‑10

---

## More projects

* **RAG Service** — retrieval + rerank + prompt templates + eval harness (`recall@k`, faithfulness).
* **Agentic Reviewer** — post‑hoc auditing loop (citation checks, rubric scores, red‑team prompts).
* **Embedding Mapper** — compare embedding models; visualize drift and retrieval deltas.
* **EDP (Enterprise Data Pipeline)** — ingestion/validation to dataset release with schema contracts.

Each has: Quickstart, config examples, and `eval/` outputs.

---

## Operating standards (applies to all repos)

* [x] Pinned dependencies & lockfiles
* [x] Deterministic seeds & reproducible runs
* [x] Makefile targets for common actions
* [x] CI: lint (`ruff`), typecheck (`mypy`/`pyright`), tests (`pytest`)
* [x] Structured logs + metrics hooks
* [x] Minimal data fixtures checked into repo
* [x] Doc: Quickstart + E2E path ≤10 minutes

Badges (add per‑repo):

```
[![CI](https://img.shields.io/github/actions/workflow/status/<user>/<repo>/ci.yml?branch=main)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
```

---

## Repo layout (monorepo‑style pointers)

```
portfolio/
├─ pcc/
├─ mtp/
├─ simple-model-api/
├─ rag-service/
├─ agentic-reviewer/
├─ embedding-mapper/
├─ edp/
├─ observability/
└─ docs/
```

---

## Limitations & next steps (scoped)

* Replace synthetic fixtures with small anonymized real‑world‑like sets (scripted in `data/`); keep size ≤10MB.
* Add golden sets for RAG faithfulness with explicit citation spans.
* Provide a one‑click `docker compose up` that brings **SMA + RAG + Grafana** together.

---

## About me

I come from linguistics/philosophy/translation. I use that symbolic lens to design reliable NLP systems: clear problem framing, careful retrieval/representation choices, and evaluation you can trust.

* LinkedIn: <link>
* Substack: <link>
* Email: <link>
