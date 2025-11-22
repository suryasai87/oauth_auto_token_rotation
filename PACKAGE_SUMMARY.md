# Databricks OAuth Auto Token Rotation - Package Summary

## 🎉 Package Successfully Published!

**Repository:** https://github.com/suryasai87/oauth_auto_token_rotation

## Installation

```bash
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git
```

## Package Structure

```
oauth_auto_token_rotation/
├── databricks_oauth_rotator/          # Main package
│   ├── __init__.py                    # Package initialization
│   ├── rotator.py                     # Core OAuth rotation logic
│   ├── cli.py                         # Command-line interface
│   ├── install.py                     # Service installation helper
│   └── templates/
│       └── launchd.plist.template     # macOS LaunchAgent template
├── setup.py                           # Package configuration
├── requirements.txt                   # Dependencies
├── MANIFEST.in                        # Package manifest
├── README.md                          # Full documentation
├── QUICKSTART.md                      # 2-minute setup guide
├── LICENSE                            # Apache 2.0 license
└── .gitignore                         # Git ignore rules
```

## Key Features

✅ **Zero-Config Installation** - One `pip install` command
✅ **Automatic Token Rotation** - Every 50 minutes (before 60-min expiry)
✅ **Dual Authentication** - OAuth M2M (production) + CLI (development)
✅ **Background Service** - macOS LaunchAgent / Linux systemd
✅ **Atomic Updates** - Safe .pgpass file modifications
✅ **Comprehensive Logging** - Rotating logs with full operation history
✅ **Cross-Platform** - macOS and Linux support
✅ **Fully Parameterized** - All settings configurable via CLI or env vars

## CLI Commands

### Main Rotator
```bash
databricks-oauth-rotator --once                    # Test rotation
databricks-oauth-rotator --interval 45             # Custom interval
databricks-oauth-rotator --help                    # Full help
```

### Service Management
```bash
databricks-oauth-install                           # Install service
databricks-oauth-status                            # Check status
databricks-oauth-restart                           # Restart service
databricks-oauth-uninstall                         # Remove service
```

## Python API

```python
from databricks_oauth_rotator import DatabricksOAuthRotator

rotator = DatabricksOAuthRotator(
    workspace_url="https://workspace.cloud.databricks.com",
    pg_host="instance.database.cloud.databricks.com",
    pg_username="user@company.com"
)

rotator.run_once()      # Single rotation
rotator.run_daemon()    # Continuous rotation
```

## Environment Variables

- `DATABRICKS_HOST` - Workspace URL
- `DATABRICKS_CLIENT_ID` - OAuth client ID (M2M)
- `DATABRICKS_CLIENT_SECRET` - OAuth secret (M2M)
- `DATABRICKS_PG_HOST` - PostgreSQL hostname
- `DATABRICKS_PG_USERNAME` - PostgreSQL username

## Configuration Parameters

All aspects are configurable:
- Workspace URL
- OAuth credentials
- PostgreSQL connection details
- .pgpass file location
- Log file location
- Rotation interval

## Authentication Methods

### 1. Databricks CLI (Development)
```bash
databricks auth login --host https://workspace.cloud.databricks.com
databricks-oauth-rotator --once
```

### 2. OAuth M2M (Production)
```bash
export DATABRICKS_CLIENT_ID="sp-id"
export DATABRICKS_CLIENT_SECRET="sp-secret"
databricks-oauth-rotator --once
```

## Installation Examples

### Minimal (with CLI auth)
```bash
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git
databricks auth login
databricks-oauth-install --pg-host instance.db.com --pg-username user@co.com
```

### Full (with OAuth M2M)
```bash
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git
export DATABRICKS_HOST="https://workspace.cloud.databricks.com"
export DATABRICKS_CLIENT_ID="service-principal-id"
export DATABRICKS_CLIENT_SECRET="oauth-secret"
export DATABRICKS_PG_HOST="instance.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="user@company.com"
databricks-oauth-install
```

## What It Does

1. **Every 50 minutes:**
   - Obtains fresh OAuth token from Databricks
   - Verifies token validity (60-minute expiry)
   - Updates `~/.pgpass` file atomically
   - Logs operation details

2. **On system login:**
   - Service starts automatically
   - Performs initial token rotation
   - Schedules next rotation

3. **On errors:**
   - Logs detailed error information
   - Retries on next scheduled rotation
   - Continues running (no crashes)

## Documentation

- **README.md** - Complete documentation (100+ lines)
- **QUICKSTART.md** - 2-minute setup guide
- **CLI --help** - Built-in command help
- **GitHub Issues** - Community support

## Testing

```bash
# Test basic functionality
databricks-oauth-rotator --once

# Test with full config
databricks-oauth-rotator \
  --workspace-url https://workspace.cloud.databricks.com \
  --pg-host instance.database.cloud.databricks.com \
  --pg-username user@company.com \
  --once

# Check logs
tail -f ~/.databricks_oauth_rotator.log
```

## Success Metrics

✅ Package installable via `pip install git+https://...`
✅ All CLI commands work correctly
✅ Service installs on macOS (LaunchAgent)
✅ Service installs on Linux (systemd)
✅ OAuth M2M authentication works
✅ Databricks CLI authentication works
✅ .pgpass file updates atomically
✅ Logging works with rotation
✅ Background service starts automatically
✅ Token rotation succeeds

## Repository

- **URL:** https://github.com/suryasai87/oauth_auto_token_rotation
- **License:** Apache 2.0
- **Language:** Python 3.8+
- **Platform:** macOS, Linux
- **Status:** Public ✅

## Next Steps for Users

1. Install: `pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git`
2. Configure: Set environment variables or use CLI args
3. Test: `databricks-oauth-rotator --once`
4. Install service: `databricks-oauth-install`
5. Verify: `databricks-oauth-status`
6. Monitor: `tail -f ~/.databricks_oauth_rotator.log`

## Support

- **Issues:** https://github.com/suryasai87/oauth_auto_token_rotation/issues
- **Documentation:** https://github.com/suryasai87/oauth_auto_token_rotation#readme
- **Quick Start:** https://github.com/suryasai87/oauth_auto_token_rotation/blob/main/QUICKSTART.md

---

**Package Version:** 1.0.0
**Python Required:** 3.8+
**Dependencies:** PyJWT, requests
**Platforms:** macOS, Linux
**License:** Apache 2.0
