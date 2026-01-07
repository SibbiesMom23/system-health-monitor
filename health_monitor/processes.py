"""
Process enumeration module.
Collects information about running processes on the system.
"""

import psutil
from typing import List, Dict, Any


def enumerate_processes(sort_by: str = "memory", limit: int = None) -> List[Dict[str, Any]]:
    """
    Enumerate all running processes and collect their information.

    Args:
        sort_by: Field to sort processes by ('memory', 'cpu', 'pid', 'name')
        limit: Maximum number of processes to return (None for all)

    Returns:
        List of dictionaries containing process information including:
        - pid: Process ID
        - name: Process name
        - username: User running the process
        - status: Process status (running, sleeping, etc.)
        - cpu_percent: CPU usage percentage
        - memory_percent: Memory usage percentage
        - memory_mb: Memory usage in MB
        - num_threads: Number of threads
        - create_time: Process creation timestamp
    """
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'status',
                                     'cpu_percent', 'memory_percent',
                                     'memory_info', 'num_threads', 'create_time']):
        try:
            pinfo = proc.info
            processes.append({
                "pid": pinfo['pid'],
                "name": pinfo['name'],
                "username": pinfo['username'] or "N/A",
                "status": pinfo['status'],
                "cpu_percent": pinfo['cpu_percent'] or 0.0,
                "memory_percent": round(pinfo['memory_percent'] or 0.0, 2),
                "memory_mb": round(pinfo['memory_info'].rss / (1024**2), 2) if pinfo['memory_info'] else 0,
                "num_threads": pinfo['num_threads'],
                "create_time": pinfo['create_time']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process terminated or we don't have permission
            continue

    # Sort processes
    if sort_by == "memory":
        processes.sort(key=lambda x: x["memory_percent"], reverse=True)
    elif sort_by == "cpu":
        processes.sort(key=lambda x: x["cpu_percent"], reverse=True)
    elif sort_by == "pid":
        processes.sort(key=lambda x: x["pid"])
    elif sort_by == "name":
        processes.sort(key=lambda x: x["name"].lower())

    # Apply limit if specified
    if limit:
        processes = processes[:limit]

    return processes


def get_process_summary() -> Dict[str, Any]:
    """
    Get a high-level summary of running processes.

    Returns:
        Dictionary containing:
        - total_processes: Total number of running processes
        - running: Number of processes in running state
        - sleeping: Number of processes in sleeping state
        - stopped: Number of processes in stopped state
        - zombie: Number of zombie processes
    """
    status_count = {
        "running": 0,
        "sleeping": 0,
        "stopped": 0,
        "zombie": 0,
        "other": 0
    }

    for proc in psutil.process_iter(['status']):
        try:
            status = proc.info['status']
            if status in status_count:
                status_count[status] += 1
            else:
                status_count["other"] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    total = sum(status_count.values())

    return {
        "total_processes": total,
        **status_count
    }


def collect_process_info(top_n: int = 20) -> Dict[str, Any]:
    """
    Collect comprehensive process information.

    Args:
        top_n: Number of top processes to include (by memory usage)

    Returns:
        Dictionary containing process summary and top processes
    """
    return {
        "summary": get_process_summary(),
        "top_processes_by_memory": enumerate_processes(sort_by="memory", limit=top_n),
        "top_processes_by_cpu": enumerate_processes(sort_by="cpu", limit=top_n)
    }
