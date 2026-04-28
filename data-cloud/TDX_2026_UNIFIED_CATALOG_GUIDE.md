# Salesforce Data Cloud Unified Catalog - TDX 2026 Guide

## Overview

The **Unified Catalog** is a centralized interface in Salesforce Data Cloud that provides a comprehensive view of all your data assets, schemas, and metadata across connected systems. This feature was highlighted at TrailblazerDX 2026 as a key capability for data governance and discovery.

## What is the Unified Catalog?

The Unified Catalog serves as a single source of truth for:

- **Data Model Objects (DMOs)**: All entities in your data model
- **Data Sources**: Connected systems (Salesforce, external APIs, data lakes)
- **Data Lineage**: How data flows between systems
- **Schemas**: Field definitions, data types, relationships
- **Metadata**: Business context, descriptions, tags
- **Data Quality Metrics**: Completeness, accuracy, freshness

## Accessing the Unified Catalog

### Method 1: Through Data Cloud App

1. **Open Data Cloud**:
   - Click the App Launcher (waffle icon)
   - Search for "Data Cloud"
   - Click to open the Data Cloud app

2. **Navigate to Unified Catalog**:
   - In the left navigation panel, click **Unified Catalog**
   - You'll see a dashboard view of all catalog entities

### Method 2: Direct URL

Navigate directly to:
```
https://[your-org].lightning.force.com/lightning/app/c__DataCloud
```

Then select **Unified Catalog** from the navigation menu.

### Method 3: Setup Access

For administrative tasks:
```
Setup → Data Cloud → Unified Catalog
```

## Key Features (TDX 2026 Highlights)

### 1. **Catalog Dashboard**
- **Entity Count**: Total number of DMOs
- **Source Systems**: Connected data sources
- **Data Volume**: Records per entity
- **Quality Score**: Overall data health

### 2. **Entity Browser**
Browse all data entities with:
- **Search & Filter**: Find entities by name, source, or tag
- **Visual Lineage**: See data flow diagrams
- **Schema View**: Inspect fields and relationships
- **Sample Data**: Preview actual records

### 3. **Data Lineage Graph**
Interactive visualization showing:
- Source systems → Data Streams → DMOs
- Transformations and mappings
- Impact analysis (upstream/downstream)

### 4. **Metadata Management**
For each entity, manage:
- **Business Names**: User-friendly labels
- **Descriptions**: What the data represents
- **Tags**: Categories and classifications
- **Ownership**: Data stewards and owners
- **Sensitivity**: PII/PHI classification

### 5. **Data Quality Insights**
Monitor health metrics:
- **Completeness**: % of null values
- **Accuracy**: Validation rule compliance
- **Freshness**: Last update timestamp
- **Consistency**: Cross-entity checks

### 6. **Search & Discovery**
Powerful search capabilities:
- **Global Search**: Find any entity or field
- **Natural Language**: "Show me customer data"
- **Faceted Filters**: By source, type, quality
- **Saved Searches**: Bookmark common queries

## Setting Up the Unified Catalog

### Prerequisites

1. **Data Cloud License**: Enterprise or Unlimited edition
2. **API Version**: v66.0 or higher
3. **Permissions**: Data Cloud Admin or equivalent

### Step 1: Enable Data Cloud

```bash
# Via Salesforce CLI
sf org open --target-org YOUR_ORG --path /lightning/setup/DataCloudSetup/home
```

Follow the setup wizard to:
- Enable Data Cloud
- Configure workspace
- Set data retention policies

### Step 2: Assign Permissions

Users need the following permissions:
- **Data Cloud Integration User**
- **View Data Cloud Metadata**
- **Manage Data Cloud Metadata** (for admins)

Use the included permission set:
```bash
sf project deploy start --source-dir force-app/main/default/permissionsets
sf org assign permset --name "Data_Cloud_Catalog_Access" --target-org YOUR_ORG
```

### Step 3: Connect Data Sources

1. Go to **Data Cloud** → **Data Sources**
2. Click **New Data Source**
3. Choose your source type:
   - Salesforce CRM
   - Marketing Cloud
   - External APIs
   - Data Lakes (S3, Azure, GCS)
   - Files (CSV, JSON, Parquet)

### Step 4: Create Data Model Objects

Define your entities in the catalog:

