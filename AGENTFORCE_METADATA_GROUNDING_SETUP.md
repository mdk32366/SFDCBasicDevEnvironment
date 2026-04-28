# Agentforce Metadata Grounding - Setup Guide

## What Is This?

**Agentforce Metadata Grounding** allows Agentforce to access and understand your Salesforce org's metadata, including:
- Custom objects and fields
- Flows and workflows
- Validation rules
- Apex classes and triggers
- Page layouts
- Permission sets
- And more...

This enables Agentforce to:
- ✅ Answer questions about your org configuration
- ✅ Generate flow diagrams
- ✅ Explain how objects are related
- ✅ Describe field dependencies
- ✅ Document your org setup
- ✅ Provide org-specific guidance

## How to Enable Metadata Grounding

### Step 1: Enable Einstein and Agentforce

1. **Go to Setup** → Search for "Einstein Setup"
2. Click **Einstein Setup**
3. Enable **Einstein** if not already enabled
4. Enable **Agentforce**

### Step 2: Enable Metadata Grounding

1. **Setup** → Search for "Agentforce"
2. Click **Agentforce Settings**
3. Look for **"Metadata Grounding"** or **"Org Context"**
4. Toggle **Enable Metadata Grounding** to ON
5. Click **Save**

### Step 3: Configure Metadata Access

You may need to specify what metadata Agentforce can access:

1. In **Agentforce Settings**:
   - **Metadata Types**: Select which types (Objects, Flows, Apex, etc.)
   - **Scope**: Choose All or Specific metadata
   - **Refresh**: Set how often metadata is synced

### Step 4: Grant Permissions

Ensure your user has:
- **View All Data** (or specific object permissions)
- **View Setup and Configuration**
- **Agentforce User** permission

### Step 5: Test It

Ask Agentforce questions like:
- "What custom objects exist in this org?"
- "Show me the fields on the Account object"
- "Explain the Lead conversion process"
- "Generate a diagram of the Opportunity flow"

## Accessing Metadata Grounding

### Via Agentforce Chat (Recommended)

1. Open **Agentforce** (in app launcher or Einstein icon)
2. Ask metadata questions:
   ```
   "What custom objects are in my org?"
   "Show me all flows related to Opportunity"
   "Diagram the Account object relationships"
   "What validation rules exist on Contact?"
   ```

### Via Einstein Copilot

If you have Einstein Copilot:
1. Click the **Einstein icon** in the header
2. Ask org-specific questions
3. Copilot uses metadata grounding automatically

### Via API (for advanced users)

```bash
# Query metadata via CLI
sf project retrieve start --metadata CustomObject:*
sf project retrieve start --metadata Flow:*
```

## Features Enabled by Metadata Grounding

### 1. Object Discovery
**Ask**: "What custom objects exist?"
**Agentforce Response**: Lists all custom objects with descriptions

### 2. Field Analysis
**Ask**: "Show me fields on the Account object"
**Agentforce Response**: Lists fields with types, labels, and properties

### 3. Relationship Mapping
**Ask**: "How are Account and Contact related?"
**Agentforce Response**: Explains lookup/master-detail relationships

### 4. Flow Visualization
**Ask**: "Show me the Lead conversion flow"
**Agentforce Response**: Generates flow diagram

### 5. Validation Rule Explanation
**Ask**: "What validation rules exist on Opportunity?"
**Agentforce Response**: Lists rules with formulas and error messages

### 6. Apex Code Understanding
**Ask**: "What triggers are on the Contact object?"
**Agentforce Response**: Lists triggers with descriptions

### 7. Permission Analysis
**Ask**: "What permissions does the Sales profile have?"
**Agentforce Response**: Details object and field permissions

## Configuration Options

### Metadata Types You Can Enable:

- ✅ **Custom Objects** - Objects, fields, relationships
- ✅ **Flows** - Screen flows, autolaunched, record-triggered
- ✅ **Validation Rules** - All validation logic
- ✅ **Apex** - Classes, triggers, test classes
- ✅ **Profiles & Permission Sets** - Security configuration
- ✅ **Page Layouts** - UI configuration
- ✅ **Lightning Pages** - FlexiPages and components
- ✅ **Reports & Dashboards** - Analytics configuration

### Scope Options:

**Option 1: All Metadata**
- Agentforce can access everything
- Best for admins and power users

**Option 2: Managed Package Only**
- Limits to specific packages
- Good for ISV developers

**Option 3: Custom Metadata Only**
- Only custom objects and configurations
- Good for security-conscious orgs

