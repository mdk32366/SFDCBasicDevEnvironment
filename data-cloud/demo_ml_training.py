"""
Complete Demo: Create ML Training Dataset and Export

Demonstrates the full workflow:
1. Create ML training dataset with real Salesforce-like data
2. Export in CSV format for scikit-learn
3. Export in Parquet format for big data tools
4. Generate feature statistics
"""

import sys
import json
sys.path.insert(0, '/transformations')

from transformations.ml_training import MLTrainingDatasetManager, FeatureEngineer
from transformations.data_pipeline import DataTransformer
from connectors.salesforce_connector import DataCloudIngestor

def main():
    print("\n" + "="*70)
    print("AGENTFORCE VIBES - DATA CLOUD ML TRAINING DATASET DEMO")
    print("="*70)
    
    # Step 1: Initialize ML Manager
    print("\n[1] Initializing ML Training Dataset Manager...")
    ml_manager = MLTrainingDatasetManager(workspace_id="default", retention_days=730)
    print("    ✓ ML Manager initialized (2-year retention)")
    
    # Step 2: Load unified catalog
    print("\n[2] Loading Unified Catalog...")
    with open('schemas/unified_catalog.json', 'r') as f:
        catalog = json.load(f)
    print(f"    ✓ Loaded catalog with {len(catalog['entities'])} entities")
    for entity in catalog['entities']:
        print(f"      - {entity['entity_name']} ({entity['source_system']})")
    
    # Step 3: Create realistic sample data
    print("\n[3] Creating Realistic Sample Data...")
    sample_features = {
        "account_id": ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"],
        "account_name": [
            "Acme Corp", "TechStart Inc", "Global Industries", 
            "CloudFirst Systems", "DataSoft LLC", "SecureBank", 
            "MedTech Solutions", "GreenEnergy Co", "FinTech Hub", "RetailPro"
        ],
        "industry": ["Tech", "Tech", "Manufacturing", "Tech", "Tech", "Finance", "Healthcare", "Energy", "Finance", "Retail"],
        "annual_revenue": [1000000, 2500000, 5000000, 1500000, 3000000, 8000000, 2000000, 4000000, 6000000, 1200000],
        "employees": [50, 150, 500, 75, 200, 400, 100, 250, 350, 60],
        "billing_country": ["USA", "USA", "Canada", "USA", "UK", "USA", "Germany", "USA", "Singapore", "USA"],
        "contact_count": [5, 15, 45, 10, 25, 60, 20, 40, 55, 8],
        "opportunity_count": [3, 8, 20, 5, 12, 35, 15, 25, 40, 4],
        "avg_deal_size": [150000, 200000, 300000, 175000, 250000, 500000, 180000, 350000, 450000, 95000]
    }
    print(f"    ✓ Created {len(sample_features['account_id'])} sample account records")
    print(f"    ✓ {len(sample_features)} features per record")
    
    # Step 4: Create ML Dataset
    print("\n[4] Creating ML Training Dataset...")
    dataset = ml_manager.create_training_dataset(
        name="Account_ML_Training_20260428",
        entity_names=["Account", "Contact", "Opportunity"],
        features=sample_features,
        train_test_split=0.8
    )
    
    dataset_id = dataset["dataset_id"]
    stats = dataset["statistics"]
    
    print(f"    ✓ Dataset Created: {dataset_id}")
    print(f"    ✓ Total Samples: {stats['total_samples']}")
    print(f"    ✓ Training Samples (80%): {stats['training_samples']}")
    print(f"    ✓ Test Samples (20%): {stats['test_samples']}")
    print(f"    ✓ Features: {stats['feature_count']}")
    
    # Step 5: Export in Multiple Formats
    print("\n[5] Exporting ML Training Data...")
    
    formats = ["csv", "parquet", "json"]
    exports = {}
    
    for fmt in formats:
        export_result = ml_manager.export_dataset(dataset_id, format=fmt)
        exports[fmt] = export_result
        print(f"    ✓ {fmt.upper()}: {export_result['file_path']}")
    
    # Step 6: Feature Engineering
    print("\n[6] Auto-Generating ML Features...")
    feature_engineer = FeatureEngineer(auto_create_features=True)
    
    generated_features = feature_engineer.auto_generate_features(sample_features)
    print(f"    ✓ Auto-generated {len(generated_features)} statistical features")
    
    # Show feature examples
    print("\n    Generated Features (sample):")
    for i, feat in enumerate(generated_features[:5]):
        print(f"      - {feat['name']} ({feat['type']})")
    if len(generated_features) > 5:
        print(f"      ... and {len(generated_features) - 5} more")
    
    # Step 7: Dataset Statistics
    print("\n[7] Dataset Statistics Summary")
    dataset_stats = ml_manager.get_dataset_statistics(dataset_id)
    print(f"    Dataset: {dataset_stats['name']}")
    print(f"    Status: {dataset_stats['status']}")
    print("\n    Feature Breakdown:")
    for feature_name in list(sample_features.keys())[:5]:
        values = sample_features[feature_name]
        if isinstance(values[0], (int, float)):
            print(f"      - {feature_name}: min={min(values)}, max={max(values)}, avg={sum(values)/len(values):.0f}")
        else:
            print(f"      - {feature_name}: {len(set(values))} unique values")
    
    # Step 8: Unified Identity Creation
    print("\n[8] Creating Unified Customer Identities...")
    ingestor = DataCloudIngestor(workspace_id="default", api_key="demo")
    
    contact_data = {
        "contact_id": "00300000001",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@acmecorp.com",
        "phone": "+1-555-0100",
        "title": "VP Sales"
    }
    
    account_data = {
        "account_id": "001",
        "account_name": "Acme Corp",
        "industry": "Technology",
        "annual_revenue": 1000000
    }
    
    unified_identity = ingestor.create_unified_identity(contact_data, account_data)
    print(f"    ✓ Created Unified Identity: {unified_identity['unified_id']}")
    print(f"      Contact: {unified_identity['name']} ({unified_identity['email']})")
    print(f"      Company: {unified_identity['company']}")
    
    # Step 9: List All Datasets
    print("\n[9] Listing All Training Datasets")
    all_datasets = ml_manager.list_datasets()
    print(f"    ✓ Total Datasets: {len(all_datasets)}")
    for ds in all_datasets:
        print(f"      - {ds['name']}: {ds['sample_count']} samples ({ds['status']})")
    
    # Step 10: Final Summary
    print("\n" + "="*70)
    print("DEMO COMPLETE ✓")
    print("="*70)
    print("\nWorkflow Summary:")
    print(f"  1. ✓ Created ML training dataset: {dataset_id}")
    print(f"  2. ✓ Generated {stats['training_samples']} training samples")
    print(f"  3. ✓ Generated {stats['test_samples']} test samples")
    print(f"  4. ✓ Exported in 3 formats: {', '.join(formats)}")
    print(f"  5. ✓ Auto-generated {len(generated_features)} ML features")
    print(f"  6. ✓ Created unified customer identities")
    print("\nNext Steps:")
    print(f"  • Download exported data from:")
    for fmt in formats:
        print(f"    - {exports[fmt]['file_path']}")
    print(f"\n  • Use in ML frameworks:")
    print(f"    - TensorFlow/PyTorch: Use Parquet format")
    print(f"    - scikit-learn: Use CSV format")
    print(f"    - Big Data tools: Use Parquet format")
    print(f"\n  • Integrate with Agentforce agent:")
    print(f"    - Use unified identity context for customer interactions")
    print(f"    - Train models using exported datasets")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
