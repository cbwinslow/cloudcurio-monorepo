"""
CloudCurio SysMon - System Monitoring and Configuration Tracking Tool

This tool monitors system changes, tracks executed commands,
captures configuration snapshots, and provides tools for system reproduction.
"""

import os
import sys
import json
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import sqlite3
import re
import logging
from dataclasses import dataclass, asdict
from enum import Enum


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of system events that can be monitored"""
    PACKAGE_INSTALL = "package_install"
    PACKAGE_REMOVE = "package_remove"
    PACKAGE_UPGRADE = "package_upgrade"
    SERVICE_START = "service_start"
    SERVICE_STOP = "service_stop"
    SERVICE_RESTART = "service_restart"
    CONFIG_CHANGE = "config_change"
    COMMAND_EXECUTION = "command_execution"
    FILE_CHANGE = "file_change"
    PROCESS_START = "process_start"
    PROCESS_STOP = "process_stop"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    NETWORK_ACTIVITY = "network_activity"
    REPO_ADD = "repo_add"
    REPO_REMOVE = "repo_remove"


@dataclass
class SystemEvent:
    """Represents a system event to be tracked"""
    event_type: EventType
    timestamp: datetime
    source: str  # Where the event came from (e.g., "apt", "systemd", "user")
    details: Dict[str, Any]  # Additional details about the event
    user: str  # User who initiated the event
    command: Optional[str] = None  # Command that triggered the event if applicable


class DatabaseManager:
    """Manages the SQLite database for storing system events"""
    
    def __init__(self, db_path: str = "~/.cloudcurio/sysmon.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    source TEXT NOT NULL,
                    details TEXT NOT NULL,  -- JSON string
                    user TEXT NOT NULL,
                    command TEXT
                )
            ''')
            
            # Create indexed timestamps for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_type ON events(event_type)')
            
            conn.commit()
    
    def insert_event(self, event: SystemEvent):
        """Insert an event into the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (event_type, timestamp, source, details, user, command)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                event.event_type.value,
                event.timestamp.isoformat(),
                event.source,
                json.dumps(event.details),
                event.user,
                event.command
            ))
            
            conn.commit()
    
    def get_events(self, limit: int = 100, offset: int = 0) -> List[SystemEvent]:
        """Retrieve events from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT event_type, timestamp, source, details, user, command
                FROM events
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            events = []
            for row in cursor.fetchall():
                event = SystemEvent(
                    event_type=EventType(row[0]),
                    timestamp=datetime.fromisoformat(row[1]),
                    source=row[2],
                    details=json.loads(row[3]),
                    user=row[4],
                    command=row[5]
                )
                events.append(event)
            
            return events


class CommandTracker:
    """Tracks executed commands and identifies system changes"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.previous_packages = self._get_current_packages()
        self.previous_services = self._get_current_services()
        self.previous_repos = self._get_current_repos()
    
    def _get_current_packages(self) -> set:
        """Get currently installed packages"""
        try:
            # This works for Debian/Ubuntu systems
            result = subprocess.run(['dpkg', '--get-selections'], 
                                  capture_output=True, text=True, check=True)
            packages = set()
            for line in result.stdout.split('\n'):
                if '\tinstall' in line:
                    package = line.split()[0]
                    if ':' in package:  # Architecture-specific package names
                        package = package.split(':')[0]
                    packages.add(package)
            return packages
        except subprocess.CalledProcessError:
            # Fallback for other systems
            try:
                # For Red Hat/CentOS/Fedora
                result = subprocess.run(['rpm', '-qa'], 
                                      capture_output=True, text=True, check=True)
                return set(result.stdout.strip().split('\n'))
            except subprocess.CalledProcessError:
                # For Arch Linux
                try:
                    result = subprocess.run(['pacman', '-Q'], 
                                          capture_output=True, text=True, check=True)
                    return {line.split()[0] for line in result.stdout.strip().split('\n') if line}
                except subprocess.CalledProcessError:
                    return set()  # Return empty if no package manager found
    
    def _get_current_services(self) -> set:
        """Get currently enabled services"""
        try:
            result = subprocess.run(['systemctl', 'list-unit-files', '--state=enabled', '--type=service'], 
                                  capture_output=True, text=True, check=True)
            services = set()
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if '.service' in line:
                    service = line.split()[0]
                    services.add(service)
            return services
        except subprocess.CalledProcessError:
            return set()
    
    def _get_current_repos(self) -> set:
        """Get currently configured repositories"""
        repos = set()
        
        # For Debian/Ubuntu
        if Path('/etc/apt/sources.list').exists():
            with open('/etc/apt/sources.list', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        repos.add(line.strip())
        
        # Check additional sources
        apt_sources_dir = Path('/etc/apt/sources.list.d/')
        if apt_sources_dir.exists():
            for file_path in apt_sources_dir.glob('*.list'):
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            repos.add(line.strip())
        
        return repos
    
    def detect_package_changes(self):
        """Detect package installation/removal since last check"""
        current_packages = self._get_current_packages()
        previous_packages = self.previous_packages
        
        # Find newly installed packages
        new_packages = current_packages - previous_packages
        for pkg in new_packages:
            event = SystemEvent(
                event_type=EventType.PACKAGE_INSTALL,
                timestamp=datetime.now(),
                source="package_manager",
                details={"package": pkg},
                user=os.getenv("USER", "unknown")
            )
            self.db_manager.insert_event(event)
        
        # Find removed packages
        removed_packages = previous_packages - current_packages
        for pkg in removed_packages:
            event = SystemEvent(
                event_type=EventType.PACKAGE_REMOVE,
                timestamp=datetime.now(),
                source="package_manager",
                details={"package": pkg},
                user=os.getenv("USER", "unknown")
            )
            self.db_manager.insert_event(event)
        
        self.previous_packages = current_packages
    
    def detect_service_changes(self):
        """Detect service changes since last check"""
        current_services = self._get_current_services()
        previous_services = self.previous_services
        
        # Find newly enabled services
        new_services = current_services - previous_services
        for service in new_services:
            event = SystemEvent(
                event_type=EventType.SERVICE_START,
                timestamp=datetime.now(),
                source="systemd",
                details={"service": service},
                user=os.getenv("USER", "unknown")
            )
            self.db_manager.insert_event(event)
        
        # Find disabled services
        removed_services = previous_services - current_services
        for service in removed_services:
            event = SystemEvent(
                event_type=EventType.SERVICE_STOP,
                timestamp=datetime.now(),
                source="systemd",
                details={"service": service},
                user=os.getenv("USER", "unknown")
            )
            self.db_manager.insert_event(event)
        
        self.previous_services = current_services
    
    def detect_repo_changes(self):
        """Detect repository changes since last check"""
        current_repos = self._get_current_repos()
        previous_repos = self.previous_repos
        
        # Find newly added repositories
        new_repos = current_repos - previous_repos
        for repo in new_repos:
            event = SystemEvent(
                event_type=EventType.REPO_ADD,
                timestamp=datetime.now(),
                source="apt",
                details={"repository": repo},
                user=os.getenv("USER", "unknown")
            )
            self.db_manager.insert_event(event)
        
        # Find removed repositories
        removed_repos = previous_repos - current_repos
        for repo in removed_repos:
            event = SystemEvent(
                event_type=EventType.REPO_REMOVE,
                timestamp=datetime.now(),
                source="apt",
                details={"repository": repo},
                user=os.getenv("USER", "unknown")
            )
            self.db_manager.insert_event(event)
        
        self.previous_repos = current_repos
    
    def check_for_changes(self):
        """Check for all types of changes since last check"""
        self.detect_package_changes()
        self.detect_service_changes()
        self.detect_repo_changes()


class LogAggregator:
    """Aggregates system logs from various sources"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.log_sources = {
            '/var/log/syslog': self._parse_syslog,
            '/var/log/messages': self._parse_messages,
            '/var/log/auth.log': self._parse_auth_log,
            '/var/log/dpkg.log': self._parse_dpkg_log,
            '/var/log/apt/history.log': self._parse_apt_history,
        }
        self.last_positions = self._init_last_positions()
    
    def _init_last_positions(self) -> Dict[str, int]:
        """Initialize last read positions for log files"""
        positions = {}
        for log_path in self.log_sources.keys():
            path = Path(log_path)
            if path.exists():
                positions[str(path)] = path.stat().st_size
            else:
                positions[str(path)] = 0
        return positions
    
    def _parse_syslog(self, line: str) -> Optional[SystemEvent]:
        """Parse a line from syslog"""
        # Look for package manager activity
        if 'apt' in line.lower() or 'dpkg' in line.lower():
            if 'install' in line.lower():
                match = re.search(r'install\s+(\S+)', line)
                if match:
                    return SystemEvent(
                        event_type=EventType.PACKAGE_INSTALL,
                        timestamp=datetime.now(),  # In real implementation, parse from log
                        source="syslog",
                        details={"package": match.group(1)},
                        user="system"
                    )
        return None
    
    def _parse_auth_log(self, line: str) -> Optional[SystemEvent]:
        """Parse a line from auth log"""
        # Look for authentication events
        if 'session opened' in line.lower():
            # Extract user from line - this is simplified
            user_match = re.search(r'USER=(\w+)', line) or re.search(r'user (\w+)', line, re.IGNORECASE)
            if user_match:
                return SystemEvent(
                    event_type=EventType.USER_LOGIN,
                    timestamp=datetime.now(),
                    source="auth_log",
                    details={"method": "session_open"},
                    user=user_match.group(1)
                )
        elif 'session closed' in line.lower():
            return SystemEvent(
                event_type=EventType.USER_LOGOUT,
                timestamp=datetime.now(),
                source="auth_log",
                details={"method": "session_close"},
                user="unknown"
            )
        return None
    
    def _parse_dpkg_log(self, line: str) -> Optional[SystemEvent]:
        """Parse a line from dpkg log"""
        if 'install' in line.lower():
            match = re.search(r'install\s+(\S+)', line)
            if match:
                return SystemEvent(
                    event_type=EventType.PACKAGE_INSTALL,
                    timestamp=datetime.now(),
                    source="dpkg_log",
                    details={"package": match.group(1)},
                    user="system"
                )
        elif 'remove' in line.lower():
            match = re.search(r'remove\s+(\S+)', line)
            if match:
                return SystemEvent(
                    event_type=EventType.PACKAGE_REMOVE,
                    timestamp=datetime.now(),
                    source="dpkg_log",
                    details={"package": match.group(1)},
                    user="system"
                )
        return None
    
    def _parse_apt_history(self, line: str) -> Optional[SystemEvent]:
        """Parse a line from apt history log"""
        if 'Commandline' in line:
            cmd = line.replace('Commandline:', '').strip()
            if 'install' in cmd:
                packages = re.findall(r'(\S+)', cmd.split('install')[1].strip())
                for pkg in packages:
                    return SystemEvent(
                        event_type=EventType.PACKAGE_INSTALL,
                        timestamp=datetime.now(),
                        source="apt_history",
                        details={"package": pkg},
                        user="system",
                        command=cmd
                    )
            elif 'remove' in cmd or 'purge' in cmd:
                packages = re.findall(r'(\S+)', cmd.split('remove')[1].strip()) if 'remove' in cmd else re.findall(r'(\S+)', cmd.split('purge')[1].strip())
                for pkg in packages:
                    return SystemEvent(
                        event_type=EventType.PACKAGE_REMOVE,
                        timestamp=datetime.now(),
                        source="apt_history",
                        details={"package": pkg},
                        user="system",
                        command=cmd
                    )
        return None
    
    def _parse_messages(self, line: str) -> Optional[SystemEvent]:
        """Parse a line from messages log"""
        # Generic message parsing
        return None  # Add specific parsing as needed
    
    def aggregate_logs(self):
        """Read new entries from log files and process them"""
        for log_path_str, parser in self.log_sources.items():
            log_path = Path(log_path_str)
            if not log_path.exists():
                continue
            
            current_size = log_path.stat().st_size
            last_pos = self.last_positions.get(str(log_path), 0)
            
            if current_size > last_pos:
                # New data available
                with open(log_path, 'r') as f:
                    f.seek(last_pos)
                    new_lines = f.readlines()
                
                for line in new_lines:
                    event = parser(line.strip())
                    if event:
                        self.db_manager.insert_event(event)
                
                # Update last read position
                self.last_positions[str(log_path)] = current_size


class ConfigurationSnapshot:
    """Captures and manages system configuration snapshots"""
    
    def __init__(self):
        self.snapshot_dir = Path.home() / ".cloudcurio" / "snapshots"
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    def create_snapshot(self, name: str = None) -> str:
        """Create a new configuration snapshot"""
        if name is None:
            name = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        snapshot_path = self.snapshot_dir / name
        snapshot_path.mkdir(exist_ok=True)
        
        # Capture installed packages
        self._capture_packages(snapshot_path)
        
        # Capture installed services
        self._capture_services(snapshot_path)
        
        # Capture repository configuration
        self._capture_repositories(snapshot_path)
        
        # Capture system-wide configurations
        self._capture_system_configs(snapshot_path)
        
        # Capture user configurations
        self._capture_user_configs(snapshot_path)
        
        logger.info(f"Configuration snapshot created: {snapshot_path}")
        return str(snapshot_path)
    
    def _capture_packages(self, snapshot_path: Path):
        """Capture list of installed packages"""
        packages_path = snapshot_path / "packages.json"
        
        # Get packages from different package managers
        packages = {
            "apt": [],
            "rpm": [],
            "pacman": [],
            "pip": [],
            "npm": [],
            "snap": [],
            "flatpak": []
        }
        
        try:
            # Get apt packages
            result = subprocess.run(['dpkg', '--get-selections'], 
                                  capture_output=True, text=True, check=True)
            packages['apt'] = [line.split()[0] for line in result.stdout.split('\n') if '\tinstall' in line]
        except subprocess.CalledProcessError:
            pass  # apt not available
        
        try:
            # Get rpm packages
            result = subprocess.run(['rpm', '-qa'], 
                                  capture_output=True, text=True, check=True)
            packages['rpm'] = [pkg for pkg in result.stdout.strip().split('\n') if pkg]
        except subprocess.CalledProcessError:
            pass  # rpm not available
        
        try:
            # Get pacman packages
            result = subprocess.run(['pacman', '-Q'], 
                                  capture_output=True, text=True, check=True)
            packages['pacman'] = [line.split()[0] for line in result.stdout.split('\n') if line.strip()]
        except subprocess.CalledProcessError:
            pass  # pacman not available
        
        try:
            # Get pip packages
            result = subprocess.run(['pip', 'list', '--format', 'freeze'], 
                                  capture_output=True, text=True, check=True)
            packages['pip'] = [line for line in result.stdout.strip().split('\n') if line and not line.startswith('#')]
        except subprocess.CalledProcessError:
            pass  # pip not available
        
        try:
            # Get npm global packages
            result = subprocess.run(['npm', 'list', '-g', '--depth=0', '--json'], 
                                  capture_output=True, text=True, check=True)
            npm_data = json.loads(result.stdout)
            packages['npm'] = list(npm_data['dependencies'].keys()) if 'dependencies' in npm_data else []
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            pass  # npm not available or json invalid
        
        # Get snap packages
        try:
            result = subprocess.run(['snap', 'list'], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            packages['snap'] = [line.split()[0] for line in lines if line.strip()]
        except subprocess.CalledProcessError:
            pass  # snap not available
        
        # Get flatpak packages
        try:
            result = subprocess.run(['flatpak', 'list', '--app'], 
                                  capture_output=True, text=True, check=True)
            packages['flatpak'] = [line.split()[0] for line in result.stdout.strip().split('\n') if line.strip()]
        except subprocess.CalledProcessError:
            pass  # flatpak not available
        
        # Save packages to JSON
        with open(packages_path, 'w') as f:
            json.dump(packages, f, indent=2)
    
    def _capture_services(self, snapshot_path: Path):
        """Capture enabled services"""
        services_path = snapshot_path / "services.json"
        
        services = {
            "systemd_enabled": [],
            "systemd_disabled": [],
            "systemd_masked": []
        }
        
        try:
            # Get enabled services
            result = subprocess.run(['systemctl', 'list-unit-files', '--type=service', '--state=enabled'], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            services['systemd_enabled'] = [line.split()[0] for line in lines if line.strip()]
        except subprocess.CalledProcessError:
            pass  # systemctl not available
        
        try:
            # Get disabled services
            result = subprocess.run(['systemctl', 'list-unit-files', '--type=service', '--state=disabled'], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            services['systemd_disabled'] = [line.split()[0] for line in lines if line.strip()]
        except subprocess.CalledProcessError:
            pass  # systemctl not available
        
        try:
            # Get masked services
            result = subprocess.run(['systemctl', 'list-unit-files', '--type=service', '--state=masked'], 
                                  capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            services['systemd_masked'] = [line.split()[0] for line in lines if line.strip()]
        except subprocess.CalledProcessError:
            pass  # systemctl not available
        
        # Save services to JSON
        with open(services_path, 'w') as f:
            json.dump(services, f, indent=2)
    
    def _capture_repositories(self, snapshot_path: Path):
        """Capture configured repositories"""
        repos_path = snapshot_path / "repositories.json"
        
        repos = {
            "apt_sources": [],
            "apt_keys": []
        }
        
        # Get apt sources
        apt_sources_dir = Path('/etc/apt/sources.list.d/')
        if apt_sources_dir.exists():
            for file_path in apt_sources_dir.glob('*.list'):
                with open(file_path, 'r') as f:
                    repos['apt_sources'].extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
        
        # Get main sources list
        main_sources = Path('/etc/apt/sources.list')
        if main_sources.exists():
            with open(main_sources, 'r') as f:
                repos['apt_sources'].extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
        
        # Get apt keys (simplified)
        try:
            result = subprocess.run(['apt-key', 'list'], capture_output=True, text=True, check=True)
            # Extract key fingerprints - simplified approach
            repos['apt_keys'] = [line.strip() for line in result.stdout.split('\n') if 'pub' in line or 'sub' in line]
        except subprocess.CalledProcessError:
            pass  # apt-key might not be available
        
        # Save repositories to JSON
        with open(repos_path, 'w') as f:
            json.dump(repos, f, indent=2)
    
    def _capture_system_configs(self, snapshot_path: Path):
        """Capture important system configuration files"""
        configs_dir = snapshot_path / "system_configs"
        configs_dir.mkdir(exist_ok=True)
        
        # List of important system config files to capture
        system_configs = [
            '/etc/hostname',
            '/etc/hosts',
            '/etc/fstab',
            '/etc/ssh/sshd_config',
            '/etc/ssh/ssh_config',
            '/etc/environment',
            '/etc/default/grub',
            '/etc/sysctl.conf',
            '/etc/security/limits.conf',
            '/etc/passwd',
            '/etc/group',
            '/etc/shadow',
            '/etc/gshadow',
            '/etc/crontab',
            '/etc/timezone',
            '/etc/localtime',
            '/etc/resolv.conf',
            '/etc/hosts',
        ]
        
        for config_path in system_configs:
            path = Path(config_path)
            if path.exists():
                dest_path = configs_dir / path.name
                try:
                    # For security files like /etc/shadow, we'll just record their existence
                    if path.name in ['shadow', 'gshadow']:
                        with open(dest_path, 'w') as f:
                            f.write(f"File exists: {path}\n")
                    else:
                        # For regular config files, copy the content
                        with open(path, 'r') as src, open(dest_path, 'w') as dst:
                            dst.write(src.read())
                except PermissionError:
                    # Skip files we don't have permission to read
                    with open(dest_path, 'w') as f:
                        f.write(f"Permission denied: {path}\n")
    
    def _capture_user_configs(self, snapshot_path: Path):
        """Capture user configuration files"""
        configs_dir = snapshot_path / "user_configs"
        configs_dir.mkdir(exist_ok=True)
        
        # List of important user config files to capture
        user_configs = [
            '~/.bashrc',
            '~/.bash_profile',
            '~/.zshrc',
            '~/.profile',
            '~/.gitconfig',
            '~/.vimrc',
            '~/.ssh/config',
            '~/.config/fish/config.fish',
            '~/.tmux.conf',
            '~/.screenrc',
            '~/.inputrc',
            '~/.curlrc',
            '~/.wgetrc',
        ]
        
        for config_path in user_configs:
            path = Path(config_path).expanduser()
            if path.exists():
                # Create destination path preserving directory structure
                relative_path = path.relative_to(Path.home())
                dest_path = configs_dir / relative_path
                
                # Create parent directories if they don't exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    # Copy the content
                    with open(path, 'r') as src, open(dest_path, 'w') as dst:
                        dst.write(src.read())
                except PermissionError:
                    # Skip files we don't have permission to read
                    with open(dest_path, 'w') as f:
                        f.write(f"Permission denied: {path}\n")


class ReproductionEngine:
    """Generates scripts to reproduce system configuration"""
    
    def __init__(self, snapshot_path: str):
        self.snapshot_path = Path(snapshot_path)
    
    def generate_bash_script(self, output_path: str) -> str:
        """Generate a bash script to reproduce the configuration"""
        output_path = Path(output_path)
        
        with open(output_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Generated by CloudCurio SysMon - System Reproduction Script\n")
            f.write("# This script will attempt to reproduce the system configuration\n")
            f.write("\nset -e  # Exit on any error\n")
            f.write("\necho 'Starting system reproduction...'\n")
            
            # Add packages section
            packages_path = self.snapshot_path / "packages.json"
            if packages_path.exists():
                with open(packages_path) as pkg_file:
                    packages = json.load(pkg_file)
                
                f.write("\n# Installing packages\n")
                
                # Install apt packages if any
                if packages.get('apt'):
                    f.write("echo 'Installing apt packages...'\n")
                    f.write("sudo apt update\n")
                    pkg_list = ' '.join(packages['apt'])
                    f.write(f"sudo apt install -y {pkg_list}\n")
                
                # Install pip packages if any
                if packages.get('pip'):
                    f.write("echo 'Installing pip packages...'\n")
                    for pkg in packages['pip']:
                        f.write(f"pip install {pkg.split('==')[0]}\n")  # Use package name without version
                
                # Install npm packages if any
                if packages.get('npm'):
                    f.write("echo 'Installing npm packages...'\n")
                    for pkg in packages['npm']:
                        f.write(f"sudo npm install -g {pkg}\n")
                
                # Install snap packages if any
                if packages.get('snap'):
                    f.write("echo 'Installing snap packages...'\n")
                    for pkg in packages['snap']:
                        f.write(f"sudo snap install {pkg}\n")
                
                # Install flatpak packages if any
                if packages.get('flatpak'):
                    f.write("echo 'Installing flatpak packages...'\n")
                    for pkg in packages['flatpak']:
                        f.write(f"flatpak install flathub {pkg}\n")
            
            # Add services section
            services_path = self.snapshot_path / "services.json"
            if services_path.exists():
                with open(services_path) as svc_file:
                    services = json.load(svc_file)
                
                f.write("\n# Enabling services\n")
                
                # Enable systemd services
                for service in services.get('systemd_enabled', []):
                    f.write(f"sudo systemctl enable {service}\n")
                    f.write(f"sudo systemctl start {service}\n")
            
            # Add repository section
            repos_path = self.snapshot_path / "repositories.json"
            if repos_path.exists():
                with open(repos_path) as repo_file:
                    repos = json.load(repo_file)
                
                f.write("\n# Adding repositories\n")
                
                # Add apt repositories
                for repo in repos.get('apt_sources', []):
                    f.write(f"echo '{repo}' | sudo tee -a /etc/apt/sources.list.d/cloudcurio.list\n")
                
                f.write("sudo apt update\n")
            
            # Add user configuration files
            user_configs_dir = self.snapshot_path / "user_configs"
            if user_configs_dir.exists():
                f.write("\n# Restoring user configuration files\n")
                
                for config_file in user_configs_dir.rglob('*'):
                    if config_file.is_file():
                        relative_path = config_file.relative_to(user_configs_dir)
                        dest_path = Path.home() / relative_path
                        f.write(f"mkdir -p {dest_path.parent}\n")
                        f.write(f"cp '{config_file}' '{dest_path}'\n")
            
            f.write("\necho 'System reproduction complete!'\n")
            f.write("echo 'Some services may need to be restarted manually.'\n")
        
        # Make the script executable
        output_path.chmod(0o755)
        
        return str(output_path)


class SysMon:
    """Main class for the System Monitoring Tool"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.command_tracker = CommandTracker(self.db_manager)
        self.log_aggregator = LogAggregator(self.db_manager)
        self.config_snapshot = ConfigurationSnapshot()
        self.monitoring = False
    
    def start_monitoring(self):
        """Start monitoring the system"""
        self.monitoring = True
        logger.info("Starting system monitoring...")
        
        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring the system"""
        self.monitoring = False
        logger.info("Stopping system monitoring...")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Check for changes in packages, services, repos
                self.command_tracker.check_for_changes()
                
                # Aggregate log data
                self.log_aggregator.aggregate_logs()
                
                # Sleep before next check
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Wait a bit before retrying
    
    def get_recent_events(self, limit: int = 50) -> List[SystemEvent]:
        """Get recent system events"""
        return self.db_manager.get_events(limit=limit)
    
    def create_configuration_snapshot(self, name: str = None) -> str:
        """Create a configuration snapshot"""
        return self.config_snapshot.create_snapshot(name)
    
    def generate_reproduction_script(self, snapshot_name: str, output_path: str) -> str:
        """Generate a script to reproduce a configuration snapshot"""
        snapshot_path = self.config_snapshot.snapshot_dir / snapshot_name
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot {snapshot_name} does not exist")
        
        engine = ReproductionEngine(str(snapshot_path))
        return engine.generate_bash_script(output_path)


# Example usage and testing
if __name__ == "__main__":
    print("CloudCurio SysMon - System Monitoring and Configuration Tracking Tool")
    
    # Initialize the system monitor
    sysmon = SysMon()
    
    # Create a snapshot
    print("Creating initial configuration snapshot...")
    snapshot_path = sysmon.create_configuration_snapshot()
    print(f"Snapshot created: {snapshot_path}")
    
    # Try to generate a reproduction script (optional)
    try:
        script_path = sysmon.create_configuration_snapshot()
        print(f"Reproduction script would be generated at: {script_path}")
    except Exception as e:
        print(f"Could not generate reproduction script: {e}")
    
    print("Initialization complete. To start continuous monitoring, use sysmon.start_monitoring()")