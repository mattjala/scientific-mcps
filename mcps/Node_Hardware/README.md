# Node Hardware MCP - System Monitoring for LLMs


## Description

Node Hardware MCP is a Model Context Protocol server that enables LLMs to monitor and analyze system hardware information including CPU specifications, memory usage, disk performance, network interfaces, GPU details, and sensor data for both local and remote nodes via SSH connections, providing comprehensive hardware monitoring and performance analysis capabilities.


## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- SSH client (for remote node capabilities)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "node-hardware-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

```json
"mcp": {
  "servers": {
    "node-hardware-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add node-hardware-mcp -- uvx iowarp-mcps node-hardware
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "node-hardware-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "node-hardware"]
    }
  }
}
```

</details>

<details>
<summary><b>Manual Setup</b></summary>

**Linux/macOS:**
```bash
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Node_Hardware run node-hardware-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Node_Hardware run node-hardware-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Node_Hardware run node-hardware-mcp --help
```

</details>

## Capabilities

### `get_cpu_info`
**Description**: Get comprehensive CPU information including specifications, core count, frequency, architecture, and performance metrics with intelligent analysis and optimization recommendations.

**Parameters**: None required

**Returns**: Complete CPU specifications with architecture details, performance metrics, utilization analysis, and optimization insights.

### `get_memory_info`
**Description**: Analyze system memory including total, available, used memory, swap information, and performance metrics with intelligent memory usage analysis and optimization recommendations.

**Parameters**: None required

**Returns**: Comprehensive memory analysis with usage statistics, performance metrics, and memory optimization recommendations.

### `get_system_info`
**Description**: Get detailed system information including operating system, kernel version, hostname, uptime, and system configuration with comprehensive system health analysis.

**Parameters**: None required

**Returns**: Complete system information with configuration details, uptime analysis, and system health assessment.

### `get_disk_info`
**Description**: Analyze disk storage including capacity, usage, file systems, and I/O performance metrics with intelligent storage analysis and optimization recommendations.

**Parameters**: None required

**Returns**: Comprehensive disk analysis with storage usage, I/O performance, and storage optimization insights.

### `get_network_info`
**Description**: Get network interface information including IP addresses, bandwidth, traffic statistics, and performance metrics with network analysis and optimization recommendations.

**Parameters**: None required

**Returns**: Complete network analysis with interface details, traffic statistics, and network performance insights.

### `get_gpu_info`
**Description**: Analyze GPU hardware including specifications, memory, utilization, and performance metrics with intelligent GPU analysis for machine learning and computational workloads.

**Parameters**: None required

**Returns**: Comprehensive GPU information with specifications, utilization metrics, and performance optimization recommendations.

### `get_sensor_info`
**Description**: Monitor system sensors including temperature, fan speeds, voltage, and thermal management with intelligent thermal analysis and system health monitoring.

**Parameters**: None required

**Returns**: Complete sensor data with thermal analysis, cooling efficiency, and system health recommendations.

### `get_process_info`
**Description**: Analyze running processes including CPU usage, memory consumption, and performance metrics with intelligent process analysis and resource optimization insights.

**Parameters**: None required

**Returns**: Comprehensive process analysis with resource usage, performance metrics, and optimization recommendations.

### `get_performance_info`
**Description**: Get detailed performance metrics including CPU load, memory pressure, I/O statistics, and system bottleneck analysis with intelligent performance optimization recommendations.

**Parameters**: None required

**Returns**: Complete performance analysis with bottleneck identification, efficiency metrics, and optimization strategies.

### `get_remote_node_info`
**Description**: Monitor remote system hardware via SSH connection with comprehensive component analysis, performance monitoring, and intelligent insights for distributed system management.

**Parameters**:
- `hostname` (str): Remote host IP address or hostname
- `username` (str): SSH username for authentication
- `password` (str, optional): SSH password (use key-based auth when possible)
- `port` (int, optional): SSH port (default: 22)
- `components` (list, optional): Specific components to monitor

**Returns**: Complete remote hardware analysis with component details, performance metrics, and comparative insights.

### `health_check`
**Description**: Perform comprehensive system health check with capability verification, diagnostic assessment, and intelligent system analysis for monitoring tool validation and system reliability.

**Parameters**: None required

**Returns**: Complete health assessment with system status, capability verification, diagnostic insights, and maintenance recommendations.

## Examples

### 1. Local Hardware Overview
```
I need a comprehensive overview of my local system's hardware including CPU, memory, disk, and network components.
```

**Tools called:**
- `get_node_info` - Get complete local hardware information with all components
- Components collected: cpu, memory, disk, network, system, summary

### 2. Remote Server Monitoring
```
Monitor the hardware status of a remote server via SSH, focusing on CPU and memory utilization for performance analysis.
```

**Tools called:**
- `get_remote_node_info` - Connect to remote host with SSH authentication
- Components collected: cpu, memory, performance, system

### 3. GPU and Thermal Monitoring
```
Check GPU specifications and thermal sensors on both local and remote systems for machine learning workloads.
```

**Tools called:**
- `get_node_info` - Local GPU and sensor monitoring  
- `get_remote_node_info` - Remote GPU and thermal analysis
- Components collected: gpu, sensors, performance

### 4. System Health Assessment
```
Perform a comprehensive health check of system capabilities and verify all monitoring tools are working correctly.
```

**Tools called:**
- `health_check` - System health verification and diagnostic assessment
- `get_node_info` - Comprehensive local system analysis with health metrics

### 5. Performance Bottleneck Analysis  
```
Identify performance bottlenecks on a production server by analyzing CPU, memory, disk I/O, and running processes.
```

**Tools called:**
- `get_remote_node_info` - Remote performance analysis via SSH
- Components collected: cpu, memory, disk, performance, processes

### 6. Storage and Network Analysis
```
Analyze storage health and network interface performance on multiple systems for infrastructure monitoring.
```

**Tools called:**
- `get_node_info` - Local storage and network analysis
- `get_remote_node_info` - Remote storage and network monitoring  
- Components collected: disk, network, system, summary

