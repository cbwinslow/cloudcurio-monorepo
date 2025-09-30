# CloudCurio SysMon - System Monitoring and Configuration Tracking Tool

CloudCurio SysMon is a comprehensive system monitoring and configuration tracking tool that captures all changes to your system, including installed packages, services, configurations, and user actions. It allows you to create snapshots of your system configuration and reproduce them on other systems.

## Features

- **Real-time Monitoring**: Tracks system changes as they happen
- **Command Tracking**: Monitors executed commands that modify the system
- **Log Aggregation**: Collects from various system logs (syslog, auth.log, dpkg.log, apt history, etc.)
- **Configuration Snapshots**: Creates complete snapshots of your system configuration
- **Reproduction Engine**: Generates bash scripts to reproduce your system configuration
- **Event Database**: Stores all system events in a SQLite database
- **Bash Completion**: Full bash completion support
- **Systemd Integration**: Can run as a background service

## Installation

1. Run the setup script:
   ```bash
   ./setup_sysmon.sh
   ```

2. Add the binary directory to your PATH (if not already present):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Load bash completion:
   ```bash
   source ./sysmon/cloudcurio-sysmon-completion.bash
   # Or add it to your ~/.bashrc for persistence:
   echo 'source /path/to/cloudcurio/sysmon/cloudcurio-sysmon-completion.bash' >> ~/.bashrc
   ```

## Usage

### Basic Commands

```bash
# Setup initial configuration
cloudcurio-sysmon setup

# Create a configuration snapshot
cloudcurio-sysmon snapshot [snapshot_name]

# List all configuration snapshots
cloudcurio-sysmon list-snapshots

# Show recent system events
cloudcurio-sysmon events [--limit N] [--type event_type]

# Monitor for changes once
cloudcurio-sysmon monitor

# Monitor continuously in foreground
cloudcurio-sysmon monitor --continuous

# Generate reproduction script from a snapshot
cloudcurio-sysmon reproduce <snapshot_name> <output_script_path>
```

### Running as a Service

To run CloudCurio SysMon as a background service:

```bash
# Reload systemd configuration
systemctl --user daemon-reload

# Enable the service (start automatically)
systemctl --user enable cloudcurio-sysmon.service

# Start the service now
systemctl --user start cloudcurio-sysmon.service

# Check service status
systemctl --user status cloudcurio-sysmon.service
```

## Event Types Tracked

CloudCurio SysMon tracks the following system events:

- `package_install`: When a package is installed
- `package_remove`: When a package is removed
- `package_upgrade`: When a package is upgraded
- `service_start`: When a service is started
- `service_stop`: When a service is stopped
- `config_change`: When configuration files are modified
- `command_execution`: When system-modifying commands are executed
- `user_login`: When a user logs in
- `user_logout`: When a user logs out
- `repo_add`: When a repository is added
- `repo_remove`: When a repository is removed

## Reproduction Scripts

The reproduction engine generates comprehensive bash scripts that can recreate your system configuration on another machine. These scripts include:

- Package installations (apt, pip, npm, snap, flatpak)
- Service enabling and starting
- Repository additions
- User configuration file restoration

**Important**: Always review reproduction scripts before running them, as they may make significant system changes.

## Data Storage

- Event database: `~/.cloudcurio/sysmon.db`
- Configuration snapshots: `~/.cloudcurio/snapshots/`
- Logs: `~/.cloudcurio/logs/`

## Contributing

This tool is designed to be extended. Additional log sources, package managers, and system events can be easily added to enhance monitoring capabilities.

## License

This project is part of the CloudCurio suite under the MIT License.