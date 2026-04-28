# Salesforce Data Cloud - Unified Catalog Setup Guide

## Overview

This guide provides step-by-step instructions to set up a unified data catalog in Salesforce Data Cloud for Agentforce Vibes. The catalog integrates multiple data sources (Salesforce objects, external APIs, CSV files) for ML-driven agent training.

## Prerequisites

- Salesforce Data Cloud license/subscription
- Salesforce CLI (sf) installed and configured
- Access to Salesforce org with Data Cloud enabled
- Python 3.9+ (for local data transformations)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Data Sources                          │
│  ┌──────────────┐ ┌──────────┐ ┌──────┐ ┌──────────┐   │
│  │ Salesforce   │ │ External │ │ CSV  │ │ Marketo/ │   │
│  │ Production   │ │ APIs     │ │Files │ │   SAP    │   │
│  └──────────────┘ └──────────┘ └──────┘ └──────────┘   │
└────────────────────────┬─────────────────────────────────┘
                         │
                    ┌────▼────┐
                    │Connectors│
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐     ┌────▼────┐     ┌───▼────┐
    │Validate │     │Transform │     │Normalize
    │         │     │          │     │        │
    └────┬────┘     └────┬────┘     └───┬────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                 ┌───────▼────────┐
                 │  Unified Catalog
                 │   (Data Cloud)
                 └───────┬────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐     ┌────▼────┐     ┌───▼────┐
    │ ML Train │     │Analytics │    │ Reports
    │Datasets  │     │Dashboards│    │        │
    └──────────┘     └──────────┘    └────────┘
```

## Step 1: Enable Data Cloud in Your Org

1. Log into Salesforce as an admin
2. Navigate to **Setup** → **Platform** → **Data Cloud** → **Setup Wizard**
3. Follow the wizard to enable Data Cloud
4. Configure your workspace and retention settings

## Step 2: Configure API Access

### Create Connected App for Data Cloud API

1. In Salesforce Setup, go to **Apps** → **App Manager**
2. Click **New Connected App**
3. Fill in the details:
   - **Connected App Name**: Agentforce Vibes Data Cloud
   - **API Name**: agentforce_vibes_datacloud
   - Enable OAuth Settings
   - Add scopes: `api`, `data_cloud_api`
4. Save and get your **Client ID** and **Client Secret**

### Create a Consumer Key

1. Go to your Consumer app details
2. Click **Manage** 
3. Note the **Consumer Key** and generate a **Consumer Secret**

## Step 3: Configure Environment Variables

Create a `.env` file in your project:

```bash
# Salesforce Configuration
SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com
SALESFORCE_CLIENT_ID=your_client_id_here
SALESFORCE_CLIENT_SECRET=your_client_secret_here
SALESFORCE_USERNAME=admin@example.com

# Data Cloud Configuration
DATACLOUD_WORKSPACE_ID=your_workspace_id
DATACLOUD_API_KEY=your_api_key_here
DATACLOUD_WORKSPACE_ENDPOINT=https://your-instance.salesforce.com/api/v1/dc

# ML Configuration
ML_MODEL_TRAINING_SPLIT=0.8
ML_FEATURE_AUTO_GENERATION=true
ML_RETENTION_DAYS=730
```

## Step 4: Set Up Unified Catalog

### Understanding the Catalog Structure

The unified catalog (`schemas/unified_catalog.json`) defines:

- **Entities**: Core objects (Account, Contact, Opportunity, Policy)
- **Fields**: Individual data attributes with types and mappings
- **Relationships**: How entities connect
- **Data Sources**: Where data comes from
- **ML Configuration**: Training data settings

### Core Entities

#### Account
- **Source**: Salesforce
- **Key Fields**: Account ID, Name, Industry, Annual Revenue, Employees
- **ML Use**: Company-level classification and segmentation

#### Contact
- **Source**: Salesforce
- **Key Fields**: Contact ID, Email, Phone, Title, Company
- **Relationships**: Links to Account
- **ML Use**: Person-level profiles and engagement scoring

#### Opportunity
- **Source**: Salesforce
- **Key Fields**: Opportunity ID, Amount, Stage, Close Date, Probability
- **Relationships**: Links to Account
- **ML Use**: Deal sizing and win probability prediction

#### Policy
- **Source**: External APIs
- **Key Fields**: Policy ID, Type, Premium, Status
- **Relationships**: Links to Account
- **ML Use**: Customer lifetime value and cross-sell modeling

## Step 5: Create Data Connectors

### Salesforce Connector

```python
from connectors.salesforce_connector import SalesforceDataCloudConnector

