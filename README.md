# Databricks OAuth Auto Token Rotation

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)]()

Automatic OAuth token rotation for Databricks PostgreSQL (Lakebase) connections. Eliminates the need for manual token updates by running as a background service that automatically refreshes OAuth tokens every 50 minutes and updates your `.pgpass` file.

## Features

✅ **Automatic Token Rotation** - Refreshes OAuth tokens every 50 minutes (before 60-minute expiry)
✅ **Zero Downtime** - Atomic `.pgpass` file updates prevent connection interruptions
✅ **Dual Authentication** - Supports both OAuth M2M (production) and CLI (development)
✅ **Background Service** - Runs as macOS LaunchAgent or Linux systemd service
✅ **Comprehensive Logging** - Rotating logs with detailed operation tracking
✅ **Easy Installation** - Simple `pip install` and one-command setup
✅ **Cross-Platform** - Works on macOS and Linux

## Quick Start

### Installation

```bash
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git
```

### Configuration

Set your Databricks workspace and PostgreSQL connection details:

```bash
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_PG_HOST="instance-xyz.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="your-email@company.com"
```

### Test It

Run a test rotation to verify everything works:

```bash
databricks-oauth-rotator --once
```

### Install as Background Service

Install and start the automatic rotation service:

```bash
databricks-oauth-install \
  --workspace-url https://your-workspace.cloud.databricks.com \
  --pg-host instance-xyz.database.cloud.databricks.com \
  --pg-username your-email@company.com
```

That's it! The service will now automatically rotate your OAuth tokens every 50 minutes.

## How It Works

```
┌─────────────────────────────────────┐
│   Background Service (every 50m)    │
└──────────────┬──────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  1. Get fresh OAuth token            │
│     - Try OAuth M2M first            │
│     - Fallback to Databricks CLI     │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  2. Verify token validity (60 min)   │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  3. Update ~/.pgpass atomically      │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  4. Log success and sleep            │
└──────────────────────────────────────┘
```

## Authentication Methods

### Option 1: Databricks CLI (Recommended for Development)

Easiest for personal use - uses browser-based OAuth:

```bash
pip install databricks-cli
databricks auth login --host https://your-workspace.cloud.databricks.com
```

The rotator will automatically use your CLI credentials.

### Option 2: OAuth M2M (Recommended for Production)

Best for automation and production use:

1. Create a service principal in Databricks
2. Generate OAuth secret
3. Set environment variables:

```bash
export DATABRICKS_CLIENT_ID="your-service-principal-id"
export DATABRICKS_CLIENT_SECRET="your-oauth-secret"
```

## Usage

### Command-Line Interface

```bash
# Run once (test mode)
databricks-oauth-rotator --once

# Run as daemon with custom interval
databricks-oauth-rotator --interval 45

# Specify all parameters explicitly
databricks-oauth-rotator \
  --workspace-url https://workspace.cloud.databricks.com \
  --pg-host instance-xyz.database.cloud.databricks.com \
  --pg-username user@company.com \
  --pg-port 5432 \
  --pg-database databricks_postgres \
  --interval 50
```

### Service Management

```bash
# Install service
databricks-oauth-install

# Check service status
databricks-oauth-status

# Restart service
databricks-oauth-restart

# Uninstall service
databricks-oauth-uninstall
```

### Python API

Use the rotator programmatically in your Python code:

```python
from databricks_oauth_rotator import DatabricksOAuthRotator

# Create rotator instance
rotator = DatabricksOAuthRotator(
    workspace_url="https://workspace.cloud.databricks.com",
    pg_host="instance-xyz.database.cloud.databricks.com",
    pg_username="user@company.com",
    rotation_interval=50  # minutes
)

# Run once
rotator.run_once()

# Or run as daemon
rotator.run_daemon()
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABRICKS_HOST` | Workspace URL | Yes |
| `DATABRICKS_PG_HOST` | PostgreSQL hostname | Yes |
| `DATABRICKS_PG_USERNAME` | PostgreSQL username | Yes |
| `DATABRICKS_CLIENT_ID` | OAuth client ID (M2M) | No |
| `DATABRICKS_CLIENT_SECRET` | OAuth client secret (M2M) | No |

### Command-Line Arguments

```
--workspace-url URL        Databricks workspace URL
--pg-host HOST             PostgreSQL hostname
--pg-port PORT             PostgreSQL port (default: 5432)
--pg-database DB           Database name (default: databricks_postgres)
--pg-username USER         PostgreSQL username
--pgpass-file PATH         Path to .pgpass file (default: ~/.pgpass)
--log-file PATH            Log file path (default: ~/.databricks_oauth_rotator.log)
--interval MINUTES         Rotation interval (default: 50)
--once                     Run once and exit (test mode)
```

## Monitoring

### View Logs

```bash
# Follow logs in real-time
tail -f ~/.databricks_oauth_rotator.log

# Check recent activity
tail -50 ~/.databricks_oauth_rotator.log

# Search for errors
grep ERROR ~/.databricks_oauth_rotator.log
```

### Log Format

```
2025-01-22 14:30:00 - INFO - Starting OAuth token rotation cycle
2025-01-22 14:30:01 - INFO - Successfully obtained token via OAuth M2M
2025-01-22 14:30:01 - INFO - New token details:
2025-01-22 14:30:01 - INFO -   - Subject: user@company.com
2025-01-22 14:30:01 - INFO -   - Expires at: 2025-01-22T15:30:01
2025-01-22 14:30:01 - INFO -   - Valid for: 60 minutes
2025-01-22 14:30:01 - INFO - Successfully updated /Users/user/.pgpass
2025-01-22 14:30:01 - INFO - Token rotation completed successfully
```

