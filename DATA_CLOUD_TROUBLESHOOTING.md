# Data Cloud Unified Catalog - Troubleshooting Guide

## Issue: Unified Catalog Menu Not Visible

If you're not seeing the "Unified Catalog" menu in Data Cloud, here are the possible reasons and solutions:

## Root Causes

### 1. Data Cloud Not Enabled
**Symptom**: No Data Cloud app in App Launcher, or Data Cloud app exists but is empty/minimal

**Solution**:
1. Go to **Setup** → Search "Data Cloud"
2. Click **Data Cloud Setup**
3. If you see a setup wizard, Data Cloud is NOT enabled yet
4. You'll need to enable/provision Data Cloud first

**To Enable Data Cloud**:
- Contact your Salesforce Account Executive
- Data Cloud requires a separate license
- Once licensed, enable via Setup → Data Cloud → Enable

### 2. Data Cloud Not Licensed
**Symptom**: Can't access Data Cloud Setup or get licensing errors

**Solution**:
- Data Cloud is a paid add-on to Salesforce
- Check with your org administrator about licensing
- Developer orgs may not include Data Cloud
- Trial orgs may have limited Data Cloud features

### 3. Unified Catalog Feature Not Available
**Symptom**: Data Cloud works but no "Unified Catalog" menu item

**Possible Reasons**:
- **API Version**: Requires API v66.0+ (you have this ✅)
- **Data Cloud Edition**: Some features are edition-specific
- **Feature Flag**: Unified Catalog may need to be enabled
- **Pilot/Beta**: Feature may be in pilot for select customers

### 4. Wrong Data Cloud App Version
**Symptom**: Old Data Cloud interface without new TDX 2026 features

**Solution**:
- Data Cloud UI updates over time
- Unified Catalog may be in newer versions only
- Check if your org has latest Data Cloud updates

## Verification Steps

### Step 1: Check Data Cloud Status

```bash
sf org open --target-org vibes-org --path /lightning/setup/DataCloudSetup/home
```

**What to Look For**:
- ✅ **Enabled**: You see Data Cloud dashboard with data sources, streams, etc.
- ❌ **Not Enabled**: You see a setup wizard or "Get Started" page
- ❌ **Not Licensed**: You see licensing/provisioning messages

### Step 2: Check Data Cloud App

1. Open App Launcher
2. Search for "Data Cloud"
3. Click to open

**What to Look For**:
- ✅ **Full App**: You see: Home, Data Explorer, Data Model, Data Streams, etc.
- ⚠️ **Limited App**: You see basic interface with few options
- ❌ **No App**: Data Cloud not installed

### Step 3: Check for Unified Catalog

In Data Cloud app, look in left navigation for:
- Data Model
- Data Streams
- **Unified Catalog** ← This is what you're looking for
- Segments
- Calculated Insights

**If you see "Data Model" but not "Unified Catalog"**:
- The feature may not be available in your org yet
- It may be called something different
- It may be under a different menu

## Alternative: The "Unified Catalog" may actually be "Data Model"

In some Data Cloud versions, what was shown as "Unified Catalog" at TDX 2026 is accessed through:

**Data Cloud → Data Model**

This shows:
- All Data Model Objects (DMOs)
- Entity schemas and relationships
- Data lineage
- Source mappings

**Try this**:
1. Open Data Cloud app
2. Click "Data Model" in left nav
3. This IS your unified catalog of data entities

## What Data Cloud Features You CAN Use

Even without the specific "Unified Catalog" menu label, you can use:

### Via Data Cloud App:
1. **Data Model** → View all entities
2. **Data Explorer** → Query catalog data
3. **Data Streams** → See data sources
4. **Segments** → Create unified profiles

### Via Your Project Tools:

```bash
# Use Python to interact with catalog
cd data-cloud
python orchestrator.py

# This will:
# - Connect to Salesforce
# - Create/sync DMOs
# - Manage catalog entries
# - Export data
```

### Via Salesforce CLI:

```bash
# Query Data Model Objects
sf data query --query "SELECT Id, Name FROM DataModelObject" --target-org vibes-org --use-tooling-api

# List Data Streams
sf data query --query "SELECT Id, Name FROM DataStream" --target-org vibes-org --use-tooling-api
```

## Understanding TDX 2026 vs Reality

**What Was Shown at TDX 2026**:
- Preview of future Data Cloud features
- Roadmap items that may not be released yet
- Features that may require specific licenses
- Demos that may be from beta/pilot programs

**Current Reality**:
- Some TDX features are released
- Some are still in development
- Some require specific licenses/editions
- Feature availability varies by org type

## Recommended Path Forward

### Option 1: Use Data Model Instead
The **Data Model** section in Data Cloud is essentially your unified catalog:
1. Open Data Cloud app
2. Go to **Data Model**
3. View all your entities (DMOs)
4. Click any entity to see details

### Option 2: Use Python Tools
Your project can work with the catalog programmatically:
```bash
cd data-cloud
python orchestrator.py
```

### Option 3: Check with Salesforce
If you need the exact "Unified Catalog" menu:
- Contact Salesforce Support
- Ask about Data Cloud licensing
- Inquire about feature availability
- Request access to TDX 2026 features

### Option 4: Use Alternative Org
- Create a new scratch org with Data Cloud
- Use a Developer Edition org
- Request a Data Cloud trial

## Documentation You Have

Even without the UI, you have:
1. **Complete Guide**: `data-cloud/TDX_2026_UNIFIED_CATALOG_GUIDE.md`
2. **Python Tools**: Working connectors and orchestration
3. **Schema Definition**: `data-cloud/schemas/unified_catalog.json`
4. **This Troubleshooting Guide**

## Next Steps

1. **Check Your Org Type**:
   ```bash
   sf org display --target-org vibes-org
   ```
   
2. **Try Data Model**:
   - Open Data Cloud → Data Model
   - This may be your "Unified Catalog"

3. **Use Python Tools**:
   ```bash
   cd data-cloud
   python orchestrator.py
   ```

4. **Contact Admin**:
   - Ask about Data Cloud licensing
   - Request feature enablement
   - Inquire about TDX 2026 features

## Summary

**The "Unified Catalog" Menu May Not Exist (Yet) Because**:
- ❌ Data Cloud not enabled in your org
- ❌ Data Cloud not licensed
- ❌ Feature still in pilot/beta
- ❌ Feature not released yet
- ✅ Feature is actually called "Data Model"

**What You CAN Do**:
- ✅ Use Data Model section (if Data Cloud is enabled)
- ✅ Use Python tools in this project
- ✅ Read comprehensive documentation created
- ✅ Contact Salesforce about licensing

**Bottom Line**: The specific "Unified Catalog" menu name from TDX 2026 may not be available in all orgs yet, but the functionality exists under "Data Model" if Data Cloud is enabled.

---

**Created**: 4/28/2026
**Purpose**: Help troubleshoot missing Unified Catalog menu