# Portfolio

This portfolio documents my journey building end-to-end ML systems with a focus on infrastructure, deployment patterns, monitoring, and symbolic NLP. All projects are solo implementations designed to solve real problems, explore production-oriented architecture, and build fluency in ML engineering.

---

## **Core Projects: Systematic ML Engineering**

These projects apply real-world engineering patterns—like modular pipelines, CI/CD, monitoring, and cloud storage—to learning and personal-use contexts. They're not scaled production systems but working implementations that reflect how production systems are built.

| Project | Description | Type | Stack | Status | Repo |
|--------|-------------|------|--------|--------|------|
| `PCC` | ML inference pipeline for classifying privacy intent using BigQuery orchestration, dynamic model loading, and logging via Looker | ML Pipeline | BigQuery, MiniLM, Docker, GCS, Looker | 🟢 Running | [Repo](https://github.com/naaas94/PCC) |
| `model-training-pipeline` | End-to-end training pipeline with dataset curation, hyperparameter tuning, evaluation, and model registry | MLOps | MLflow, scikit-learn, GCS, Random Search | 🟢 Complete | [Repo](https://github.com/naaas94/model-training-pipeline) |
| `data-pipeline` | NLP-focused data pipeline for synthetic data creation and feature extraction with full lineage tracking | Data Eng | Pandas, TF-IDF, SentenceTransformers | 🟢 Complete | [Repo](https://github.com/naaas94/data-pipeline) |
| `simple-model-api` | FastAPI service for model inference with LLM routing, Docker deployment, GitHub Actions, and metrics logging | ML Infra | FastAPI, Docker, GitHub Actions, Prometheus | 🟡 In Progress | [Repo](https://github.com/naaas94/simple-model-api) |
| `agentic-reviewer` | Prototype for a retrieval-augmented validation system that semantically audits ML predictions | ML Engineering | Python, FastAPI, RAG, LLMs | 🟡 In Progress | [Repo](https://github.com/naaas94/agentic-reviewer) |

---

## **Advanced Projects: Symbolic & Semantic NLP**

Planned and ongoing experiments that apply symbolic reasoning and embedding-based modeling to more abstract domains, often driven by personal use cases.

| Project | Description | Type | Stack | Status | Repo |
|--------|-------------|------|--------|--------|------|
| `embedding-mapper` | Tool to visualize and compare sentence embeddings across domains using UMAP + interactive plots | NLP | SentenceTransformers, UMAP, Plotly | 🟡 In Progress | [Repo](https://github.com/naaas94/embedding-mapper) |
| `SNR QuickCapture` | Semantic ingestion prototype for structured note routing with symbolic parsing and hybrid storage | NLP Infra | Python, SQLite, FAISS, Prometheus | 🟡 In Progress | [Repo](https://github.com/naaas94/quick-capture-snr) |
| `dl-symbolic-perception` | Prototype for visual-semantic grounding using CLIP/CNN for symbolic reasoning tasks | DL/NLP | PyTorch, CLIP, torchvision | 🔴 Planned | TBD |

---

## **System Design Highlights**

### **End-to-End Engineering Patterns**
- Full training-to-inference pipelines with config management and version control
- Deployed inference services with structured input validation and logging
- Personal-scale monitoring stacks using Prometheus and Looker
- GitHub Actions used for CI/CD in containerized environments

### **Data & Model Ops**
- Custom training loops with hyperparameter tuning (random search)
- Model performance tracked via MLflow
- Cloud-native storage and artifact management (GCS, BigQuery)
- Schema enforcement via Pydantic

### **Observability & Robustness**
- Basic alerting via metrics collection and error logs
- Failure recovery logic in pipelines (e.g., retries, fallbacks)
- Monitoring dashboards to visualize pipeline output and drift

---

## **Design Ethos**

- **Practical over polished**: These projects solve real tasks I care about (e.g. note capture, audit validation, classification pipelines)
- **Pattern-driven**: Designed using the same concepts that power scaled systems, but built for individual use
- **Learning through building**: Each implementation reflects deliberate practice, not résumé padding

---

## **Follow My Work**

I post weekly updates on [LinkedIn](https://linkedin.com/in/alejandro-garay-338257243) to share insights on system design, ML pipelines, and symbolic reasoning with LLMs.