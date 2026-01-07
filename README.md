# System Health & Integrity Monitor

A Python-based system monitoring tool that collects and logs comprehensive system health metrics. Designed for operational awareness and system integrity monitoring with a focus on defensive monitoring practices.

## Features

- **System Metrics Collection**
  - CPU usage (overall and per-core)
  - Memory utilization (RAM and swap)
  - Disk usage across all mounted partitions

- **Process Enumeration**
  - Complete process inventory
  - Top processes by CPU and memory usage
  - Process status summary

- **Network Monitoring**
  - Active network connections
  - Listening ports identification
  - Network interface statistics
  - Connection summaries by protocol and status

- **Flexible Output**
  - JSON format for automated parsing
  - Human-readable text reports
  - Timestamped log files

- **Cross-Platform Support**
  - Windows
  - Linux
  - macOS

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/system-health-monitor.git
cd system-health-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the monitor with default settings (JSON output to current directory):
```bash
python monitor.py
```

### Command Line Options

```
Options:
  -h, --help            Show help message and exit
  -o, --output-dir DIR  Directory to write log files (default: current directory)
  -f, --format FORMAT   Output format: json or text (default: json)
  -t, --top-processes N Number of top processes to include (default: 20)
  -a, --all-connections Include all network connections (not just summary)
  -v, --version         Show version information
```

### Examples

**Generate a text report:**
```bash
python monitor.py --format text
```

**Save to specific directory with top 50 processes:**
```bash
python monitor.py --output-dir /var/log/health --top-processes 50
```

**Include detailed network connections:**
```bash
python monitor.py --all-connections
```

**Combine multiple options:**
```bash
python monitor.py --format text --output-dir ./logs --top-processes 30 --all-connections
```

### Elevated Privileges

Some system metrics may require elevated privileges:

**Linux/macOS:**
```bash
sudo python monitor.py
```

**Windows:**
Run Command Prompt or PowerShell as Administrator, then execute the script.

## Output Format

### JSON Output

The JSON output includes structured data organized into sections:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "system_info": {
    "hostname": "workstation",
    "platform": "Linux",
    "os_version": "Linux 5.15.0"
  },
  "metrics": {
    "cpu": { ... },
    "memory": { ... },
    "disk": { ... }
  },
  "processes": {
    "summary": { ... },
    "top_processes_by_memory": [ ... ],
    "top_processes_by_cpu": [ ... ]
  },
  "network": {
    "summary": { ... },
    "interfaces": { ... }
  }
}
```

### Text Output

The text output provides a human-readable report with clearly formatted sections:

```
================================================================================
SYSTEM HEALTH & INTEGRITY MONITOR REPORT
================================================================================
Timestamp: 2024-01-15T10:30:45.123456
Hostname: workstation
Platform: Linux
...
```

## Project Structure

```
system-health-monitor/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── monitor.py                # CLI entry point
└── health_monitor/           # Main package
    ├── __init__.py           # Package initialization
    ├── collector.py          # Main orchestration
    ├── metrics.py            # CPU, memory, disk collection
    ├── processes.py          # Process enumeration
    ├── network.py            # Network monitoring
    └── logger.py             # Output formatting and logging
```

## Use Cases

### Operational Awareness
- Baseline system health snapshots
- Pre/post-maintenance validation
- System performance documentation

### Security Monitoring
- Process inventory for anomaly detection
- Network connection auditing
- Resource usage monitoring

### System Administration
- Capacity planning data collection
- Troubleshooting support
- System state documentation

### Education & Training
- Understanding system monitoring concepts
- Learning Python systems programming
- Exploring cross-platform system APIs

## Technical Details

### Dependencies

- **psutil**: Cross-platform library for system and process utilities
  - CPU, memory, disk, and network metrics
  - Process enumeration and management
  - Cross-platform compatibility layer

### Data Collection

- **CPU Metrics**: 1-second sampling interval for accurate measurements
- **Process Information**: Snapshot of all accessible processes at runtime
- **Network Connections**: Current active connections (IPv4 and IPv6)
- **Disk Usage**: All mounted and accessible partitions

### Platform-Specific Notes

**Windows:**
- Administrator privileges required for complete network connection details
- Some process information may be restricted by Windows security

**Linux:**
- Root privileges required for all network connection PIDs
- Most metrics available to regular users
- Virtual filesystems (proc, sys) are excluded from disk metrics

**macOS:**
- Most metrics available without elevated privileges
- Network connection details may be limited for non-root users

## Development

### Running from Source

```bash
# Install in development mode
pip install -e .

# Run the monitor
python monitor.py
```

### Extending the Tool

The modular architecture makes it easy to add new monitoring capabilities:

1. Create a new module in `health_monitor/`
2. Implement collection functions
3. Import and integrate in `collector.py`
4. Update `__init__.py` exports

## Troubleshooting

### Permission Errors

If you encounter permission errors:
- Run with elevated privileges (sudo/admin)
- Some metrics require higher access levels
- Network connection details especially may need elevated privileges

### Missing Dependencies

If psutil is not installed:
```bash
pip install psutil
```

### Platform-Specific Issues

- **Windows**: Ensure Python is in your PATH
- **Linux**: May need `python3` instead of `python`
- **macOS**: Xcode command line tools may be required

## License

MIT License - See LICENSE file for details

## Author

GDMS Intern Project - Demonstrating systems engineering and operational awareness

## Contributing

This is an educational project, but contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

Built with [psutil](https://github.com/giampaolo/psutil) - A cross-platform library for system and process monitoring
