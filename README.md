# Agentforce Vibes

A development environment for building intelligent agents using Salesforce Apex and Python.

## Prerequisites

- Node.js 16+ (for Salesforce CLI)
- Python 3.9+
- Salesforce CLI (sfdx)
- Git

## Quick Start

### 1. Install Salesforce CLI
```bash
npm install -g @salesforce/cli
```

### 2. Set Up Python Environment
```bash
cd python
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3. Authenticate with Salesforce (Dev Org)
```bash
sf login org web --alias vibes-org
sf config set target-org vibes-org
```

Your Dev Org will persist indefinitely (unlike Scratch Orgs which expire after 30 days).

## Project Structure

- **force-app/main/default/** - Salesforce Apex and Lightning components
- **python/** - Python agent code and utilities
- **config/** - Configuration files for Salesforce and development
- **.vscode/** - VS Code settings and tasks

## Development

### Apex Development
- Use VS Code with Salesforce Extension Pack
- Deploy code to Dev Org with `sf project deploy start -o vibes-org`
- Retrieve changes with `sf project retrieve start -o vibes-org`

### Python Development
- Run scripts from `python/` directory
- Install additional packages with `pip install <package>` and update `requirements.txt`

## Useful Commands

```bash
# Salesforce CLI
sf org list
sf project deploy start -o vibes-org
sf project retrieve start -o vibes-org

# Python
pip install -r python/requirements.txt
python python/main.py
```

## Documentation

See [.github/copilot-instructions.md](.github/copilot-instructions.md) for detailed setup instructions.
