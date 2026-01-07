"""
Logging utility module.
Handles formatting and writing system health data to log files.
"""

import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class HealthLogger:
    """Logger for system health monitoring data."""

    def __init__(self, output_dir: str = ".", format: str = "json"):
        """
        Initialize the health logger.

        Args:
            output_dir: Directory to write log files to
            format: Output format ('json' or 'text')
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.format = format.lower()

    def generate_filename(self) -> str:
        """
        Generate a timestamped filename for the log.

        Returns:
            Filename string
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = "json" if self.format == "json" else "log"
        return f"health_monitor_{timestamp}.{extension}"

    def format_json(self, data: Dict[str, Any]) -> str:
        """
        Format data as JSON.

        Args:
            data: Data to format

        Returns:
            JSON-formatted string
        """
        return json.dumps(data, indent=2, default=str)

    def format_text(self, data: Dict[str, Any]) -> str:
        """
        Format data as human-readable text.

        Args:
            data: Data to format

        Returns:
            Text-formatted string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("SYSTEM HEALTH & INTEGRITY MONITOR REPORT")
        lines.append("=" * 80)
        lines.append(f"Timestamp: {data['timestamp']}")
        lines.append(f"Hostname: {data['system_info']['hostname']}")
        lines.append(f"Platform: {data['system_info']['platform']}")
        lines.append(f"OS: {data['system_info']['os_version']}")
        lines.append("")

        # CPU Metrics
        lines.append("-" * 80)
        lines.append("CPU METRICS")
        lines.append("-" * 80)
        cpu = data['metrics']['cpu']
        lines.append(f"Overall Usage: {cpu['cpu_percent']}%")
        lines.append(f"Logical CPUs: {cpu['cpu_count_logical']}")
        lines.append(f"Physical CPUs: {cpu['cpu_count_physical']}")
        lines.append(f"Per-Core Usage: {cpu['cpu_per_core']}")
        lines.append("")

        # Memory Metrics
        lines.append("-" * 80)
        lines.append("MEMORY METRICS")
        lines.append("-" * 80)
        mem = data['metrics']['memory']
        lines.append(f"Total: {mem['total_gb']} GB")
        lines.append(f"Available: {mem['available_gb']} GB")
        lines.append(f"Used: {mem['used_gb']} GB ({mem['percent']}%)")
        lines.append(f"Swap Used: {mem['swap_percent']}%")
        lines.append("")

        # Disk Metrics
        lines.append("-" * 80)
        lines.append("DISK METRICS")
        lines.append("-" * 80)
        for mount, disk in data['metrics']['disk'].items():
            lines.append(f"\nMount: {mount}")
            lines.append(f"  Device: {disk['device']}")
            lines.append(f"  Type: {disk['fstype']}")
            lines.append(f"  Total: {disk['total_gb']} GB")
            lines.append(f"  Used: {disk['used_gb']} GB ({disk['percent']}%)")
            lines.append(f"  Free: {disk['free_gb']} GB")
        lines.append("")

        # Process Summary
        lines.append("-" * 80)
        lines.append("PROCESS SUMMARY")
        lines.append("-" * 80)
        proc_summary = data['processes']['summary']
        lines.append(f"Total Processes: {proc_summary['total_processes']}")
        lines.append(f"Running: {proc_summary['running']}")
        lines.append(f"Sleeping: {proc_summary['sleeping']}")
        lines.append(f"Stopped: {proc_summary['stopped']}")
        lines.append(f"Zombie: {proc_summary['zombie']}")
        lines.append("")

        # Top Processes by Memory
        lines.append("-" * 80)
        lines.append("TOP PROCESSES BY MEMORY")
        lines.append("-" * 80)
        lines.append(f"{'PID':<10} {'Name':<30} {'User':<15} {'Memory %':<12} {'Memory MB':<12}")
        lines.append("-" * 80)
        for proc in data['processes']['top_processes_by_memory'][:10]:
            lines.append(
                f"{proc['pid']:<10} {proc['name'][:28]:<30} "
                f"{proc['username'][:13]:<15} {proc['memory_percent']:<12.2f} {proc['memory_mb']:<12.2f}"
            )
        lines.append("")

        # Network Summary
        lines.append("-" * 80)
        lines.append("NETWORK SUMMARY")
        lines.append("-" * 80)
        net_summary = data['network']['summary']
        lines.append(f"Total Connections: {net_summary['total_connections']}")
        lines.append(f"Connections by Status: {net_summary['by_status']}")
        lines.append(f"Connections by Protocol: {net_summary['by_protocol']}")
        lines.append(f"\nListening Ports ({len(net_summary['listening_ports'])}):")
        for port_info in net_summary['listening_ports'][:20]:
            lines.append(f"  Port {port_info['port']}: {port_info['address']} (PID: {port_info['pid']})")
        lines.append("")

        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    def write_log(self, data: Dict[str, Any]) -> str:
        """
        Write health monitoring data to a log file.

        Args:
            data: Complete health monitoring data

        Returns:
            Path to the created log file
        """
        # Add system info and timestamp
        enhanced_data = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "hostname": platform.node(),
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "os_version": f"{platform.system()} {platform.release()}"
            },
            **data
        }

        # Format data
        if self.format == "json":
            content = self.format_json(enhanced_data)
        else:
            content = self.format_text(enhanced_data)

        # Write to file
        filename = self.generate_filename()
        filepath = self.output_dir / filename

        with open(filepath, 'w') as f:
            f.write(content)

        return str(filepath)
