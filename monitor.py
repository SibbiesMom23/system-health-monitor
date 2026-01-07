#!/usr/bin/env python3
"""
System Health & Integrity Monitor - CLI Entry Point

A tool for monitoring system health metrics including CPU, memory, disk usage,
running processes, and network connections.

Usage:
    python monitor.py [options]

Author: GDMS Intern Project
"""

import argparse
import sys
from health_monitor import HealthCollector


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="System Health & Integrity Monitor - Collect and log system health metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (JSON output to current directory)
  python monitor.py

  # Output as human-readable text
  python monitor.py --format text

  # Save to specific directory with top 50 processes
  python monitor.py --output-dir /var/log/health --top-processes 50

  # Include all network connections in report
  python monitor.py --all-connections

  # Combine options
  python monitor.py --format text --output-dir ./logs --top-processes 30
        """
    )

    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="Directory to write log files (default: current directory)"
    )

    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["json", "text"],
        default="json",
        help="Output format: json or text (default: json)"
    )

    parser.add_argument(
        "-t", "--top-processes",
        type=int,
        default=20,
        help="Number of top processes to include in report (default: 20)"
    )

    parser.add_argument(
        "-a", "--all-connections",
        action="store_true",
        help="Include all network connections (not just summary)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="System Health Monitor v1.0.0"
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    try:
        args = parse_arguments()

        # Create and run collector
        collector = HealthCollector(
            top_processes=args.top_processes,
            include_all_connections=args.all_connections,
            output_dir=args.output_dir,
            output_format=args.format
        )

        log_file = collector.run()

        # Display summary
        print(f"\nSummary:")
        print(f"  Format: {args.format.upper()}")
        print(f"  Top Processes: {args.top_processes}")
        print(f"  All Connections: {'Yes' if args.all_connections else 'No'}")
        print(f"  Log File: {log_file}")

        return 0

    except KeyboardInterrupt:
        print("\n\nMonitoring interrupted by user.")
        return 130

    except PermissionError as e:
        print(f"\nPermission Error: {e}", file=sys.stderr)
        print("Note: Some metrics may require elevated privileges (run with sudo/admin).", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
