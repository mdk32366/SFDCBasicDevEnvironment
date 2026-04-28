# Agentforce Vibes

A development environment for building intelligent agents using Salesforce Apex and Python.

## Prerequisites

- Node.js 16+ (for Salesforce CLI)
- Python 3.9+
- Salesforce CLI (sfdx)
- Git

## Quick Start

### 1. Install Salesforce CLI
```bash
npm install -g @salesforce/cli
```

### 2. Set Up Python Environment
```bash
cd python
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3. Authenticate with Salesforce (Dev Org)
```bash
sf login org web --alias vibes-org
sf config set target-org vibes-org
```

Your Dev Org will persist indefinitely (unlike Scratch Orgs which expire after 30 days).

## Project Structure

- **force-app/main/default/** - Salesforce Apex and Lightning components
- **python/** - Python agent code and utilities
- **data-cloud/** - Data Cloud unified catalog configuration and ML datasets
- **config/** - Configuration files for Salesforce and development
- **.vscode/** - VS Code settings and tasks

## Development

### Apex Development
- Use VS Code with Salesforce Extension Pack
- Deploy code to Dev Org with `sf project deploy start -o vibes-org`
- Retrieve changes with `sf project retrieve start -o vibes-org`

### Python Development
- Run scripts from `python/` directory
- Install additional packages with `pip install <package>` and update `requirements.txt`

### Data Cloud Development
- Configure unified catalog in `data-cloud/schemas/unified_catalog.json`
- Create data connectors and transformations
- Generate ML training datasets
- See [Data Cloud Setup Guide](data-cloud/SETUP_GUIDE.md) for detailed instructions

## Useful Commands

```bash
# Salesforce CLI
sf org list
sf project deploy start -o vibes-org
sf project retrieve start -o vibes-org

# Python
pip install -r python/requirements.txt
python python/agent.py

# Data Cloud
cd data-cloud
python orchestrator.py
python -m pytest test_datacloud.py
```

## Data Cloud Unified Catalog

Agentforce Vibes includes a unified Data Cloud catalog for ML-driven agent training:

**Core Entities:**
- **Account, Contact, Opportunity** - Salesforce core objects
- **Policy** - External policy management data

**Multi-source Integration:**
- Salesforce production objects
- External APIs and webhooks  
- CSV file imports
- Third-party systems (Marketo, SAP, etc.)

**ML Features:**
- Automatic train/test dataset generation
- Feature engineering and auto-generation
- Multiple export formats (CSV, Parquet, JSON)
- Data quality validation
- 2-year retention for ML training

### Quick Start

```bash
cd data-cloud

# View catalog configuration
python orchestrator.py

# Run complete sync pipeline
python -c "from orchestrator import DataCloudOrchestrator; o = DataCloudOrchestrator(); print(o.get_catalog_summary())"

# Create ML training dataset
python -c "from transformations.ml_training import MLTrainingDatasetManager; m = MLTrainingDatasetManager('default'); print('Ready for ML')"
```

## Documentation

- [Data Cloud Setup Guide](data-cloud/SETUP_GUIDE.md) - Complete Data Cloud configuration
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Project setup instructions