1. **Via UI**:
   - Data Cloud → Data Model → New Data Model Object
   - Define fields, types, and relationships

2. **Via Python** (using this project):
   ```bash
   cd data-cloud
   python orchestrator.py
   ```

3. **Via API**:
   ```bash
   sf data create record --sobject DataModelObject --values "Name='Customer' Type='Profile'"
   ```

### Step 5: Set Up Data Streams

Create data streams to populate the catalog:

1. Data Cloud → Data Streams → New Data Stream
2. Select source and target DMO
3. Map fields
4. Set refresh schedule
5. Activate the stream

## Using the Unified Catalog

### Browsing Entities

1. **Card View**: Visual grid of all entities
2. **List View**: Table with sortable columns
3. **Graph View**: Interactive lineage diagram

### Viewing Entity Details

Click any entity to see:
- **Overview**: Description, owner, tags
- **Schema**: All fields with types
- **Relationships**: Connected entities
- **Lineage**: Data flow visualization
- **Quality**: Health metrics and issues
- **Activity**: Recent changes and updates

### Searching the Catalog

**Basic Search**:
```
Customer
```

**Field Search**:
```
fields:email
```

**Tag Search**:
```
tag:pii
```

**Advanced Search**:
```
type:profile AND source:salesforce AND quality:>90
```

### Creating Custom Views

1. Build a search query
2. Apply filters (source, type, quality)
3. Click **Save View**
4. Name your view (e.g., "High-Quality Customer Data")
5. Share with team or keep private

## Data Governance with Unified Catalog

### Data Classification

Tag entities with:
- **Sensitivity**: Public, Internal, Confidential, Restricted
- **Compliance**: GDPR, CCPA, HIPAA
- **Category**: Customer, Product, Transaction, etc.

### Access Control

Set who can:
- **View**: See entity in catalog
- **Read Data**: Query actual records
- **Modify**: Change schema or metadata
- **Delete**: Remove entity

### Data Lineage Tracking

Understand data flow:
- **Source Systems**: Where data originates
- **Transformations**: How data is modified
- **Destinations**: Where data is consumed
- **Impact Analysis**: What breaks if source changes

### Quality Monitoring

Set up alerts for:
- Data freshness thresholds
- Quality score drops
- Schema changes
- Volume anomalies

## Integration with Your Project

Your project includes tools to work with the Unified Catalog programmatically:

### Python SDK

```python
from connectors.salesforce_connector import SalesforceDataCloudConnector

# Connect to Data Cloud
connector = SalesforceDataCloudConnector(
    instance_url="https://your-org.salesforce.com",
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Authenticate
connector.authenticate()

# List catalog entities
entities = connector.list_catalog_entities()
for entity in entities:
    print(f"{entity['name']}: {entity['record_count']} records")

# Get entity schema
schema = connector.get_entity_schema("Account")
print(f"Account has {len(schema['fields'])} fields")

# Query entity data
data = connector.query_entity("Account", limit=100)
```

### Orchestration Script

The project includes an orchestration pipeline:

```bash
cd data-cloud
python orchestrator.py
```

This will:
1. Load the unified catalog schema (`schemas/unified_catalog.json`)
2. Authenticate with Salesforce
3. Create/update DMOs
4. Sync data from sources
5. Validate data quality
6. Generate ML training datasets

### REST API

Direct API calls:

```bash
# List entities
curl "https://your-org.salesforce.com/services/data/v66.0/datacloud/catalog/entities" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get entity details
curl "https://your-org.salesforce.com/services/data/v66.0/datacloud/catalog/entities/Account__dlm" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Query entity data
curl "https://your-org.salesforce.com/services/data/v66.0/datacloud/query" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT * FROM Account__dlm LIMIT 10"}'
```

## Best Practices

### 1. Naming Conventions
- Use clear, descriptive names
- Follow consistent patterns (e.g., `Customer_Profile`, `Product_Catalog`)
- Avoid abbreviations unless standard

### 2. Metadata Management
- Add business descriptions to all entities
- Tag sensitive data appropriately
- Assign data owners and stewards
- Document data lineage

### 3. Data Quality
- Set quality rules for each entity
- Monitor quality dashboards regularly
- Address quality issues promptly
- Automate quality checks

### 4. Access Control
- Apply principle of least privilege
- Review permissions quarterly
- Audit access logs
- Use role-based access

