"""
Data Cloud Transformation Pipeline

Handles data validation, cleaning, and transformation for ML training
"""

import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """Validate data quality and schema compliance"""
    
    def __init__(self, schema: Dict[str, Any]):
        """Initialize validator with schema"""
        self.schema = schema
        self.validation_rules = self._build_rules()
        
    def _build_rules(self) -> Dict[str, Any]:
        """Build validation rules from schema"""
        rules = {}
        for entity in self.schema.get("entities", []):
            entity_name = entity["entity_name"]
            rules[entity_name] = {
                "fields": {f["name"]: f for f in entity["fields"]},
                "required_fields": [f["name"] for f in entity["fields"] if f.get("is_key")]
            }
        return rules
    
    def validate_record(self, entity_name: str, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a single record against schema"""
        errors = []
        
        if entity_name not in self.validation_rules:
            errors.append(f"Unknown entity: {entity_name}")
            return False, errors
        
        rules = self.validation_rules[entity_name]
        
        # Check required fields
        for required_field in rules["required_fields"]:
            if required_field not in record or record[required_field] is None:
                errors.append(f"Missing required field: {required_field}")
        
        # Validate field types
        for field_name, field_value in record.items():
            if field_name in rules["fields"]:
                field_schema = rules["fields"][field_name]
                if not self._validate_type(field_value, field_schema.get("type")):
                    errors.append(f"Invalid type for {field_name}: expected {field_schema.get('type')}")
        
        return len(errors) == 0, errors
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value matches expected type"""
        if value is None:
            return True
        
        type_map = {
            "string": str,
            "integer": int,
            "decimal": (int, float),
            "timestamp": str,
            "date": str,
            "boolean": bool
        }
        
        expected = type_map.get(expected_type)
        if expected is None:
            return True
        
        return isinstance(value, expected)


class DataTransformer:
    """Transform raw data for ML training"""
    
    def __init__(self, catalog_config: Dict[str, Any]):
        """Initialize transformer"""
        self.catalog_config = catalog_config
        self.validator = DataValidator(catalog_config)
    
    def normalize_data(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize and clean data"""
        normalized = []
        
        for record in records:
            normalized_record = {}
            
            for key, value in record.items():
                # Convert null values
                if value is None or value == "":
                    normalized_record[key] = None
                # Normalize strings
                elif isinstance(value, str):
                    normalized_record[key] = value.strip()
                # Normalize numbers
                elif isinstance(value, (int, float)):
                    normalized_record[key] = float(value)
                else:
                    normalized_record[key] = value
            
            normalized.append(normalized_record)
        
        return normalized
    
    def join_related_entities(self, primary_records: List[Dict[str, Any]], 
                             related_records: List[Dict[str, Any]], 
                             join_key: str) -> List[Dict[str, Any]]:
        """Join related entities for enriched ML features"""
        # Create lookup map for related records
        lookup = {}
        for record in related_records:
            key = record.get(join_key)
            if key:
                if key not in lookup:
                    lookup[key] = []
                lookup[key].append(record)
        
        # Join records
        joined = []
        for record in primary_records:
            key = record.get(join_key)
            if key in lookup:
                for related in lookup[key]:
                    merged = {**record, **{f"related_{k}": v for k, v in related.items()}}
                    joined.append(merged)
            else:
                joined.append(record)
        
        return joined
    
    def create_feature_matrix(self, records: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """Create feature matrix for ML training"""
        if not records:
            return {}
        
        # Initialize feature columns
        features = {key: [] for key in records[0].keys()}
        
        # Populate features
        for record in records:
            for key, value in record.items():
                features[key].append(value)
        
        return features
    
    def prepare_ml_dataset(self, entity_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare complete ML dataset"""
        logger.info(f"Preparing ML dataset for {entity_name}")
        
        # Normalize data
        normalized = self.normalize_data(records)
        
        # Validate data
        valid_records = []
        validation_errors = 0
        for record in normalized:
            is_valid, errors = self.validator.validate_record(entity_name, record)
            if is_valid:
                valid_records.append(record)
            else:
                validation_errors += 1
                logger.warning(f"Validation failed: {errors}")
        
        # Create feature matrix
        features = self.create_feature_matrix(valid_records)
        
        return {
            "entity": entity_name,
            "total_records": len(records),
            "valid_records": len(valid_records),
            "validation_errors": validation_errors,
            "feature_count": len(features),
            "features": features,
            "prepared_date": datetime.now().isoformat()
        }
