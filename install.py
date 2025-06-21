#!/usr/bin/env python3
"""
Installation script for Terraform Plan Parser

This script handles the installation of the Terraform plan parser
and its dependencies.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True


def install_dependencies():
    """Install required dependencies."""
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    return True


def install_package():
    """Install the package in development mode."""
    if not run_command("pip install -e .", "Installing package"):
        return False
    return True


def install_dev_dependencies():
    """Install development dependencies."""
    dev_deps = ["pytest", "pytest-cov", "black", "flake8"]
    for dep in dev_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            return False
    return True


def run_tests():
    """Run the test suite."""
    if not run_command("python -m pytest tests/ -v", "Running tests"):
        return False
    return True


def main():
    """Main installation function."""
    print("🚀 Terraform Plan Parser Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Install package
    if not install_package():
        print("❌ Failed to install package")
        sys.exit(1)
    
    # Ask if user wants development setup
    dev_setup = input("\n🔧 Install development dependencies? (y/N): ").lower().strip()
    if dev_setup in ['y', 'yes']:
        if not install_dev_dependencies():
            print("❌ Failed to install development dependencies")
            sys.exit(1)
        
        # Run tests
        run_tests_input = input("\n🧪 Run tests? (y/N): ").lower().strip()
        if run_tests_input in ['y', 'yes']:
            if not run_tests():
                print("❌ Tests failed")
                sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\n📖 Usage examples:")
    print("  # Parse a plan file")
    print("  python -m src.main parse plan.json [OPTIONS]")
    print("")
    print("  # Parse with detailed output")
    print("  python -m src.main parse plan.json --detailed")
    print("")
    print("  # Generate and parse a plan")
    print("  python -m src.main generate [OPTIONS]")
    print("")
    print("  # Run demo")
    print("  python examples/demo.py")
    print("")
    print("  # Show help")
    print("  python -m src.main --help")


if __name__ == "__main__":
    main() 