### 5. Documentation
- Keep README files for each data source
- Document transformation logic
- Maintain change logs
- Create user guides

## TDX 2026 Demo Scenarios

### Scenario 1: Customer 360 Discovery

**Task**: Find all data related to customers across systems

1. Open Unified Catalog
2. Search: `tag:customer`
3. View: Graph view to see relationships
4. Result: Visual map of Customer, Contact, Account, Orders, Cases

### Scenario 2: Data Quality Analysis

**Task**: Identify data quality issues

1. Go to Unified Catalog Dashboard
2. Click "Data Quality" tab
3. Sort by quality score (lowest first)
4. Drill into problematic entities
5. View specific quality issues
6. Create remediation tasks

### Scenario 3: Impact Analysis

**Task**: Understand impact of changing a source system

1. Navigate to source system in catalog
2. Click "Lineage" tab
3. Enable "Downstream Impact" view
4. See all affected DMOs, segments, and analytics
5. Export impact report

### Scenario 4: Compliance Audit

**Task**: Identify all PII data for GDPR audit

1. Search catalog: `tag:pii OR tag:gdpr`
2. Review all matching entities
3. Check access controls
4. Verify retention policies
5. Generate compliance report

## Troubleshooting

### Issue: Unified Catalog Menu Not Visible

**Solutions**:
1. Verify Data Cloud is enabled (Setup → Data Cloud)
2. Check user has Data Cloud permissions
3. Refresh browser or clear cache
4. Try direct URL: `/lightning/app/c__DataCloud`

### Issue: Entities Not Appearing

**Solutions**:
1. Check data streams are active
2. Verify data has been ingested
3. Check entity visibility settings
4. Refresh catalog cache

### Issue: Permission Errors

**Solutions**:
1. Assign Data Cloud permission sets
2. Check object-level security
3. Verify field-level security
4. Contact Salesforce admin

### Issue: Slow Performance

**Solutions**:
1. Reduce number of entities displayed
2. Use filters to narrow results
3. Clear browser cache
4. Check Data Cloud status

## Advanced Features

### Custom Catalog Extensions

Create custom metadata types:

```xml
<CustomMetadata xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Data Catalog Extension</label>
    <pluralLabel>Data Catalog Extensions</pluralLabel>
    <visibility>Public</visibility>
    <fields>
        <field>
            <label>Business Owner</label>
            <type>Text</type>
        </field>
        <field>
            <label>Cost Center</label>
            <type>Text</type>
        </field>
    </fields>
</CustomMetadata>
```

### Catalog API Automation

Automate catalog tasks:

```python
# Auto-tag entities based on naming patterns
def auto_tag_entities(connector):
    entities = connector.list_catalog_entities()
    for entity in entities:
        if 'customer' in entity['name'].lower():
            connector.tag_entity(entity['id'], ['customer', 'pii'])
        elif 'product' in entity['name'].lower():
            connector.tag_entity(entity['id'], ['product', 'inventory'])

# Monitor data quality
def monitor_quality(connector):
    entities = connector.list_catalog_entities()
    alerts = []
    for entity in entities:
        quality = connector.get_entity_quality(entity['id'])
        if quality['score'] < 80:
            alerts.append({
                'entity': entity['name'],
                'score': quality['score'],
                'issues': quality['issues']
            })
    return alerts
```

## Resources

- **Salesforce Help**: [Data Cloud Unified Catalog](https://help.salesforce.com/datacloud)
- **Trailhead**: [Data Cloud Basics](https://trailhead.salesforce.com/datacloud)
- **API Reference**: [Data Cloud REST API](https://developer.salesforce.com/docs/atlas.en-us.datacloud_api.meta/)
- **Community**: [Data Cloud Trailblazer Community](https://trailhead.salesforce.com/trailblazer-community)

## Summary

The Unified Catalog in Data Cloud provides:
- ✅ Centralized view of all data assets
- ✅ Data lineage and impact analysis
- ✅ Quality monitoring and governance
- ✅ Search and discovery capabilities
- ✅ Metadata management
- ✅ Compliance and security controls

This feature streamlines data management, improves data quality, and accelerates analytics and AI initiatives.

---

**Last Updated**: Based on TDX 2026 announcements
**Project Location**: `data-cloud/TDX_2026_UNIFIED_CATALOG_GUIDE.md`