### Refresh Frequency:

- **Real-time**: Metadata synced immediately (recommended)
- **Hourly**: Synced every hour
- **Daily**: Synced once per day
- **Manual**: Sync on-demand

## Example Use Cases

### Use Case 1: Documentation Generation

**Ask Agentforce**:
```
"Generate documentation for all custom objects in my org"
```

**Result**: Complete object documentation with fields, relationships, and descriptions

### Use Case 2: Flow Diagram

**Ask Agentforce**:
```
"Create a flowchart for the Opportunity approval process"
```

**Result**: Visual diagram of the flow

### Use Case 3: Impact Analysis

**Ask Agentforce**:
```
"If I delete the 'Industry' field from Account, what will break?"
```

**Result**: Analysis of dependencies (flows, validation rules, Apex)

### Use Case 4: Best Practices

**Ask Agentforce**:
```
"Are there any validation rules on Opportunity that conflict?"
```

**Result**: Analysis of validation rule logic

### Use Case 5: Relationship Explorer

**Ask Agentforce**:
```
"Show me all objects related to Account"
```

**Result**: Relationship diagram

## Troubleshooting

### Issue: Agentforce Can't Access Metadata

**Solutions**:
1. Check that Metadata Grounding is enabled
2. Verify user has "View Setup and Configuration"
3. Check metadata scope settings
4. Refresh metadata cache

### Issue: Incomplete Metadata

**Solutions**:
1. Trigger manual metadata sync
2. Check scope configuration
3. Verify metadata types are enabled

### Issue: Outdated Information

**Solutions**:
1. Check refresh frequency setting
2. Trigger manual refresh
3. Verify real-time sync is working

## Best Practices

### 1. Security
- Only enable for users who need metadata access
- Use scope limiting for sensitive orgs
- Review permissions regularly

### 2. Performance
- Use real-time sync for development orgs
- Use hourly/daily for production
- Limit metadata types if needed

### 3. Accuracy
- Keep metadata documentation up to date
- Use field descriptions
- Add comments to Apex and Flows

### 4. Maintenance
- Regularly review what's shared
- Update scope as org evolves
- Monitor usage and performance

## Advanced: Programmatic Access

### Via Python (Your Project)

You can use the Salesforce CLI and APIs:

```python
import subprocess
import json

def get_org_metadata():
    """Retrieve org metadata for Agentforce"""
    
    # Get all custom objects
    result = subprocess.run(
        ['sf', 'data', 'query', '--query', 
         'SELECT QualifiedApiName, Label FROM EntityDefinition WHERE IsCustomizable = true',
         '--target-org', 'vibes-org', '--json'],
        capture_output=True, text=True
    )
    
    objects = json.loads(result.stdout)
    return objects

# Get flow definitions
def get_flows():
    result = subprocess.run(
        ['sf', 'data', 'query', '--query',
         'SELECT Id, Label, ProcessType, ActiveVersion FROM FlowDefinition',
         '--target-org', 'vibes-org', '--use-tooling-api', '--json'],
        capture_output=True, text=True
    )
    
    flows = json.loads(result.stdout)
    return flows

# Use it
metadata = get_org_metadata()
flows = get_flows()
```

### Via Tooling API

```bash
# Get custom objects
sf data query --query "SELECT QualifiedApiName, Label FROM EntityDefinition WHERE IsCustomizable = true" --target-org vibes-org

# Get flows
sf data query --query "SELECT Id, Label, ProcessType FROM FlowDefinition" --target-org vibes-org --use-tooling-api

# Get validation rules
sf data query --query "SELECT Id, ValidationName, Active, ErrorDisplayField FROM ValidationRule" --target-org vibes-org --use-tooling-api
```

## Summary

**Metadata Grounding enables Agentforce to**:
- ✅ Understand your org configuration
- ✅ Generate diagrams and documentation
- ✅ Answer org-specific questions
- ✅ Provide contextual guidance
- ✅ Analyze dependencies and impacts

**Setup Steps**:
1. Enable Einstein/Agentforce
2. Enable Metadata Grounding in settings
3. Configure scope and permissions
4. Test with metadata questions

**Key Difference from Data Cloud**:
- **Metadata Grounding**: Accesses org configuration (objects, flows, code)
- **Data Cloud**: Accesses actual data records and analytics

This is likely what you saw at TDX 2026 - Agentforce understanding and explaining your org's setup!

---

**Created**: 4/28/2026
**Purpose**: Enable Agentforce to access org metadata for contextual assistance