---
noteId: "bf2c0cd0625611f084f08ddb7af7baaa"
tags: []

---

# Model Training Pipeline System

A modular, production-ready pipeline for training and versioning privacy intent classification models. Designed for integration with the PCC system and ready for plug-and-play use.

## Quick Start

### 1. Prepare Your Data
Place your data file (CSV, Parquet, or PKL) in the `src/data/` directory using the naming convention:
```
balanced_dataset_YYYYMMDD.csv
```
Where `YYYYMMDD` is the date in format YYYYMMDD (e.g., `balanced_dataset_20241201.csv`).

Ensure your data matches the required schema:

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Input text for classification |
| `intent` | string | Classification label |
| `confidence` | float | Confidence score |
| `timestamp` | string | ISO 8601 timestamp |
| `text_length` | int | Character count |
| `word_count` | int | Word count |
| `has_personal_info` | boolean | Personal info flag |
| `formality_score` | float | Formality metric |
| `urgency_score` | float | Urgency metric |
| `embeddings` | list[float] | 584-dim embeddings (384 sentence + 200 TF-IDF) |

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Pipeline
```bash
python scripts/train_pipeline.py
```

**Outputs:**
- Model: `models/pcc_model.joblib` (local) + GCS backup
- Metadata: `models/metadata.json` + GCS backup  
- Predictions: `output/predictions.parquet`
- Metrics: `output/metrics.json`
- Registry: `models/model_registry.json`

## How It Works

### Intelligent Dataset Monitoring
The pipeline now **intelligently monitors** for new training datasets instead of running on a fixed schedule:

1. **Dataset Discovery**: Automatically finds datasets matching the pattern `balanced_dataset_YYYYMMDD.csv`
2. **Change Detection**: Compares dataset dates with the last training date
3. **Conditional Training**: Only runs the full pipeline if new data is available
4. **Smart Exit**: Exits gracefully with "No new training dataset" message if no new data

### Dataset Naming Convention
```
src/data/
├── balanced_dataset_20241201.csv  # December 1, 2024
├── balanced_dataset_20241202.csv  # December 2, 2024
└── balanced_dataset_20241203.csv  # December 3, 2024
```

### Pipeline Behavior
- **With New Data**: Runs complete training pipeline and updates model
- **Without New Data**: Exits with success message "No new training dataset"
- **First Run**: Treats any available dataset as new data

## Performance Expectations

### Test Results
The pipeline achieves **perfect scores (1.0000 accuracy/F1)** on synthetic test data due to:
- Clear, non-overlapping intent patterns
- Rich 584-dimensional feature space
- Balanced class distribution

### Real-World Performance
With actual user data, expect **0.7-0.9 accuracy/F1** due to:
- Natural language ambiguity
- Class imbalance
- Text variation and noise
- Edge cases and typos

## Project Structure

```
model-training-pipeline/
├── config.yaml                # Pipeline configuration
├── src/data/                  # Input data directory (with YYYYMMDD naming)
├── scripts/
│   ├── train_pipeline.py      # Main pipeline script (with dataset monitoring)
│   ├── trigger_training.py    # Script to trigger pipeline manually/programmatically
│   └── manage_models.py       # Model registry CLI
├── src/model_training_pipeline/
│   ├── data.py                # Data ingestion, validation & dataset discovery
│   ├── preprocessing.py       # Embedding, balancing, splitting
│   ├── training.py            # Model training & optimization
│   ├── evaluation.py          # Model evaluation & metrics
│   ├── persistence.py         # Model & output saving
│   ├── model_registry.py      # Model tracking & registry
│   └── utils.py               # Config & logging utilities
├── tests/                     # Unit tests
├── models/                    # Saved models & registry
├── output/                    # Predictions & metrics
└── logs/                      # Monitoring logs
```

## Pipeline Stages

1. **Dataset Discovery** → Find latest dataset matching naming pattern
2. **Change Detection** → Check if dataset is newer than last training
3. **Conditional Logic** → Exit if no new data, proceed if new data found
4. **Data Ingestion** → Load from discovered dataset
5. **Data Validation** → Schema & embedding validation
6. **Preprocessing** → SMOTE balancing + stratified split
7. **Model Training** → Logistic Regression + hyperparameter optimization
8. **Evaluation** → F1, Accuracy, ROC-AUC, PR-AUC metrics
9. **Persistence** → Save model, predictions, logs
10. **Registry Update** → Track runs, metadata, GCS paths

## Configuration

All pipeline behavior is controlled via `config.yaml`:

```yaml
# Key sections
data:
  path: "src/data/balanced_dataset_YYYYMMDD.csv"  # Template path
  naming_pattern: "balanced_dataset_YYYYMMDD.csv"  # Pattern for discovery
  test_size: 0.2

preprocessing:
  balancing: "smote"
  embedding_model: "sentence-transformers/all-MiniLM-L6-v2"

model:
  type: "LogisticRegression"
  search_method: "random"  # 'grid', 'random', 'none'
  n_iter: 20              # For random search
  cross_val: false
  scoring: "f1"
```

## Triggering Training

### Manual Trigger
```bash
# Run pipeline directly
python scripts/train_pipeline.py

# Or use the trigger script
python scripts/trigger_training.py
```

