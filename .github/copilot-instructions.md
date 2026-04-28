# Agentforce Vibes Development Environment

## Project Overview
Agentforce Vibes is a hybrid development project combining Salesforce Apex and Python for intelligent agent development.

## Setup Checklist

- [x] **Verify Project Structure** - Core directories created
- [x] **Install Salesforce CLI** - Required for Apex development
- [x] **Configure Python Environment** - Virtual environment and dependencies
- [x] **Install VS Code Extensions** - Salesforce and Python tools
- [x] **Configure sfdx-project.json** - Salesforce project settings
- [x] **Create Python Virtual Environment** - Isolated Python environment
- [x] **Install Dependencies** - npm and pip packages
- [x] **Create Development Tasks** - Build and test tasks
- [ ] **Verify Installation** - Test Salesforce CLI and Python
- [ ] **Launch Development Environment** - Ready for development

## Development Stack
- **Salesforce**: Apex, Lightning Web Components
- **Python**: Agent development, data processing, integrations
- **Build Tools**: Salesforce CLI (SFDX), npm, pip
- **Version Control**: Git

## Key Directories
```
├── force-app/main/default/     # Apex classes, components
├── python/                      # Python modules and scripts
├── config/                      # Configuration files
└── .github/                     # GitHub workflows and docs
```

## Dev Org Setup

This project uses a persistent Dev Org (lasts 30+ days unlike Scratch Orgs).

1. Copy `.env.example` to `.env` and add your Salesforce credentials
2. Run `sf login org web --alias vibes-org` to authenticate with your Dev Org
3. Run `sf config set target-org vibes-org` to set it as the default
4. Use VS Code tasks to deploy and test code
