# Unified Data Catalog - Setup Guide

The **Unified Catalog Browser** Lightning Web Component has been successfully deployed to your Dev Org. Follow these steps to access it:

## Option 1: Add to Home Page (Recommended)

1. Go to your **Dev Org** (vibes-org)
2. Click your **Profile** icon → **Settings**
3. Go to **Display** → **Home Page**
4. Click **Edit Page**
5. In the Lightning App Builder:
   - Search for **"Unified Catalog Browser"** component
   - Drag it onto your home page
   - Click **Save**
6. Done! You can now access the Data Catalog from your home page

## Option 2: Add to an App

1. In your **Dev Org**, go to **Setup**
2. Search for **"App Manager"**
3. Find an existing app (or create a new Lightning App)
4. Click the **App Name** → **Edit**
5. In the Navigation section, scroll down to **Available Items**
6. Find **Unified Catalog Browser**
7. Click the **+** button to add it
8. Click **Save** and **Activate** if needed

## Option 3: Add as a Tab (via Lightning Application)

1. In **Setup**, go to **Create** → **Apps** → **Lightning Apps**
2. Click **New Lightning App**
3. Name it: **Agentforce Vibes**
4. In the **Items** section, search for and add **Unified Catalog Browser**
5. Set the landing page if desired
6. Click **Save**
7. Click **Activate** to make it available
8. The app will appear in your **App Launcher**

## Accessing the Unified Catalog

Once added, the Unified Catalog Browser will display:

- **4 Entities**: Account, Contact, Opportunity, Policy
- **Data Sources**: Salesforce, External Systems
- **Entity Details**: Source system, type, and field count
- **Browse Interface**: Click on any entity to view details

## Component Features

✅ **Browse Entities** - View all data catalog entities in a card-based layout  
✅ **Entity Details** - Click any entity to see detailed information  
✅ **Data Sources** - Track which systems data comes from  
✅ **Responsive Design** - Works on desktop and mobile

## Integration with Data Cloud

The component is configured to work with your Salesforce Data Cloud unified catalog:

```json
{
  "entities": [
    "Account", "Contact", "Opportunity", "Policy"
  ],
  "sources": [
    "Salesforce", "External System"
  ]
}
```

To connect live Data Cloud data, update `unifiedCatalogBrowser.js` with your API calls to the Data Cloud API endpoints.

## Next Steps

1. Add the component to your preferred location (Home, Tab, or App)
2. Test browsing the unified catalog entities
3. Customize the component styling in `unifiedCatalogBrowser.html`
4. Connect live data from your Data Cloud instance
5. Share the catalog with your team

---

**Component Location**: `force-app/main/default/lwc/unifiedCatalogBrowser/`
