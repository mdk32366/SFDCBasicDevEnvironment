# Data Cloud Setup - Quick Reference

## What's Been Created

Your Agentforce Vibes project now includes a complete **Salesforce Data Cloud** integration with:

### 1. Unified Catalog Schema
**File**: `data-cloud/schemas/unified_catalog.json`

- **4 Core Entities**:
  - Account (from Salesforce)
  - Contact (from Salesforce) 
  - Opportunity (from Salesforce)
  - Policy (from external sources)

- **3 Data Sources**:
  - Salesforce Production Org
  - External APIs (Policy Management)
  - CSV File Imports

- **ML Training Configuration**:
  - 2-year data retention
  - Auto feature generation
  - Multiple export formats (CSV, Parquet, JSON)

### 2. Data Connectors
**Directory**: `data-cloud/connectors/`

- **Salesforce Connector** (`salesforce_connector.py`):
  - OAuth2 authentication
  - SOQL query execution
  - Entity synchronization
  - Unified identity creation

- **Data Cloud Ingestor** (`data_cloud_ingestor.py`):
  - Record ingestion
  - Unified customer identity management
  - Batch processing

### 3. Data Transformation Pipeline
**Directory**: `data-cloud/transformations/`

- **Data Validator** (`data_pipeline.py`):
  - Schema validation
  - Data quality checks
  - Type validation

- **Data Transformer** (`data_pipeline.py`):
  - Data normalization
  - Entity joining
  - Feature matrix creation

- **ML Training Manager** (`ml_training.py`):
  - Automatic train/test split (80/20 default)
  - Dataset export (CSV, Parquet, JSON)
  - Dataset statistics and monitoring

- **Feature Engineer** (`ml_training.py`):
  - Auto-generate statistical features
  - Create custom features
  - Feature management and versioning

### 4. Orchestration
**File**: `data-cloud/orchestrator.py`

Complete pipeline orchestration:
- Authentication
- Entity synchronization
- Data validation
- ML dataset creation
- Pipeline monitoring

### 5. Testing
**File**: `data-cloud/test_datacloud.py`

Comprehensive unit tests for:
- Connector initialization and authentication
- Data validation (valid/invalid records)
- Data transformation (normalization, feature matrix)
- ML dataset creation and export
- Feature engineering

### 6. Documentation
**File**: `data-cloud/SETUP_GUIDE.md`

Complete setup guide including:
- Architecture overview
- Step-by-step configuration
- API setup in Salesforce
- Environment variables
- Data connector examples
- Transformation examples
- ML training examples
- Troubleshooting

## Quick Start

### 1. Test the Setup
```bash
cd data-cloud
python orchestrator.py
```

Output shows:
- Catalog summary with all entities
- Data sources configuration
- ML training enabled status

### 2. Run Unit Tests
```bash
cd data-cloud
python -m pytest test_datacloud.py -v
```

### 3. Create a Training Dataset
```python
from transformations.ml_training import MLTrainingDatasetManager

ml_manager = MLTrainingDatasetManager(workspace_id="default")

features = {
    "account_id": ["1", "2", "3", "4", "5"],
    "revenue": [100000, 250000, 150000, 500000, 300000]
}

dataset = ml_manager.create_training_dataset(
    name="Account_ML_Training",
    entity_names=["Account"],
    features=features,
    train_test_split=0.8
)

print(f"Created dataset: {dataset['dataset_id']}")
print(f"Training samples: {dataset['statistics']['training_samples']}")
print(f"Test samples: {dataset['statistics']['test_samples']}")
```

### 4. Export Training Data
```python
# Export as CSV for scikit-learn, TensorFlow, etc.
export = ml_manager.export_dataset(dataset_id, format="csv")
print(f"Download from: {export['file_path']}")

# Export as Parquet for big data tools
export = ml_manager.export_dataset(dataset_id, format="parquet")
```

## Integration with Agentforce Agent

Use unified customer data in your agent:

```python
from data_cloud.connectors.salesforce_connector import DataCloudIngestor

ingestor = DataCloudIngestor(workspace_id="default", api_key="your_api_key")

# Create unified customer identity
customer_360 = ingestor.create_unified_identity(
    contact_data=contact,
    account_data=account
)

# Use in agent context
agent.process_message(
    message="Analyze this customer opportunity",
    customer_context=customer_360
)
```

## Configuration in Salesforce

To activate this with your Dev Org:

1. **Enable Data Cloud** in Setup
2. **Create Connected App** for API access
3. **Generate API credentials** (Client ID, Secret)
4. **Update `.env`** with credentials
5. **Run orchestrator** to sync data

See `SETUP_GUIDE.md` for detailed Salesforce configuration steps.

## File Structure

```
data-cloud/
├── __init__.py
├── orchestrator.py              # Main orchestration engine
├── test_datacloud.py            # Unit tests
├── SETUP_GUIDE.md               # Complete setup documentation
├── QUICKSTART.md                # This file
├── schemas/
│   ├── __init__.py
│   ├── unified_catalog.json     # Unified catalog definition
│   └── uploads/                 # CSV import directory
├── connectors/
│   ├── __init__.py
│   └── salesforce_connector.py  # Salesforce integration
├── transformations/
│   ├── __init__.py
│   ├── data_pipeline.py         # Validation & transformation
│   ├── ml_training.py           # ML dataset management
│   └── exports/                 # ML dataset export directory
└── logs/                        # Sync and error logs
```

## Next Steps

1. ✅ Review `SETUP_GUIDE.md` for complete configuration
2. ✅ Run `python orchestrator.py` to verify setup
3. ✅ Enable Data Cloud in your Salesforce org
4. ✅ Create Connected App and get API credentials
5. ✅ Update `.env` with your credentials
6. ✅ Run full sync pipeline with real data
7. ✅ Create ML training datasets
8. ✅ Export data for model training
9. ✅ Integrate with your agent

## Support & Troubleshooting

See `SETUP_GUIDE.md` for:
- Detailed troubleshooting section
- Common issues and solutions
- Best practices
- Performance optimization

## Key Features

✅ **Multi-source data integration** - Salesforce, APIs, CSV, third-party  
✅ **Automatic data validation** - Schema compliance, data quality  
✅ **ML-ready datasets** - Auto train/test splits, feature engineering  
✅ **Flexible exports** - CSV, Parquet, JSON formats  
✅ **Unified identities** - Create 360° customer profiles  
✅ **Scalable architecture** - Batch processing, error handling  
✅ **Well-tested** - Comprehensive unit test coverage  
✅ **Fully documented** - Setup guide, examples, API docs  

---

**Ready to use Data Cloud with Agentforce Vibes!** 🚀
