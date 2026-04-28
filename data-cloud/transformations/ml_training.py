"""
ML Training Module

Prepare and manage ML training datasets from unified catalog
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLTrainingDatasetManager:
    """Manage ML training datasets from Data Cloud"""
    
    def __init__(self, workspace_id: str, retention_days: int = 730):
        """Initialize ML training manager"""
        self.workspace_id = workspace_id
        self.retention_days = retention_days
        self.datasets = {}
    
    def create_training_dataset(self, name: str, entity_names: List[str], 
                               features: Dict[str, List[Any]], 
                               train_test_split: float = 0.8) -> Dict[str, Any]:
        """Create a new ML training dataset"""
        logger.info(f"Creating training dataset: {name}")
        
        dataset_id = f"ds_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Split data into train and test sets
        total_samples = len(list(features.values())[0]) if features else 0
        split_index = int(total_samples * train_test_split)
        
        training_features = {k: v[:split_index] for k, v in features.items()}
        test_features = {k: v[split_index:] for k, v in features.items()}
        
        dataset = {
            "dataset_id": dataset_id,
            "name": name,
            "entities": entity_names,
            "created_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=self.retention_days)).isoformat(),
            "status": "created",
            "statistics": {
                "total_samples": total_samples,
                "training_samples": split_index,
                "test_samples": total_samples - split_index,
                "feature_count": len(features),
                "features": list(features.keys())
            },
            "train_test_split": {
                "ratio": train_test_split,
                "training_features": training_features,
                "test_features": test_features
            }
        }
        
        self.datasets[dataset_id] = dataset
        logger.info(f"Dataset created: {dataset_id}")
        
        return dataset
    
    def export_dataset(self, dataset_id: str, format: str = "csv") -> Dict[str, Any]:
        """Export dataset in specified format"""
        if dataset_id not in self.datasets:
            raise ValueError(f"Dataset not found: {dataset_id}")
        
        dataset = self.datasets[dataset_id]
        
        export_config = {
            "dataset_id": dataset_id,
            "format": format,
            "exported_date": datetime.now().isoformat(),
            "status": "ready_for_download"
        }
        
        if format == "csv":
            export_config["file_path"] = f"data-cloud/exports/{dataset_id}.csv"
        elif format == "parquet":
            export_config["file_path"] = f"data-cloud/exports/{dataset_id}.parquet"
        elif format == "json":
            export_config["file_path"] = f"data-cloud/exports/{dataset_id}.json"
        
        logger.info(f"Dataset exported: {dataset_id} as {format}")
        
        return export_config
    
    def get_dataset_statistics(self, dataset_id: str) -> Dict[str, Any]:
        """Get statistics for a dataset"""
        if dataset_id not in self.datasets:
            raise ValueError(f"Dataset not found: {dataset_id}")
        
        dataset = self.datasets[dataset_id]
        
        return {
            "dataset_id": dataset_id,
            "name": dataset["name"],
            "statistics": dataset["statistics"],
            "status": dataset["status"]
        }
    
    def list_datasets(self) -> List[Dict[str, Any]]:
        """List all training datasets"""
        return [
            {
                "dataset_id": ds["dataset_id"],
                "name": ds["name"],
                "created_date": ds["created_date"],
                "status": ds["status"],
                "sample_count": ds["statistics"]["total_samples"]
            }
            for ds in self.datasets.values()
        ]


class FeatureEngineer:
    """Create and manage features for ML models"""
    
    def __init__(self, auto_create_features: bool = True):
        """Initialize feature engineer"""
        self.auto_create_features = auto_create_features
        self.features = {}
    
    def create_feature(self, feature_name: str, feature_type: str, 
                      definition: str, source_entities: List[str]) -> Dict[str, Any]:
        """Create a new feature"""
        logger.info(f"Creating feature: {feature_name}")
        
        feature = {
            "name": feature_name,
            "type": feature_type,
            "definition": definition,
            "source_entities": source_entities,
            "created_date": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        self.features[feature_name] = feature
        return feature
    
    def auto_generate_features(self, entity_data: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Automatically generate features from entity data"""
        if not self.auto_create_features:
            return []
        
        generated_features = []
        
        for field_name in entity_data.keys():
            # Generate statistics features
            values = entity_data[field_name]
            
            if isinstance(values[0], (int, float)):
                features = [
                    {"name": f"{field_name}_mean", "type": "numeric"},
                    {"name": f"{field_name}_std", "type": "numeric"},
                    {"name": f"{field_name}_min", "type": "numeric"},
                    {"name": f"{field_name}_max", "type": "numeric"}
                ]
                generated_features.extend(features)
            elif isinstance(values[0], str):
                features = [
                    {"name": f"{field_name}_length", "type": "numeric"},
                    {"name": f"{field_name}_is_null", "type": "boolean"}
                ]
                generated_features.extend(features)
        
        logger.info(f"Auto-generated {len(generated_features)} features")
        return generated_features
    
    def list_features(self) -> List[Dict[str, Any]]:
        """List all features"""
        return list(self.features.values())
