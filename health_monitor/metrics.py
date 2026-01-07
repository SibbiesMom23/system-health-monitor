"""
System metrics collection module.
Collects CPU, memory, and disk usage statistics.
"""

import psutil
from typing import Dict, Any


def collect_cpu_metrics() -> Dict[str, Any]:
    """
    Collect CPU usage metrics.

    Returns:
        Dictionary containing CPU metrics including:
        - cpu_percent: Overall CPU usage percentage
        - cpu_count_logical: Number of logical CPUs
        - cpu_count_physical: Number of physical CPUs
        - cpu_per_core: List of per-core usage percentages
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_per_core": psutil.cpu_percent(interval=1, percpu=True)
    }


def collect_memory_metrics() -> Dict[str, Any]:
    """
    Collect memory usage metrics.

    Returns:
        Dictionary containing memory metrics including:
        - total: Total physical memory in bytes
        - available: Available memory in bytes
        - used: Used memory in bytes
        - percent: Memory usage percentage
        - swap_total: Total swap memory in bytes
        - swap_used: Used swap memory in bytes
        - swap_percent: Swap usage percentage
    """
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent,
        "total_gb": round(mem.total / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent
    }


def collect_disk_metrics() -> Dict[str, Any]:
    """
    Collect disk usage metrics for all mounted partitions.

    Returns:
        Dictionary containing disk metrics for each partition including:
        - mountpoint: Mount point path
        - total: Total disk space in bytes
        - used: Used disk space in bytes
        - free: Free disk space in bytes
        - percent: Disk usage percentage
    """
    partitions = psutil.disk_partitions()
    disk_info = {}

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.mountpoint] = {
                "device": partition.device,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2)
            }
        except (PermissionError, OSError):
            # Skip partitions we can't access
            continue

    return disk_info


def collect_all_metrics() -> Dict[str, Any]:
    """
    Collect all system metrics (CPU, memory, disk).

    Returns:
        Dictionary containing all system metrics organized by category
    """
    return {
        "cpu": collect_cpu_metrics(),
        "memory": collect_memory_metrics(),
        "disk": collect_disk_metrics()
    }
