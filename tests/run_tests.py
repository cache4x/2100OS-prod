#!/usr/bin/env python3
"""
Test runner for 2100OS Automation System

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py unit         # Run unit tests only
    python run_tests.py integration  # Run integration tests only
    python run_tests.py --verbose    # Run with verbose output
"""

import sys
import os
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def run_tests(test_type='all', verbose=False):
    """Run tests based on type."""

    # Discover tests
    loader = unittest.TestLoader()

    if test_type == 'unit':
        suite = loader.discover('tests/unit', pattern='test_*.py')
        print("Running unit tests...")
    elif test_type == 'integration':
        suite = loader.discover('tests/integration', pattern='test_*.py')
        print("Running integration tests...")
    elif test_type == 'performance':
        suite = loader.discover('tests/performance', pattern='test_*.py')
        print("Running performance tests...")
    else:
        suite = loader.discover('tests', pattern='test_*.py')
        print("Running all tests...")

    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


def main():
    """Main entry point."""

    # Parse arguments
    args = sys.argv[1:]
    test_type = 'all'
    verbose = False

    for arg in args:
        if arg in ['unit', 'integration', 'performance']:
            test_type = arg
        elif arg in ['-v', '--verbose']:
            verbose = True
        elif arg in ['-h', '--help']:
            print(__doc__)
            return 0

    # Run tests
    exit_code = run_tests(test_type, verbose)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
