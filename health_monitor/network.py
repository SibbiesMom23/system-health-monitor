"""
Network connections monitoring module.
Collects information about active network connections and network interfaces.
"""

import psutil
from typing import List, Dict, Any
from collections import defaultdict


def collect_network_connections() -> List[Dict[str, Any]]:
    """
    Collect information about all active network connections.

    Returns:
        List of dictionaries containing connection information including:
        - fd: File descriptor
        - family: Address family (AF_INET, AF_INET6)
        - type: Socket type (SOCK_STREAM, SOCK_DGRAM)
        - local_address: Local IP address
        - local_port: Local port
        - remote_address: Remote IP address
        - remote_port: Remote port
        - status: Connection status
        - pid: Process ID owning the connection
    """
    connections = []

    try:
        for conn in psutil.net_connections(kind='inet'):
            try:
                connections.append({
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "local_address": conn.laddr.ip if conn.laddr else "N/A",
                    "local_port": conn.laddr.port if conn.laddr else "N/A",
                    "remote_address": conn.raddr.ip if conn.raddr else "N/A",
                    "remote_port": conn.raddr.port if conn.raddr else "N/A",
                    "status": conn.status,
                    "pid": conn.pid or "N/A"
                })
            except (AttributeError, psutil.AccessDenied):
                continue
    except psutil.AccessDenied:
        # May need elevated privileges on some systems
        pass

    return connections


def get_network_summary() -> Dict[str, Any]:
    """
    Get a summary of network connections grouped by status.

    Returns:
        Dictionary containing:
        - total_connections: Total number of connections
        - by_status: Count of connections by status
        - by_protocol: Count of connections by protocol
        - listening_ports: List of ports in LISTEN state
    """
    connections = collect_network_connections()

    status_count = defaultdict(int)
    protocol_count = defaultdict(int)
    listening_ports = []

    for conn in connections:
        status_count[conn["status"]] += 1

        # Determine protocol from type
        if "STREAM" in conn["type"]:
            protocol_count["TCP"] += 1
        elif "DGRAM" in conn["type"]:
            protocol_count["UDP"] += 1

        # Collect listening ports
        if conn["status"] == "LISTEN" and conn["local_port"] != "N/A":
            listening_ports.append({
                "port": conn["local_port"],
                "address": conn["local_address"],
                "pid": conn["pid"]
            })

    return {
        "total_connections": len(connections),
        "by_status": dict(status_count),
        "by_protocol": dict(protocol_count),
        "listening_ports": sorted(listening_ports, key=lambda x: x["port"])
    }


def collect_network_interfaces() -> Dict[str, Any]:
    """
    Collect information about network interfaces and their statistics.

    Returns:
        Dictionary containing network interface information including:
        - Interface name as key
        - addresses: List of addresses (IP, netmask, broadcast)
        - stats: Network I/O statistics
    """
    interfaces = {}
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    for interface_name, addr_list in addrs.items():
        interface_info = {
            "addresses": [],
            "is_up": False,
            "speed": 0,
            "mtu": 0
        }

        # Collect addresses
        for addr in addr_list:
            interface_info["addresses"].append({
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast
            })

        # Collect interface stats
        if interface_name in stats:
            stat = stats[interface_name]
            interface_info["is_up"] = stat.isup
            interface_info["speed"] = stat.speed
            interface_info["mtu"] = stat.mtu

        # Collect I/O counters
        if interface_name in io_counters:
            counter = io_counters[interface_name]
            interface_info["io_stats"] = {
                "bytes_sent": counter.bytes_sent,
                "bytes_recv": counter.bytes_recv,
                "packets_sent": counter.packets_sent,
                "packets_recv": counter.packets_recv,
                "errin": counter.errin,
                "errout": counter.errout,
                "dropin": counter.dropin,
                "dropout": counter.dropout
            }

        interfaces[interface_name] = interface_info

    return interfaces


def collect_network_info(include_all_connections: bool = False) -> Dict[str, Any]:
    """
    Collect comprehensive network information.

    Args:
        include_all_connections: If True, include all connections; otherwise just summary

    Returns:
        Dictionary containing network summary, interfaces, and optionally all connections
    """
    info = {
        "summary": get_network_summary(),
        "interfaces": collect_network_interfaces()
    }

    if include_all_connections:
        info["all_connections"] = collect_network_connections()

    return info
