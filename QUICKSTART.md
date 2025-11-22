# Quick Start Guide

Get up and running with Databricks OAuth Auto Token Rotation in 2 minutes.

## Installation

```bash
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git
```

## Setup (Choose One Method)

### Method 1: Databricks CLI (Easiest for Personal Use)

```bash
# 1. Install Databricks CLI
pip install databricks-cli

# 2. Login via browser
databricks auth login --host https://your-workspace.cloud.databricks.com

# 3. Set PostgreSQL connection details
export DATABRICKS_PG_HOST="instance-xyz.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="your-email@company.com"

# 4. Test it
databricks-oauth-rotator --once

# 5. Install as background service
databricks-oauth-install \
  --pg-host instance-xyz.database.cloud.databricks.com \
  --pg-username your-email@company.com
```

### Method 2: OAuth M2M (Best for Production)

```bash
# 1. Create service principal in Databricks workspace
# 2. Generate OAuth secret
# 3. Set environment variables

export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_CLIENT_ID="service-principal-id"
export DATABRICKS_CLIENT_SECRET="oauth-secret"
export DATABRICKS_PG_HOST="instance-xyz.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="your-email@company.com"

# 4. Test it
databricks-oauth-rotator --once

# 5. Install as background service
databricks-oauth-install
```

## Verify It's Working

```bash
# Check service status
databricks-oauth-status

# Follow logs in real-time
tail -f ~/.databricks_oauth_rotator.log

# Check .pgpass file
cat ~/.pgpass
```

## What Happens Next?

The service will now:
- ✅ Run in the background automatically
- ✅ Rotate your OAuth token every 50 minutes
- ✅ Update your `.pgpass` file before tokens expire
- ✅ Start automatically on system login
- ✅ Log all operations to `~/.databricks_oauth_rotator.log`

## Common Commands

```bash
# Service management
databricks-oauth-status     # Check if service is running
databricks-oauth-restart    # Restart the service
databricks-oauth-uninstall  # Remove the service

# Manual rotation (test mode)
databricks-oauth-rotator --once

# Custom configuration
databricks-oauth-rotator \
  --workspace-url https://workspace.cloud.databricks.com \
  --pg-host instance.database.cloud.databricks.com \
  --pg-username user@company.com \
  --interval 45 \
  --once
```

## Troubleshooting

### Service not starting?
```bash
cat ~/.databricks_oauth_rotator_stderr.log
```

### Token not updating?
```bash
# Check authentication
databricks auth login --host https://your-workspace.cloud.databricks.com

# Test manually
databricks-oauth-rotator --once

# Check logs
tail -100 ~/.databricks_oauth_rotator.log
```

### Need help?
- Check the [full README](README.md)
- Open an [issue on GitHub](https://github.com/suryasai87/oauth_auto_token_rotation/issues)

## Example: Complete Setup

```bash
# Install
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git

# Login
databricks auth login --host https://fe-vm-hls-amer.cloud.databricks.com

# Configure
export DATABRICKS_PG_HOST="instance-abc123.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="user@company.com"

# Test
databricks-oauth-rotator --once

# Install service
databricks-oauth-install

# Verify
databricks-oauth-status

# Done! Your tokens will now rotate automatically every 50 minutes.
```

That's it! You'll never need to manually update OAuth tokens again.
