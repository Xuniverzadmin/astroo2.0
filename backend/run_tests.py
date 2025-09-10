#!/usr/bin/env python3
"""
Test runner script for the numerology application.

This script provides an easy way to run tests with different configurations
and generate coverage reports.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print("Make sure pytest is installed: pip install pytest pytest-cov")
        return False


def run_unit_tests():
    """Run unit tests only."""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_panchangam_core.py::TestPanchangamCore",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests only."""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_panchangam_core.py::TestPanchangamIntegration",
        "tests/test_health_endpoints.py::TestHealthEndpointIntegration",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "Integration Tests")


def run_health_tests():
    """Run health endpoint tests only."""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_health_endpoints.py",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "Health Endpoint Tests")


def run_all_tests():
    """Run all tests."""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "All Tests")


def run_tests_with_coverage():
    """Run tests with coverage report."""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=numerology_app",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
        "-v"
    ]
    return run_command(cmd, "Tests with Coverage")


def run_specific_test(test_path):
    """Run a specific test file or test function."""
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, f"Specific Test: {test_path}")


def run_fast_tests():
    """Run only fast tests (exclude slow tests)."""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-m", "not slow",
        "-v",
        "--tb=short"
    ]
    return run_command(cmd, "Fast Tests Only")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests for the numerology application")
    parser.add_argument(
        "test_type",
        choices=[
            "unit", "integration", "health", "all", "coverage", 
            "fast", "specific"
        ],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--test-path",
        help="Specific test path (required for 'specific' test type)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("🧪 Numerology Application Test Runner")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    success = False
    
    if args.test_type == "unit":
        success = run_unit_tests()
    elif args.test_type == "integration":
        success = run_integration_tests()
    elif args.test_type == "health":
        success = run_health_tests()
    elif args.test_type == "all":
        success = run_all_tests()
    elif args.test_type == "coverage":
        success = run_tests_with_coverage()
    elif args.test_type == "fast":
        success = run_fast_tests()
    elif args.test_type == "specific":
        if not args.test_path:
            print("❌ --test-path is required for 'specific' test type")
            sys.exit(1)
        success = run_specific_test(args.test_path)
    
    if success:
        print(f"\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
