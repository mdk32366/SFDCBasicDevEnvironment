# Dev Org Setup Guide

## Overview

Agentforce Vibes uses a persistent **Dev Org** that lasts indefinitely (unlike Scratch Orgs which expire after 30 days).

## Initial Setup (One-time)

### 1. Authenticate with Your Dev Org
```bash
sf login org web --alias vibes-org
```

This opens a browser window for you to log in with your Salesforce credentials. A Dev Org provides a stable development environment that persists across sessions.

### 2. Set as Default Org (Optional)
```bash
sf config set target-org vibes-org
```

### 3. Verify Connection
```bash
sf org list
```

You should see `vibes-org` listed and connected.

## Advantages of Dev Org

✅ **Persistent**: Stays active indefinitely (no 30-day expiration)  
✅ **Cost-Effective**: Uses your existing Salesforce instance  
✅ **Collaborative**: Team members can access the same org  
✅ **Data Retention**: Keep test data and configurations between sessions  

## Working with Your Dev Org

### Deploy Code
```bash
sf project deploy start -o vibes-org
```

### Retrieve Changes
```bash
sf project retrieve start -o vibes-org
```

### Open Org in Browser
```bash
sf org open -o vibes-org
```

## Notes

- The Dev Org is tied to your Salesforce account
- Keep `.env` and credentials secure
- Use meaningful deployment names for tracking changes
- Set up proper code reviews before deploying to production
