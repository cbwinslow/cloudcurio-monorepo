#!/bin/bash

# CloudCurio Tabby Terminal Setup Script

set -e  # Exit on any error

echo "Setting up CloudCurio Tabby Terminal Configuration..."

# Create the Tabby config directory if it doesn't exist
TABBY_CONFIG_DIR="$HOME/.tabby"
mkdir -p "$TABBY_CONFIG_DIR"

# Copy the Tabby configuration to the proper location
TABBY_CONFIG_FILE="$TABBY_CONFIG_DIR/config.json"
CLOUDCURIO_TABBY_CONFIG="./terminal_tools/tabby_config.json"

if [ -f "$CLOUDCURIO_TABBY_CONFIG" ]; then
    echo "Copying Tabby configuration to $TABBY_CONFIG_FILE..."
    cp "$CLOUDCURIO_TABBY_CONFIG" "$TABBY_CONFIG_FILE"
    
    # Replace placeholder API keys with actual values from environment
    if [ ! -z "$TABBY_API_KEY" ]; then
        sed -i.bak "s/{TABBY_API_KEY_PLACEHOLDER}/$TABBY_API_KEY/g" "$TABBY_CONFIG_FILE"
    fi
    
    if [ ! -z "$OPENAI_API_KEY" ]; then
        sed -i.bak "s/{AI_API_KEY_PLACEHOLDER}/$OPENAI_API_KEY/g" "$TABBY_CONFIG_FILE"
    fi
    
    echo "Tabby configuration updated with API keys"
else
    echo "Warning: Tabby configuration file not found at $CLOUDCURIO_TABBY_CONFIG"
    echo "Please ensure the configuration file exists."
fi

# Create SSH config directory if it doesn't exist
SSH_CONFIG_DIR="$HOME/.ssh"
mkdir -p "$SSH_CONFIG_DIR"

# Set proper permissions for SSH directory
chmod 700 "$SSH_CONFIG_DIR"

# Create a sample SSH config for CloudCurio
SSH_CONFIG_FILE="$SSH_CONFIG_DIR/cloudcurio_config"

cat << 'EOF' > "$SSH_CONFIG_FILE"
# CloudCurio SSH Configuration

# CloudCurio Development Server
Host cloudcurio-dev
    HostName your-dev-server.com
    User your-username
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

# CloudCurio Production Server
Host cloudcurio-prod
    HostName your-prod-server.com
    User your-username
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Example additional servers
Host work-server
    HostName work.example.com
    User work-username
    Port 22
    IdentityFile ~/.ssh/work_key
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

echo "SSH configuration created at $SSH_CONFIG_FILE"

# Append to the main SSH config
if [ -f "$SSH_CONFIG_DIR/config" ]; then
    # Check if CloudCurio config is already included
    if ! grep -q "cloudcurio_config" "$SSH_CONFIG_DIR/config"; then
        echo "" >> "$SSH_CONFIG_DIR/config"
        echo "# Include CloudCurio SSH configurations" >> "$SSH_CONFIG_DIR/config"
        echo "Include cloudcurio_config" >> "$SSH_CONFIG_DIR/config"
    fi
else
    # Create a new SSH config file
    echo "# Include CloudCurio SSH configurations" >> "$SSH_CONFIG_DIR/config"
    echo "Include cloudcurio_config" >> "$SSH_CONFIG_DIR/config"
fi

# Set proper permissions for SSH files
chmod 600 "$SSH_CONFIG_FILE"
chmod 600 "$SSH_CONFIG_DIR/config"

echo "SSH configuration updated to include CloudCurio settings"

# Create a script to launch Tabby with CloudCurio settings
TABBY_LAUNCHER="$HOME/.local/bin/cloudcurio-terminal"
mkdir -p "$HOME/.local/bin"

cat << 'EOF' > "$TABBY_LAUNCHER"
#!/bin/bash
# Launcher script for CloudCurio Tabby Terminal

# Setup environment variables for CloudCurio
export TABBY_CONFIG_PATH="$HOME/.tabby/config.json"

# Launch Tabby terminal
if command -v tabby &> /dev/null; then
    tabby "$@"
elif [ -f "/Applications/Tabby.app/Contents/MacOS/Tabby" ]; then
    # macOS default installation
    /Applications/Tabby.app/Contents/MacOS/Tabby "$@"
elif [ -f "$HOME/Applications/Tabby.app/Contents/MacOS/Tabby" ]; then
    # macOS user installation
    "$HOME/Applications/Tabby.app/Contents/MacOS/Tabby" "$@"
elif [ -f "/opt/Tabby/tabby" ]; then
    # Linux default installation
    /opt/Tabby/tabby "$@"
elif [ -f "$HOME/tabby/tabby" ]; then
    # Linux user installation
    "$HOME/tabby/tabby" "$@"
else
    echo "Error: Tabby terminal not found."
    echo "Please install Tabby from https://eugeny.github.io/tabby/"
    exit 1
fi
EOF

chmod +x "$TABBY_LAUNCHER"

echo "Tabby terminal launcher created at $TABBY_LAUNCHER"
echo "You can now launch Tabby with 'cloudcurio-terminal' command"

# Create a systemd service file for Tabby (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SYSTEMD_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SYSTEMD_DIR"
    
    cat << 'EOF' > "$SYSTEMD_DIR/tabby.service"
[Unit]
Description=CloudCurio Tabby Terminal
After=network.target

[Service]
Type=forking
ExecStart=/usr/bin/tabby
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF
    
    echo "Systemd service file created for Tabby (Linux only)"
    echo "Enable with: systemctl --user enable tabby.service"
fi

echo "Tabby terminal setup completed!"
echo ""
echo "Next steps:"
echo "1. Install Tabby terminal from: https://eugeny.github.io/tabby/"
echo "2. If you have a Tabby API key, set it in your environment: export TABBY_API_KEY=your_key_here"
echo "3. Launch Tabby with your CloudCurio configuration using: cloudcurio-terminal"