#!/usr/bin/env python3
"""
CloudCurio Release Management Script

This script handles versioning, tagging, and releasing of CloudCurio packages.
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path


def get_current_version():
    """Get current version from setup.py or pyproject.toml"""
    # Try setup.py first
    setup_py = Path("setup.py")
    if setup_py.exists():
        with open(setup_py, "r") as f:
            content = f.read()
            # Look for version in setup.py
            import re
            match = re.search(r'version="([^"]+)"', content)
            if match:
                return match.group(1)
    
    # Try pyproject.toml
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        import toml
        data = toml.load(pyproject)
        if "tool" in data and "poetry" in data["tool"] and "version" in data["tool"]["poetry"]:
            return data["tool"]["poetry"]["version"]
    
    # Default version
    return "1.0.0"


def update_version_in_file(file_path, old_version, new_version):
    """Update version in a specific file"""
    with open(file_path, "r") as f:
        content = f.read()
    
    # Replace version (be specific to avoid replacing other numbers)
    updated_content = content.replace(f'version="{old_version}"', f'version="{new_version}"')
    
    if updated_content != content:
        with open(file_path, "w") as f:
            f.write(updated_content)
        print(f"Updated version in {file_path}")
        return True
    return False


def bump_version(current_version, part="patch"):
    """Bump version (major.minor.patch)"""
    major, minor, patch = map(int, current_version.split("."))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    
    return f"{major}.{minor}.{patch}"


def create_git_tag(version):
    """Create a git tag for the version"""
    try:
        # Create annotated tag
        result = subprocess.run([
            "git", "tag", "-a", f"v{version}", "-m", f"Release version {version}"
        ], capture_output=True, text=True, check=True)
        print(f"Created git tag v{version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating git tag: {e}")
        return False


def push_tag_to_remote(tag_name, remote="origin"):
    """Push the tag to remote repository"""
    try:
        result = subprocess.run([
            "git", "push", remote, tag_name
        ], capture_output=True, text=True, check=True)
        print(f"Pushed tag {tag_name} to {remote}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error pushing tag: {e}")
        return False


def generate_changelog(version, previous_version=None):
    """Generate a changelog for the release"""
    try:
        if previous_version:
            result = subprocess.run([
                "git", "log", f"v{previous_version}..HEAD", "--oneline"
            ], capture_output=True, text=True, check=True)
        else:
            result = subprocess.run([
                "git", "log", "--oneline"
            ], capture_output=True, text=True, check=True)
        
        commits = result.stdout.strip().split('\n')
        
        changelog = f"## CloudCurio v{version} - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        changelog += "### Features\n"
        features = [c for c in commits if any(keyword in c.lower() for keyword in ['feat:', 'feature:', 'add:', 'implement:'])]
        for commit in features:
            changelog += f"- {commit}\n"
        
        changelog += "\n### Bug Fixes\n"
        fixes = [c for c in commits if any(keyword in c.lower() for keyword in ['fix:', 'bug:', 'patch:'])]
        for commit in fixes:
            changelog += f"- {commit}\n"
        
        changelog += "\n### Other Changes\n"
        others = [c for c in commits if c not in features and c not in fixes and c.strip()]
        for commit in others:
            changelog += f"- {commit}\n"
        
        return changelog
    except subprocess.CalledProcessError as e:
        print(f"Error generating changelog: {e}")
        return f"## CloudCurio v{version} - {datetime.now().strftime('%Y-%m-%d')}\n\nChangelog generation failed."


def update_changelog_file(new_content):
    """Update the CHANGELOG.md file"""
    changelog_path = Path("CHANGELOG.md")
    
    if changelog_path.exists():
        with open(changelog_path, "r") as f:
            existing_content = f.read()
        new_content = new_content + "\n\n" + existing_content
    
    with open(changelog_path, "w") as f:
        f.write(new_content)
    
    print("Updated CHANGELOG.md")


def run_tests():
    """Run tests before releasing"""
    try:
        result = subprocess.run([
            "python", "-m", "pytest", "tests/", "-v"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("All tests passed!")
            return True
        else:
            print("Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def build_packages():
    """Build pip and Docker packages"""
    try:
        # Build pip package
        result = subprocess.run([
            "python", "-m", "build"
        ], capture_output=True, text=True, check=True)
        print("Built pip package")
        
        # Build Docker images
        result = subprocess.run([
            "docker", "build", "-f", "Dockerfile.mcp", "-t", f"cbwinslow/cloudcurio-mcp:latest", "."
        ], capture_output=True, text=True)
        if result.returncode == 0:
            print("Built Docker image")
        else:
            print("Docker build failed, but continuing...")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building packages: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="CloudCurio Release Management")
    parser.add_argument("action", choices=["version", "bump", "release", "changelog"], 
                       help="Action to perform")
    parser.add_argument("--part", choices=["major", "minor", "patch"], default="patch",
                       help="Version part to bump (for bump action)")
    parser.add_argument("--version", help="Specific version to use")
    parser.add_argument("--skip-tests", action="store_true", 
                       help="Skip running tests before release")
    parser.add_argument("--skip-build", action="store_true", 
                       help="Skip building packages before release")
    
    args = parser.parse_args()
    
    if args.action == "version":
        current_version = get_current_version()
        print(f"Current version: {current_version}")
    
    elif args.action == "bump":
        current_version = get_current_version()
        new_version = bump_version(current_version, args.part)
        print(f"Bumped version: {current_version} -> {new_version}")
        
        # Update version in setup.py
        update_version_in_file("setup.py", current_version, new_version)
        
        # Git operations
        try:
            subprocess.run(["git", "add", "setup.py"], check=True)
            subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
            print(f"Committed version bump: {new_version}")
        except subprocess.CalledProcessError as e:
            print(f"Error committing version bump: {e}")
    
    elif args.action == "release":
        current_version = args.version or get_current_version()
        print(f"Preparing to release version: {current_version}")
        
        if not args.skip_tests:
            print("Running tests...")
            if not run_tests():
                print("Tests failed. Release aborted.")
                return 1
        
        if not args.skip_build:
            print("Building packages...")
            if not build_packages():
                print("Build failed. Release aborted.")
                return 1
        
        # Create git tag
        if not create_git_tag(current_version):
            print("Failed to create git tag. Release aborted.")
            return 1
        
        # Push tag to remote
        if not push_tag_to_remote(f"v{current_version}"):
            print("Failed to push git tag. Release aborted.")
            return 1
        
        # Generate and update changelog
        changelog = generate_changelog(current_version)
        update_changelog_file(changelog)
        
        print(f"Successfully released version: {current_version}")
        print(f"Tag created: v{current_version}")
        print(f"Changelog updated in CHANGELOG.md")
        
        # Update version to next development version
        next_version = bump_version(current_version, "patch")
        update_version_in_file("setup.py", current_version, next_version)
        print(f"Updated development version to: {next_version}")
    
    elif args.action == "changelog":
        current_version = get_current_version()
        changelog = generate_changelog(current_version)
        print(changelog)


if __name__ == "__main__":
    sys.exit(main() or 0)