connector = SalesforceDataCloudConnector(
    instance_url="https://your-instance.salesforce.com",
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Authenticate
if connector.authenticate():
    # Sync entities
    result = connector.sync_all_entities(catalog_config)
    print(result)
```

### External API Connector

For external data sources (Marketo, SAP, policies API), create custom connectors:

```python
class ExternalAPIConnector:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
    
    def fetch_data(self, resource: str) -> List[Dict]:
        # Implement API calls
        pass
```

## Step 6: Data Transformation and Validation

### Transform Data

```python
from transformations.data_pipeline import DataTransformer

transformer = DataTransformer(catalog_config)

# Normalize and validate
normalized = transformer.normalize_data(raw_records)

# Create ML-ready features
dataset = transformer.prepare_ml_dataset("Account", normalized)
```

### Validate Data Quality

```python
from transformations.data_pipeline import DataValidator

validator = DataValidator(catalog_config)

# Validate individual records
is_valid, errors = validator.validate_record("Account", account_record)
```

## Step 7: Create ML Training Datasets

### Create Training Dataset

```python
from transformations.ml_training import MLTrainingDatasetManager

ml_manager = MLTrainingDatasetManager(workspace_id="default")

# Create dataset with 80/20 train/test split
dataset = ml_manager.create_training_dataset(
    name="Account_ML_Training",
    entity_names=["Account", "Contact", "Opportunity"],
    features=feature_matrix,
    train_test_split=0.8
)

print(f"Dataset created: {dataset['dataset_id']}")
```

### Auto-Generate Features

```python
from transformations.ml_training import FeatureEngineer

engineer = FeatureEngineer(auto_create_features=True)

# Auto-generate statistical features
features = engineer.auto_generate_features(entity_data)
```

### Export Training Data

```python
# Export as CSV for ML frameworks
export_result = ml_manager.export_dataset(dataset_id, format="csv")
print(f"Download from: {export_result['file_path']}")

# Or export as Parquet for big data tools
export_result = ml_manager.export_dataset(dataset_id, format="parquet")
```

## Step 8: Run the Complete Pipeline

### Orchestrate Sync and ML

```python
from orchestrator import DataCloudOrchestrator

orchestrator = DataCloudOrchestrator()

# Initialize connectors
orchestrator.initialize_connectors(
    salesforce_config={...},
    datacloud_config={...}
)

# Run full pipeline
result = orchestrator.run_full_sync()

print("Pipeline completed!")
print(f"Sync Status: {result['stages']['sync']}")
print(f"ML Datasets: {result['stages']['ml_training']}")
```

### Run from Command Line

```bash
cd data-cloud
python orchestrator.py
```

## Step 9: Create Data Cloud Rules and Segments

In Salesforce Data Cloud, create rules to define unified identities:

1. **Setup Identity Resolution**:
   - Go to **Setup** → **Data Cloud** → **Settings** → **Identity Resolution**
   - Define match rules for contacts (email, phone, etc.)

2. **Create Unified Customer Profiles**:
   - Map fields from Account, Contact, Opportunity to unified profile
   - Configure relationship maps

3. **Create Segments**:
   - Go to **Data Cloud** → **Segments**
   - Create segments for ML model training (e.g., "High-Value Accounts")

## Step 10: Monitor and Maintain

### Check Sync Status

```bash
sf data cloud org sync --status
```

### View Data Quality Metrics

Monitor in Salesforce:
- Setup → Data Cloud → Workspaces → Your Workspace
- Check **Data Quality** dashboard

### Schedule Automatic Syncs

```bash
# Configure scheduled sync in sfdx-project.json
"dataCloud": {
  "sync": {
    "frequency": "hourly",
    "entities": ["Account", "Contact", "Opportunity", "Policy"]
  }
}
```

## Integration with Agentforce

Your agent can now access unified customer data:

```python
from data_cloud.connectors.salesforce_connector import DataCloudIngestor

# Get customer 360
unified_identity = ingestor.create_unified_identity(contact_data, account_data)

# Use in agent
agent.process_message(
    message="Show me this customer's opportunities",
    customer_data=unified_identity
)
```

## Troubleshooting

### Issue: Authentication Failed
- Verify Consumer Key and Secret
- Check OAuth scopes include `data_cloud_api`
- Ensure IP is whitelisted

### Issue: Sync Errors
- Check field mappings in catalog schema
- Verify source data quality
- Review logs: `sf project deploy log`

### Issue: ML Dataset Too Small
- Increase data retention period in `ml_training_config`
- Add more data sources
- Reduce train/test split (if needed)

## Best Practices

1. **Data Quality**: Always validate before ingestion
2. **Security**: Encrypt credentials, use IP whitelisting
3. **Performance**: Batch ingestion for large datasets
4. **Monitoring**: Track sync errors and data quality metrics
5. **Versioning**: Version catalog schema changes
6. **Governance**: Document data lineage and transformations

## Next Steps

1. Complete the setup above
2. Run your first sync: `python orchestrator.py`
3. Create ML training dataset
4. Export data for model training
5. Monitor data quality in Data Cloud dashboard
6. Integrate with your Agentforce agent

## Support

For issues or questions:
- Review Salesforce Data Cloud docs: https://help.salesforce.com/
- Check data validation logs in `data-cloud/logs/`
- Contact your Salesforce admin
