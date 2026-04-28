# Agentforce Vibes - Template Usage Quick Reference

## One-Command Project Setup (Windows)

```powershell
# From your projects folder
.\init-new-project.ps1 -ProjectName "MyAgentProject"
```

The script will:
- ✓ Clone the template repository
- ✓ Set up a fresh git repository
- ✓ Update configuration files for your project
- ✓ Create environment files
- ✓ Make an initial commit

## Manual Multi-Platform Setup

```bash
# 1. Clone
git clone https://github.com/mdk32366/SFDCBasicDevEnvironment.git MyProject
cd MyProject
rm -r .git && git init

# 2. Configure
# - Edit sfdx-project.json (project name, namespace)
# - Copy .env.example to .env
# - Edit README.md

# 3. Authenticate
sf login org web --alias my-org
sf config set target-org my-org

# 4. First commit
git add . && git commit -m "Initial project setup"
```

## Project Customization Checklist

### Apex Code
- [ ] Rename `VibesAgent.cls` → `YourAgent.cls`
- [ ] Update class implementation
- [ ] Update corresponding test class
- [ ] Review `.cls-meta.xml` API version

### Python Agent
- [ ] Customize `agent.py` class and methods
- [ ] Update `requirements.txt` with dependencies
- [ ] Test with `python -m pytest python/test_agent.py -v`

### Data Cloud
- [ ] Edit `data-cloud/schemas/unified_catalog.json`
- [ ] Define your entities and data sources
- [ ] Configure `connectors/` for your systems
- [ ] Update `transformations/` as needed

### Configuration
- [ ] Update `sfdx-project.json` with project details
- [ ] Configure `.env` with Salesforce credentials
- [ ] Update `README.md` with project description

## Verify Setup

```bash
# Test all components
python data-cloud/verify_installation.py

# Run unit tests
python -m pytest python/test_agent.py -v
python -m pytest data-cloud/test_datacloud.py -v

# Deploy to Salesforce
sfdx project deploy start -d force-app/
```

## Key Features Inherited

✓ Hybrid Salesforce/Python development  
✓ Data Cloud unified catalog (4 entities, 3 sources)  
✓ ML training dataset generation  
✓ Multi-format data export  
✓ End-to-end orchestration pipeline  
✓ Comprehensive unit tests  
✓ VS Code automation tasks  
✓ Full documentation & quickstart guides  

## File Structure

```
MyProject/
├── force-app/main/default/    # Apex: Customize VibesAgent
├── python/                    # Python: Customize agent.py
├── data-cloud/               # Data Cloud: Update catalog.json
├── config/                   # Configuration files
├── .vscode/                  # Tasks and settings
├── sfdx-project.json        # Update: project name
├── .env.example             # Copy to .env and configure
└── README.md                # Update: project description
```

## Common Tasks

### Deploy Apex to Org
```bash
sf project deploy start -d force-app/
```

### Run Python Tests
```bash
python -m pytest python/ -v
```

### Generate ML Dataset
```bash
cd data-cloud
python demo_ml_training.py
```

### Full Data Pipeline
```bash
python data-cloud/demo_orchestrator_pipeline.py
```

### Verify System Health
```bash
python data-cloud/verify_installation.py
```

## Support

- [TEMPLATE.md](TEMPLATE.md) - Full template documentation
- [README.md](README.md) - Project overview
- [data-cloud/SETUP_GUIDE.md](data-cloud/SETUP_GUIDE.md) - Data Cloud setup
- [data-cloud/QUICKSTART.md](data-cloud/QUICKSTART.md) - Code examples

## Tips

✓ Start with one agent and expand gradually  
✓ Test thoroughly before deploying  
✓ Keep regular commits to git  
✓ Use descriptive branch names  
✓ Document your customizations  

---

**Agentforce Vibes Template v1.0**  
Ready to build powerful AI agents! 🚀
