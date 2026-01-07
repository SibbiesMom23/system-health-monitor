"""
Main health collector orchestration module.
Coordinates collection of all system health metrics.
"""

from typing import Dict, Any
from .metrics import collect_all_metrics
from .processes import collect_process_info
from .network import collect_network_info
from .logger import HealthLogger


class HealthCollector:
    """Main collector class that orchestrates all health monitoring."""

    def __init__(self,
                 top_processes: int = 20,
                 include_all_connections: bool = False,
                 output_dir: str = ".",
                 output_format: str = "json"):
        """
        Initialize the health collector.

        Args:
            top_processes: Number of top processes to include in report
            include_all_connections: If True, include all network connections
            output_dir: Directory to write log files
            output_format: Output format ('json' or 'text')
        """
        self.top_processes = top_processes
        self.include_all_connections = include_all_connections
        self.logger = HealthLogger(output_dir=output_dir, format=output_format)

    def collect_all(self) -> Dict[str, Any]:
        """
        Collect all system health metrics.

        Returns:
            Dictionary containing all collected metrics
        """
        print("Collecting system metrics...")
        metrics = collect_all_metrics()

        print("Enumerating processes...")
        processes = collect_process_info(top_n=self.top_processes)

        print("Analyzing network connections...")
        network = collect_network_info(include_all_connections=self.include_all_connections)

        return {
            "metrics": metrics,
            "processes": processes,
            "network": network
        }

    def run(self) -> str:
        """
        Run the health collector and write results to log file.

        Returns:
            Path to the generated log file
        """
        print("Starting System Health & Integrity Monitor...")
        print("-" * 60)

        # Collect all data
        data = self.collect_all()

        # Write to log
        print("\nWriting results to log file...")
        log_file = self.logger.write_log(data)

        print(f"\nHealth monitoring complete!")
        print(f"Report saved to: {log_file}")
        print("-" * 60)

        return log_file