### Programmatic Trigger
```bash
# From external systems (data pipelines, CI/CD, etc.)
python scripts/trigger_training.py
```

### Kubernetes Job
```bash
# Create a job from the template
kubectl apply -f k8s/job-template.yaml
```

## Hyperparameter Optimization

### Available Methods

| Method | Speed | Effectiveness | Best For |
|--------|-------|---------------|----------|
| **Random Search** | Fast | Better | **Recommended** |
| Grid Search | Medium | Good | Small parameter spaces |
| No Search | Fastest | Basic | Quick testing |

### Random Search (Recommended)
```yaml
model:
  search_method: 'random'
  n_iter: 20
```

**Advantages:**
- Tests continuous parameter ranges (C: 0.01 to 1000)
- Often finds better hyperparameters than grid search
- Faster exploration of parameter space

### Grid Search
```yaml
model:
  search_method: 'grid'
```

**Advantages:**
- Exhaustive search of predefined combinations
- Reproducible results
- Good for small parameter spaces

## Model Registry Management

Use the CLI tool to manage models:

```bash
# List recent model runs
python scripts/manage_models.py list

# Show latest successful model
python scripts/manage_models.py latest

# Get performance summary
python scripts/manage_models.py summary

# Export registry to CSV
python scripts/manage_models.py export

# Get details for specific model version
python scripts/manage_models.py get --version v20250729084352
```

### Registry Features
- **Run Tracking**: Every pipeline run logged with full metadata
- **Dataset Tracking**: Dataset dates recorded for each training run
- **Performance History**: Track F1 scores, accuracy over time
- **GCS Integration**: Automatic tracking of model locations
- **Export Capabilities**: Export registry data for analysis
- **Failure Tracking**: Failed runs logged for debugging

## GCS Integration

Models are automatically saved to Google Cloud Storage:

```
gs://pcc-datasets/pcc-models/
├── v20250729084352/
│   ├── model.joblib
│   └── metadata.json
├── v20250729084415/
│   ├── model.joblib
│   └── metadata.json
└── ...
```

**Features:**
- Automatic versioning with timestamp-based versions
- Complete metadata storage alongside models
- Easy retrieval from GCS paths
- Local + GCS backup strategy

## Testing

Run all unit tests:
```bash
pytest
```

## Key Features

- **Intelligent Monitoring**: Only trains when new datasets are available
- **Dynamic Dataset Discovery**: Automatically finds datasets by date pattern
- **Config-driven**: All behavior controlled via `config.yaml`
- **Modular**: Each stage is a separate, swappable module
- **Schema-compliant**: Ready for downstream PCC integration
- **Secure**: Uses `ast.literal_eval()` for safe data parsing
- **Extensible**: Add new models/features with minimal changes
- **Unit tested**: Core modules covered by tests
- **Logging**: Comprehensive logging throughout pipeline

## Production Workflow

1. **New Dataset Arrives** → Place in `src/data/` with YYYYMMDD naming
2. **Trigger Pipeline** → Run `python scripts/train_pipeline.py` or use trigger script
3. **Automatic Detection** → Pipeline discovers and validates new dataset
4. **Conditional Training** → Only trains if dataset is newer than last training
5. **Model Saved** → Automatically saved to GCS with versioning
6. **Registry Updated** → Run tracked with performance metrics and dataset date
7. **Smart Exit** → Exits gracefully if no new data available

## Recent Enhancements

- **Dataset Monitoring**: Intelligent detection of new training datasets
- **Conditional Training**: Only runs pipeline when new data is available
- **Dynamic Naming**: Support for YYYYMMDD dataset naming convention
- **Smart Exit Logic**: Graceful exit with "No new training dataset" message
- **Trigger Script**: Easy manual/programmatic pipeline triggering
- **Kubernetes Job Template**: Replaces fixed CronJob with on-demand jobs
- **Schema Consistency**: Fixed column naming across modules
- **Security**: Replaced `eval()` with `ast.literal_eval()`
- **Dependencies**: Added missing packages (imbalanced-learn, PyYAML, google-cloud-storage)
- **Random Search**: Added for better hyperparameter optimization
- **GCS Integration**: Automatic model saving to Google Cloud Storage
- **Model Registry**: Complete tracking system for all runs
- **CLI Tools**: Management interface for model registry

## Future Enhancements

### High Priority
- **Enhanced Metrics**: Training/validation scores, per-class analysis
- **Bayesian Optimization**: Optuna integration for advanced hyperparameter tuning
- **Cross-Validation**: Detailed CV metrics across folds

### Medium Priority  
- **Automated Workflows**: GitHub Actions for CI/CD
- **Model Monitoring**: Drift detection and performance tracking
- **Data Quality**: Enhanced validation and profiling

### Low Priority
- **Advanced MLOps**: Docker, Kubernetes deployment
- **API Endpoints**: RESTful model serving
- **Security**: Encryption, access control, compliance

*Each enhancement can be implemented incrementally without breaking existing functionality.*

---

**This pipeline now intelligently monitors for new datasets and only trains when new data is available!**

For questions or customization, see the code comments and config file, or contact the pipeline author. 
