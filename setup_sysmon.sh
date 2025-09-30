#!/bin/bash

# CloudCurio SysMon Setup Script

set -e  # Exit on any error

echo "Setting up CloudCurio SysMon - System Monitoring Tool..."

# Create the main config directory
CONFIG_DIR="$HOME/.cloudcurio"
mkdir -p "$CONFIG_DIR"

echo "Configuration directory created at: $CONFIG_DIR"

# Create database file with proper permissions
DB_FILE="$CONFIG_DIR/sysmon.db"
touch "$DB_FILE"
chmod 600 "$DB_FILE"

echo "Database file created at: $DB_FILE"

# Create snapshots directory
SNAPSHOTS_DIR="$CONFIG_DIR/snapshots"
mkdir -p "$SNAPSHOTS_DIR"

echo "Snapshots directory created at: $SNAPSHOTS_DIR"

# Create logs directory
LOGS_DIR="$CONFIG_DIR/logs"
mkdir -p "$LOGS_DIR"

echo "Logs directory created at: $LOGS_DIR"

# Create the bin directory if it doesn't exist
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# Copy the executable scripts to the bin directory
cp "$PWD/cloudcurio-sysmon" "$BIN_DIR/"
chmod +x "$BIN_DIR/cloudcurio-sysmon"

echo "SysMon launcher installed to: $BIN_DIR/cloudcurio-sysmon"

# Create a symlink to make it easier to use
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "Note: $BIN_DIR is not in your PATH."
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Create the systemd user service directory
SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_DIR"

# Copy the systemd service file
cp "$PWD/sysmon/cloudcurio-sysmon.service" "$SYSTEMD_DIR/"
echo "Systemd service file copied to: $SYSTEMD_DIR/cloudcurio-sysmon.service"

echo ""
echo "Creating initial configuration snapshot..."
./sysmon/cli.py setup

echo ""
echo "==========================================="
echo "CloudCurio SysMon Setup Complete!"
echo "==========================================="
echo ""
echo "Usage:"
echo "  cloudcurio-sysmon setup            # Initial setup"
echo "  cloudcurio-sysmon snapshot         # Create a configuration snapshot"
echo "  cloudcurio-sysmon list-snapshots   # List all snapshots"
echo "  cloudcurio-sysmon events           # Show recent system events"
echo "  cloudcurio-sysmon monitor          # Monitor for changes once"
echo "  cloudcurio-sysmon monitor --continuous  # Monitor continuously"
echo "  cloudcurio-sysmon reproduce <snapshot_name> <output_script>  # Generate reproduction script"
echo ""
echo "To run the monitor as a service:"
echo "  systemctl --user daemon-reload"
echo "  systemctl --user enable cloudcurio-sysmon.service"
echo "  systemctl --user start cloudcurio-sysmon.service"
echo ""
echo "Your configuration snapshots are stored in: $SNAPSHOTS_DIR"
echo "The event database is at: $DB_FILE"
echo ""