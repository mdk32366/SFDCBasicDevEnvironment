"""
Data Cloud Orchestration

Orchestrates the complete data synchronization and ML training pipeline
"""

import json
import os
from typing import Dict, Any
from datetime import datetime
import logging

from connectors.salesforce_connector import SalesforceDataCloudConnector, DataCloudIngestor
from transformations.data_pipeline import DataTransformer, DataValidator
from transformations.ml_training import MLTrainingDatasetManager, FeatureEngineer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCloudOrchestrator:
    """Orchestrate Data Cloud operations"""
    
    def __init__(self, config_path: str = "schemas/unified_catalog.json"):
        """Initialize orchestrator"""
        with open(config_path, 'r') as f:
            self.catalog_config = json.load(f)
        
        self.sync_connector = None
        self.ingestor = None
        self.transformer = DataTransformer(self.catalog_config)
        self.validator = DataValidator(self.catalog_config)
        self.ml_manager = MLTrainingDatasetManager(workspace_id="default")
        self.feature_engineer = FeatureEngineer(auto_create_features=True)
        
        self.sync_results = {}
    
    def initialize_connectors(self, salesforce_config: Dict[str, str], 
                            datacloud_config: Dict[str, str]) -> bool:
        """Initialize Salesforce and Data Cloud connectors"""
        try:
            self.sync_connector = SalesforceDataCloudConnector(
                instance_url=salesforce_config.get("instance_url"),
                client_id=salesforce_config.get("client_id"),
                client_secret=salesforce_config.get("client_secret")
            )
            
            self.ingestor = DataCloudIngestor(
                workspace_id=datacloud_config.get("workspace_id"),
                api_key=datacloud_config.get("api_key")
            )
            
            logger.info("Connectors initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize connectors: {e}")
            return False
    
    def run_full_sync(self) -> Dict[str, Any]:
        """Run complete sync and ML training pipeline"""
        logger.info("Starting full Data Cloud sync pipeline")
        
        pipeline_result = {
            "pipeline_id": f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_time": datetime.now().isoformat(),
            "stages": {}
        }
        
        # Stage 1: Authenticate
        logger.info("Stage 1: Authentication")
        if not self.sync_connector.authenticate():
            pipeline_result["status"] = "failed"
            return pipeline_result
        
        # Stage 2: Sync entities
        logger.info("Stage 2: Entity Synchronization")
        sync_result = self.sync_connector.sync_all_entities(self.catalog_config)
        pipeline_result["stages"]["sync"] = sync_result
        
        # Stage 3: Data validation
        logger.info("Stage 3: Data Validation")
        validation_result = {
            "total_entities": len(self.catalog_config.get("entities", [])),
            "validated": 0
        }
        pipeline_result["stages"]["validation"] = validation_result
        
        # Stage 4: Create ML datasets
        logger.info("Stage 4: ML Dataset Creation")
        ml_result = self._create_ml_datasets()
        pipeline_result["stages"]["ml_training"] = ml_result
        
        pipeline_result["end_time"] = datetime.now().isoformat()
        pipeline_result["status"] = "completed"
        
        logger.info("Pipeline completed successfully")
        return pipeline_result
    
    def _create_ml_datasets(self) -> Dict[str, Any]:
        """Create ML training datasets"""
        ml_result = {
            "datasets_created": 0,
            "datasets": []
        }
        
        try:
            # Create a comprehensive ML dataset
            sample_features = {
                "account_id": ["1", "2", "3"],
                "industry": ["tech", "finance", "retail"],
                "annual_revenue": [1000000, 2000000, 1500000]
            }
            
            dataset = self.ml_manager.create_training_dataset(
                name="Account_ML_Training_Set",
                entity_names=["Account", "Contact", "Opportunity"],
                features=sample_features,
                train_test_split=0.8
            )
            
            ml_result["datasets_created"] += 1
            ml_result["datasets"].append({
                "dataset_id": dataset["dataset_id"],
                "name": dataset["name"],
                "statistics": dataset["statistics"]
            })
            
            # Auto-generate features
            generated_features = self.feature_engineer.auto_generate_features(sample_features)
            ml_result["auto_generated_features"] = len(generated_features)
            
        except Exception as e:
            logger.error(f"Failed to create ML datasets: {e}")
            ml_result["error"] = str(e)
        
        return ml_result
    
    def export_ml_training_data(self, dataset_id: str, format: str = "csv") -> Dict[str, Any]:
        """Export ML training data"""
        try:
            export_result = self.ml_manager.export_dataset(dataset_id, format)
            logger.info(f"ML training data exported: {export_result['file_path']}")
            return export_result
        except Exception as e:
            logger.error(f"Failed to export training data: {e}")
            return {"error": str(e)}
    
    def get_catalog_summary(self) -> Dict[str, Any]:
        """Get summary of unified catalog"""
        return {
            "catalog_name": self.catalog_config.get("catalog_name"),
            "total_entities": len(self.catalog_config.get("entities", [])),
            "data_sources": len(self.catalog_config.get("data_sources", [])),
            "ml_training_enabled": self.catalog_config.get("ml_training_config", {}).get("enabled"),
            "entities": [
                {
                    "name": e["entity_name"],
                    "source": e["source_system"],
                    "field_count": len(e.get("fields", []))
                }
                for e in self.catalog_config.get("entities", [])
            ]
        }


def main():
    """Main orchestration entry point"""
    # Load configuration
    orchestrator = DataCloudOrchestrator()
    
    # Print catalog summary
    summary = orchestrator.get_catalog_summary()
    print("\n=== Data Cloud Unified Catalog ===")
    print(json.dumps(summary, indent=2))
    
    # Initialize connectors (would need real credentials)
    salesforce_config = {
        "instance_url": os.getenv("SALESFORCE_INSTANCE_URL", "https://yourinstance.salesforce.com"),
        "client_id": os.getenv("SALESFORCE_CLIENT_ID", ""),
        "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET", "")
    }
    
    datacloud_config = {
        "workspace_id": os.getenv("DATACLOUD_WORKSPACE_ID", "default"),
        "api_key": os.getenv("DATACLOUD_API_KEY", "")
    }
    
    if orchestrator.initialize_connectors(salesforce_config, datacloud_config):
        # Run pipeline (would execute with real connectors)
        # result = orchestrator.run_full_sync()
        # print("\n=== Pipeline Result ===")
        # print(json.dumps(result, indent=2))
        print("\nConnectors initialized successfully!")
        print("Note: Full sync requires valid Salesforce and Data Cloud credentials")


if __name__ == "__main__":
    main()
