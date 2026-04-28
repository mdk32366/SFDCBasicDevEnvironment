#Requires -Version 5.0

<#
.SYNOPSIS
Initialize a new Agentforce project from the template repository.

.DESCRIPTION
This script clones the BasicDevEnvironment template and customizes it for a new project.
It updates configuration files, sets up git, and prepares the environment.

.PARAMETER ProjectName
The name of the new project (required).

.PARAMETER TemplateRepository
The URL or path to the template repository.
Defaults to https://github.com/mdk32366/SFDCBasicDevEnvironment.git

.PARAMETER OrgAlias
The Salesforce org alias for this project.
Defaults to {ProjectName}-org

.EXAMPLE
.\init-new-project.ps1 -ProjectName "CustomerAI"

.EXAMPLE
.\init-new-project.ps1 -ProjectName "DataAnalyzer" -OrgAlias "data-analytics-org"
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$false)]
    [string]$TemplateRepository = "https://github.com/mdk32366/SFDCBasicDevEnvironment.git",
    
    [Parameter(Mandatory=$false)]
    [string]$OrgAlias = ""
)

# Defaults
if ([string]::IsNullOrEmpty($OrgAlias)) {
    $OrgAlias = "$($ProjectName.ToLower())-org"
}

$projectPath = Join-Path -Path $PWD -ChildPath $ProjectName
$projectNameFormatted = $ProjectName -replace '[^a-zA-Z0-9_]', '_'

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║         AGENTFORCE VIBES - PROJECT INITIALIZATION              ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""

# Check if project directory already exists
if (Test-Path $projectPath) {
    Write-Host "❌ Error: Directory '$ProjectName' already exists" -ForegroundColor Red
    exit 1
}

# Step 1: Clone template
Write-Host "[1] Cloning template repository..."
Write-Host "    From: $TemplateRepository"
Write-Host "    To:   $projectPath"

try {
    git clone $TemplateRepository $projectPath 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ Template cloned successfully" -ForegroundColor Green
    } else {
        Write-Host "    ❌ Failed to clone repository" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "    ❌ Error: $_" -ForegroundColor Red
    exit 1
}

# Change to project directory
Push-Location $projectPath

# Step 2: Clear git history
Write-Host ""
Write-Host "[2] Initializing fresh git repository..."
try {
    Remove-Item -Path ".git" -Recurse -Force -ErrorAction Stop | Out-Null
    git init | Out-Null
    Write-Host "    ✓ Git repository initialized" -ForegroundColor Green
} catch {
    Write-Host "    ⚠ Warning: Could not reinitialize git: $_" -ForegroundColor Yellow
}

# Step 3: Update configuration files
Write-Host ""
Write-Host "[3] Updating configuration files..."

# Update sfdx-project.json
$sfdxConfigPath = "sfdx-project.json"
if (Test-Path $sfdxConfigPath) {
    $sfdxConfig = Get-Content $sfdxConfigPath | ConvertFrom-Json
    $sfdxConfig.name = $projectNameFormatted
    $sfdxConfig | ConvertTo-Json -Depth 10 | Set-Content $sfdxConfigPath
    Write-Host "    ✓ sfdx-project.json updated" -ForegroundColor Green
}

# Update README.md
$readmePath = "README.md"
if (Test-Path $readmePath) {
    $readmeContent = Get-Content $readmePath -Raw
    $readmeContent = $readmeContent -replace "Agentforce Vibes", $ProjectName
    $readmeContent = $readmeContent -replace "vibes-org", $OrgAlias
    Set-Content $readmePath $readmeContent
    Write-Host "    ✓ README.md updated" -ForegroundColor Green
}

# Step 4: Environment variables
Write-Host ""
Write-Host "[4] Setting up environment..."

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env" -ErrorAction SilentlyContinue
    Write-Host "    ✓ .env created from template" -ForegroundColor Green
    Write-Host "    ⚠ Update .env with your Salesforce credentials" -ForegroundColor Yellow
}

# Step 5: Initialize Salesforce
Write-Host ""
Write-Host "[5] Salesforce Configuration"
Write-Host "    Org Alias: $OrgAlias"
Write-Host "    To authenticate with Salesforce, run:"
Write-Host "    ➜ sf login org web --alias $OrgAlias" -ForegroundColor Cyan

# Step 6: Python environment
Write-Host ""
Write-Host "[6] Python Environment Setup"
Write-Host "    To set up Python virtual environment:"
Write-Host "    ➜ python -m venv venv" -ForegroundColor Cyan
Write-Host "    ➜ .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "    ➜ pip install -r python/requirements.txt" -ForegroundColor Cyan

# Step 7: Verification
Write-Host ""
Write-Host "[7] Project Structure"
Write-Host "    ✓ force-app/              (Apex code)" -ForegroundColor Green
Write-Host "    ✓ python/                (Python agent)" -ForegroundColor Green
Write-Host "    ✓ data-cloud/            (Data Cloud)" -ForegroundColor Green
Write-Host "    ✓ config/                (Configuration)" -ForegroundColor Green
Write-Host "    ✓ .vscode/               (Tasks & settings)" -ForegroundColor Green

# Step 8: Git initial commit
Write-Host ""
Write-Host "[8] Creating initial commit..."
try {
    git add . | Out-Null
    git commit -m "Initial commit: $ProjectName - Created from Agentforce Vibes template" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ Initial commit created" -ForegroundColor Green
    }
} catch {
    Write-Host "    ⚠ Warning: Could not create commit: $_" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗"
Write-Host "║                   ✓ PROJECT INITIALIZED                        ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝"
Write-Host ""
Write-Host "Project: $ProjectName" -ForegroundColor Cyan
Write-Host "Location: $projectPath" -ForegroundColor Cyan
Write-Host "Org Alias: $OrgAlias" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Authenticate with Salesforce:"
Write-Host "   ➜ cd $ProjectName" -ForegroundColor Green
Write-Host "   ➜ sf login org web --alias $OrgAlias" -ForegroundColor Green
Write-Host ""
Write-Host "2. Set up Python virtual environment:"
Write-Host "   ➜ python -m venv venv" -ForegroundColor Green
Write-Host "   ➜ .\venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "   ➜ pip install -r python/requirements.txt" -ForegroundColor Green
Write-Host ""
Write-Host "3. Deploy Apex code to org:"
Write-Host "   ➜ sfdx project deploy start -d force-app/ --target-org $OrgAlias" -ForegroundColor Green
Write-Host ""
Write-Host "4. Customize your project:"
Write-Host "   ➜ Update TEMPLATE.md for customization guide" -ForegroundColor Green
Write-Host "   ➜ See README.md and data-cloud/SETUP_GUIDE.md" -ForegroundColor Green
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Cyan
Write-Host ""

Pop-Location