## Troubleshooting

### Service Not Starting

Check the error logs:

```bash
cat ~/.databricks_oauth_rotator_stderr.log
```

Common issues:
- Missing environment variables
- Python dependencies not installed
- Authentication not configured

### Token Rotation Failing

1. **Verify authentication:**
   ```bash
   # For OAuth M2M
   echo $DATABRICKS_CLIENT_ID
   echo $DATABRICKS_CLIENT_SECRET

   # For CLI
   databricks auth login --host https://your-workspace.cloud.databricks.com
   ```

2. **Test manually:**
   ```bash
   databricks-oauth-rotator --once
   ```

3. **Check logs:**
   ```bash
   tail -100 ~/.databricks_oauth_rotator.log
   ```

### .pgpass Not Updating

1. **Check file permissions:**
   ```bash
   ls -la ~/.pgpass
   # Should be: -rw------- (0600)
   ```

2. **Verify service is running:**
   ```bash
   databricks-oauth-status
   ```

## Architecture

### Components

- **`rotator.py`** - Core rotation logic
- **`cli.py`** - Command-line interface
- **`install.py`** - Service installation and management
- **`templates/`** - LaunchAgent/systemd templates

### Authentication Flow

1. **OAuth M2M Flow** (Production):
   ```
   POST {workspace}/oidc/v1/token
   Authorization: Basic {client_id}:{client_secret}
   Body: grant_type=client_credentials&scope=all-apis
   → Returns: access_token (valid 60 minutes)
   ```

2. **Databricks CLI Flow** (Development):
   ```
   databricks auth token --host {workspace}
   → Uses stored refresh token
   → Returns: access_token (valid 60 minutes)
   ```

### File Updates

The `.pgpass` file is updated atomically to prevent corruption:

1. Write new token to temporary file
2. Set permissions to 0600 (owner read/write only)
3. Atomic rename to `.pgpass`

## Security

- **Short-lived tokens:** Access tokens expire after 60 minutes
- **Proactive rotation:** Tokens rotated at 50 minutes (10-minute safety margin)
- **Secure storage:** `.pgpass` file has restricted permissions (0600)
- **Atomic updates:** Prevents file corruption during updates
- **No credentials in code:** Uses environment variables and OAuth flows

## Platform Support

| Platform | Service Type | Status |
|----------|-------------|--------|
| macOS | LaunchAgent | ✅ Supported |
| Linux | systemd | ✅ Supported |
| Windows | - | ❌ Not yet supported |

## Examples

### Basic Setup (Development)

```bash
# Install package
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git

# Login with Databricks CLI
databricks auth login --host https://workspace.cloud.databricks.com

# Set PostgreSQL details
export DATABRICKS_PG_HOST="instance-xyz.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="user@company.com"

# Test rotation
databricks-oauth-rotator --once

# Install as service
databricks-oauth-install
```

### Production Setup (OAuth M2M)

```bash
# Install package
pip install git+https://github.com/suryasai87/oauth_auto_token_rotation.git

# Set all credentials
export DATABRICKS_HOST="https://workspace.cloud.databricks.com"
export DATABRICKS_CLIENT_ID="service-principal-id"
export DATABRICKS_CLIENT_SECRET="oauth-secret"
export DATABRICKS_PG_HOST="instance-xyz.database.cloud.databricks.com"
export DATABRICKS_PG_USERNAME="user@company.com"

# Add to shell profile (~/.bashrc, ~/.zshrc)
echo 'export DATABRICKS_HOST="..."' >> ~/.zshrc
echo 'export DATABRICKS_CLIENT_ID="..."' >> ~/.zshrc
echo 'export DATABRICKS_CLIENT_SECRET="..."' >> ~/.zshrc
echo 'export DATABRICKS_PG_HOST="..."' >> ~/.zshrc
echo 'export DATABRICKS_PG_USERNAME="..."' >> ~/.zshrc

# Install as service
databricks-oauth-install --interval 50

# Verify it's running
databricks-oauth-status
```

### Custom Configuration

```bash
# Run with all custom settings
databricks-oauth-rotator \
  --workspace-url https://custom-workspace.cloud.databricks.com \
  --client-id abc123 \
  --client-secret xyz789 \
  --pg-host custom-instance.database.cloud.databricks.com \
  --pg-port 5432 \
  --pg-database my_database \
  --pg-username custom@email.com \
  --pgpass-file ~/custom/.pgpass \
  --log-file ~/custom/logs/rotation.log \
  --interval 45
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## References

- [Databricks OAuth M2M Documentation](https://docs.databricks.com/en/dev-tools/auth/oauth-m2m.html)
- [Databricks OAuth U2M Documentation](https://docs.databricks.com/en/dev-tools/auth/oauth-u2m.html)
- [Databricks CLI Authentication](https://docs.databricks.com/en/dev-tools/cli/authentication.html)
- [PostgreSQL .pgpass Documentation](https://www.postgresql.org/docs/current/libpq-pgpass.html)

## Support

For issues, questions, or contributions:
- **Issues:** [GitHub Issues](https://github.com/suryasai87/oauth_auto_token_rotation/issues)
- **Documentation:** [README](https://github.com/suryasai87/oauth_auto_token_rotation#readme)

## Acknowledgments

Built for the Databricks community to simplify PostgreSQL Lakebase OAuth token management.

---

**Made with ❤️ for Databricks users**
