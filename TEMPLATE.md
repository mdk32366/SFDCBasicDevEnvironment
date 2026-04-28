# Agentforce Vibes - Project Template

This repository serves as a **starter template** for Agentforce development projects. Use it to quickly spin up new hybrid Salesforce/Python projects with Data Cloud integration.

## Quick Start - Clone & Customize

### Option 1: PowerShell Script (Recommended - Windows)

```powershell
# Run from your projects directory
.\init-new-project.ps1 -ProjectName "MyNewProject"
```

This script will:
- Clone the template
- Rename directories and files
- Update configuration files
- Set up a new Salesforce org alias
- Initialize git for the new project

### Option 2: Manual Setup (All Platforms)

```bash
# 1. Clone the template
git clone https://github.com/mdk32366/SFDCBasicDevEnvironment.git MyNewProject
cd MyNewProject

# 2. Remove the git history (start fresh)
rm -r .git
git init

# 3. Update project configuration files:
# - sfdx-project.json (project name, namespace, etc.)
# - python/requirements.txt (if needed)
# - README.md (project description)
# - .env.example (your org details)

# 4. Set up new Salesforce org alias
sf login org web --alias my-new-org
sf config set target-org my-new-org

# 5. Create your first commit
git add .
git commit -m "Initial commit: Project setup from Agentforce Vibes template"
```

## Template Structure

```
MyNewProject/
├── force-app/main/default/        # Apex code
│   ├── classes/
│   │   ├── VibesAgent.cls         # Customize for your agent
│   │   └── VibesAgentTest.cls
│   └── ...
├── python/                         # Python agent logic
│   ├── agent.py                   # Main agent class
│   ├── salesforce_connector.py    # Salesforce integration
│   ├── requirements.txt           # Python dependencies
│   └── test_agent.py
├── data-cloud/                    # Data Cloud integration
│   ├── orchestrator.py            # Pipeline orchestrator
│   ├── connectors/                # Data connectors
│   ├── transformations/           # Data transformations & ML
│   ├── schemas/                   # Unified catalog
│   └── ...
├── config/                        # Configuration
│   └── DEV_ORG_SETUP.md          # Org setup documentation
├── .vscode/                       # VS Code tasks & settings
├── sfdx-project.json             # Salesforce project config
├── .env.example                  # Environment template
└── README.md
```

## Customization Guide

### 1. Update Project Metadata

**sfdx-project.json**
```json
{
  "name": "YourProjectName",
  "namespace": "your_namespace",
  "sourceApiVersion": "59.0",
  "sfdcLoginUrl": "https://login.salesforce.com"
}
```

### 2. Rename the Apex Agent

Replace `VibesAgent` with your agent name throughout:
- `force-app/main/default/classes/YourAgent.cls`
- Update class names in Apex code
- Update test class accordingly

### 3. Customize Python Agent

Update `python/agent.py`:
```python
class YourAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        # Your implementation
        pass
```

### 4. Configure Data Cloud

Customize `data-cloud/schemas/unified_catalog.json`:
- Add your specific entities
- Configure your data sources
- Define entity relationships

### 5. Set Environment Variables

Copy `.env.example` to `.env` and populate:
```bash
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_secret
SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com
```

## Development Workflow

### Deploy to Salesforce
```bash
sfdx project deploy start -d force-app/ --target-org my-new-org
```

### Run Python Tests
```bash
python -m pytest python/test_agent.py -v
```

### Run Data Cloud Pipeline
```bash
python data-cloud/orchestrator.py
```

### Verify Installation
```bash
python data-cloud/verify_installation.py
```

## Included Features

✓ **Apex Agent Framework** - Salesforce server-side logic  
✓ **Python Agent SDK** - Python-based agent implementation  
✓ **Data Cloud Integration** - Unified data catalog and ML pipelines  
✓ **Data Validation** - Schema compliance checking  
✓ **ML Training** - Dataset creation and feature engineering  
✓ **Multi-Format Export** - CSV, Parquet, JSON support  
✓ **Orchestrator** - End-to-end data pipeline automation  
✓ **Comprehensive Tests** - Unit tests for all components  
✓ **VS Code Tasks** - Build and deployment automation  
✓ **Documentation** - Setup guides and quickstart examples  

## Key Technologies

- **Salesforce**: Apex (v59.0), Lightning Web Components
- **Python**: Agent development, data processing (3.11+)
- **Data Cloud**: Unified catalog, ML training infrastructure
- **Build Tools**: Salesforce CLI (SFDX), npm, pip
- **Testing**: pytest, unit test suites
- **Data Processing**: pandas, numpy, scikit-learn, pyarrow

## Next Steps After Setup

1. ✅ Initialize new project from template
2. ✅ Customize Apex and Python agents for your use case
3. ✅ Configure Data Cloud entities and data sources
4. ✅ Deploy to your Salesforce Dev Org
5. ✅ Configure CI/CD pipelines (GitHub Actions, etc.)
6. ✅ Train ML models with your data
7. ✅ Deploy agents to production

## Support & Documentation

- [README.md](README.md) - Full project documentation
- [data-cloud/SETUP_GUIDE.md](data-cloud/SETUP_GUIDE.md) - Data Cloud configuration
- [data-cloud/QUICKSTART.md](data-cloud/QUICKSTART.md) - Quick reference
- [config/DEV_ORG_SETUP.md](config/DEV_ORG_SETUP.md) - Org setup instructions

## Tips for Using as Template

### Best Practices
- Start with this template for all new Agentforce projects
- Customize incrementally - don't change everything at once
- Keep the folder structure consistent across projects
- Use the same naming conventions for easy team collaboration
- Regularly update from the template for improvements

### Avoiding Common Mistakes
- ❌ Don't forget to update `sfdx-project.json` namespace
- ❌ Don't use template code unchanged - customize agents
- ❌ Don't skip environment variable configuration
- ❌ Don't forget to create new `.env` from `.env.example`
- ✅ Do start with small, focused agents
- ✅ Do test thoroughly before deploying
- ✅ Do commit frequently to git

## Contributing Back

Have improvements to the template? Consider:
1. Testing changes thoroughly
2. Documenting new features
3. Creating a pull request to the base template repo
4. Sharing best practices with the team

---

**Template Version**: 1.0  
**Created**: April 28, 2026  
**Salesforce API**: v59.0  
**Python Version**: 3.11+  
