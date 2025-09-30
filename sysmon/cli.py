#!/usr/bin/env python3
"""
CloudCurio SysMon CLI - Command Line Interface for System Monitoring Tool

This CLI provides an interface to the system monitoring and configuration tracking tool.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root.parent))

from sysmon.sysmon import SysMon, EventType


def main():
    parser = argparse.ArgumentParser(
        description="CloudCurio SysMon - System Monitoring and Configuration Tracking Tool"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Start system monitoring")
    monitor_parser.add_argument(
        "--continuous", "-c",
        action="store_true",
        help="Run monitoring continuously in the foreground"
    )
    
    # Snapshot command
    snapshot_parser = subparsers.add_parser("snapshot", help="Create a configuration snapshot")
    snapshot_parser.add_argument(
        "name", 
        nargs="?",
        help="Name for the snapshot (default: auto-generated)"
    )
    
    # List snapshots command
    list_snapshots_parser = subparsers.add_parser("list-snapshots", help="List all configuration snapshots")
    
    # Reproduce command
    reproduce_parser = subparsers.add_parser("reproduce", help="Generate reproduction script from snapshot")
    reproduce_parser.add_argument("snapshot_name", help="Name of the snapshot to reproduce")
    reproduce_parser.add_argument("output_script", help="Output path for the reproduction script")
    
    # Events command
    events_parser = subparsers.add_parser("events", help="Show recent system events")
    events_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=20,
        help="Number of events to show (default: 20)"
    )
    events_parser.add_argument(
        "--type", "-t",
        type=str,
        help="Filter events by type"
    )
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup SysMon configuration")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize SysMon
    sysmon = SysMon()
    
    # Run the appropriate command
    if args.command == "monitor":
        if args.continuous:
            print("Starting continuous monitoring (Press Ctrl+C to stop)...")
            sysmon.start_monitoring()
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping monitoring...")
                sysmon.stop_monitoring()
        else:
            print("Checking for recent changes...")
            sysmon.command_tracker.check_for_changes()
            print("System state checked and updated.")
    
    elif args.command == "snapshot":
        try:
            snapshot_path = sysmon.create_configuration_snapshot(args.name)
            print(f"Configuration snapshot created: {snapshot_path}")
        except Exception as e:
            print(f"Error creating snapshot: {e}")
    
    elif args.command == "list-snapshots":
        snapshot_dir = Path.home() / ".cloudcurio" / "snapshots"
        if snapshot_dir.exists():
            snapshots = [d for d in snapshot_dir.iterdir() if d.is_dir()]
            if snapshots:
                print("Available snapshots:")
                for snapshot in sorted(snapshots, key=os.path.getctime, reverse=True):
                    ctime = os.path.getctime(snapshot)
                    from datetime import datetime
                    print(f"  - {snapshot.name} (created: {datetime.fromtimestamp(ctime)})")
            else:
                print("No snapshots found.")
        else:
            print("No snapshots directory found.")
    
    elif args.command == "reproduce":
        try:
            script_path = sysmon.generate_reproduction_script(args.snapshot_name, args.output_script)
            print(f"Reproduction script generated: {script_path}")
            print("IMPORTANT: Review the script before running it, as it may make significant system changes.")
        except Exception as e:
            print(f"Error generating reproduction script: {e}")
    
    elif args.command == "events":
        try:
            events = sysmon.get_recent_events(limit=args.limit)
            if args.type:
                events = [e for e in events if e.event_type.value == args.type]
            
            if events:
                print(f"Recent system events (limit: {args.limit}):")
                print("-" * 80)
                for event in events:
                    print(f"{event.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {event.event_type.value:15} | {event.source:12} | {event.details}")
            else:
                print("No events found.")
        except Exception as e:
            print(f"Error retrieving events: {e}")
    
    elif args.command == "setup":
        print("Setting up CloudCurio SysMon...")
        
        # Create the config directory
        config_dir = Path.home() / ".cloudcurio"
        config_dir.mkdir(exist_ok=True)
        print(f"Configuration directory created: {config_dir}")
        
        # Create initial snapshot
        print("Creating initial configuration snapshot...")
        snapshot_path = sysmon.create_configuration_snapshot("initial_setup")
        print(f"Initial snapshot created: {snapshot_path}")
        
        print("Setup complete!")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()