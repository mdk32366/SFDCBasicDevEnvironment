"""
Tests for Data Cloud components
"""

import json
import pytest
from datetime import datetime

from connectors.salesforce_connector import SalesforceDataCloudConnector, DataCloudIngestor
from transformations.data_pipeline import DataValidator, DataTransformer
from transformations.ml_training import MLTrainingDatasetManager, FeatureEngineer


# Load test schema
def load_test_schema():
    with open("schemas/unified_catalog.json", "r") as f:
        return json.load(f)


# Salesforce Connector Tests
class TestSalesforceConnector:
    @pytest.fixture
    def connector(self):
        return SalesforceDataCloudConnector(
            instance_url="https://test.salesforce.com",
            client_id="test_client",
            client_secret="test_secret"
        )
    
    def test_connector_initialization(self, connector):
        assert connector.instance_url == "https://test.salesforce.com"
        assert connector.access_token is None
    
    def test_authentication(self, connector):
        result = connector.authenticate()
        assert result is True
        assert connector.access_token is not None


# Data Validation Tests
class TestDataValidator:
    @pytest.fixture
    def validator(self):
        schema = load_test_schema()
        return DataValidator(schema)
    
    def test_valid_record(self, validator):
        account = {
            "account_id": "001XX000003DHP",
            "account_name": "Test Corp",
            "industry": "Technology",
            "annual_revenue": 1000000,
            "created_date": "2024-01-01"
        }
        is_valid, errors = validator.validate_record("Account", account)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_invalid_record_missing_key(self, validator):
        account = {
            "account_name": "Test Corp",
            "industry": "Technology"
        }
        is_valid, errors = validator.validate_record("Account", account)
        assert is_valid is False
        assert any("account_id" in err for err in errors)


# Data Transformation Tests
class TestDataTransformer:
    @pytest.fixture
    def transformer(self):
        schema = load_test_schema()
        return DataTransformer(schema)
    
    def test_normalize_data(self, transformer):
        raw_records = [
            {
                "account_name": "  Test Corp  ",
                "annual_revenue": "1000000"
            }
        ]
        normalized = transformer.normalize_data(raw_records)
        assert normalized[0]["account_name"] == "Test Corp"
        assert normalized[0]["annual_revenue"] == 1000000.0
    
    def test_create_feature_matrix(self, transformer):
        records = [
            {"id": "1", "value": 100},
            {"id": "2", "value": 200}
        ]
        features = transformer.create_feature_matrix(records)
        assert features["id"] == ["1", "2"]
        assert features["value"] == [100, 200]


# ML Training Tests
class TestMLTrainingDatasetManager:
    @pytest.fixture
    def ml_manager(self):
        return MLTrainingDatasetManager(workspace_id="test_workspace")
    
    def test_create_training_dataset(self, ml_manager):
        features = {
            "account_id": ["1", "2", "3", "4", "5"],
            "revenue": [100, 200, 300, 400, 500]
        }
        
        dataset = ml_manager.create_training_dataset(
            name="Test Dataset",
            entity_names=["Account"],
            features=features,
            train_test_split=0.8
        )
        
        assert dataset["name"] == "Test Dataset"
        assert dataset["statistics"]["total_samples"] == 5
        assert dataset["statistics"]["training_samples"] == 4
        assert dataset["statistics"]["test_samples"] == 1
    
    def test_export_dataset(self, ml_manager):
        features = {
            "account_id": ["1", "2", "3"],
            "revenue": [100, 200, 300]
        }
        
        dataset = ml_manager.create_training_dataset(
            name="Test",
            entity_names=["Account"],
            features=features
        )
        
        export = ml_manager.export_dataset(dataset["dataset_id"], format="csv")
        assert export["format"] == "csv"
        assert "csv" in export["file_path"]


# Feature Engineering Tests
class TestFeatureEngineer:
    @pytest.fixture
    def engineer(self):
        return FeatureEngineer(auto_create_features=True)
    
    def test_auto_generate_numeric_features(self, engineer):
        data = {
            "revenue": [100, 200, 300],
            "employees": [10, 20, 30]
        }
        
        features = engineer.auto_generate_features(data)
        feature_names = [f["name"] for f in features]
        
        assert "revenue_mean" in feature_names
        assert "employees_min" in feature_names
    
    def test_create_custom_feature(self, engineer):
        feature = engineer.create_feature(
            feature_name="high_value_account",
            feature_type="boolean",
            definition="revenue > 1000000",
            source_entities=["Account"]
        )
        
        assert feature["name"] == "high_value_account"
        assert feature["type"] == "boolean"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
