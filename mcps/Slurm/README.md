# Slurm MCP - HPC Job Management for LLMs


## Description

Slurm MCP is a Model Context Protocol server that enables LLMs to manage HPC workloads on Slurm-managed clusters with comprehensive job submission, monitoring, and resource management capabilities, featuring intelligent job scheduling, cluster monitoring, array job support, and interactive node allocation for seamless high-performance computing workflows.


## 🛠️ Installation

### Requirements

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

<details>
<summary><b>Install in Cursor</b></summary>

Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`

Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.

```json
{
  "mcpServers": {
    "slurm-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
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
    "slurm-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add slurm-mcp -- uvx iowarp-mcps slurm
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "slurm-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "slurm"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Slurm run slurm-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Slurm run slurm-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Slurm run slurm-mcp --help
```

</details>

## Capabilities

### `submit_slurm_job`
**Description**: Submit Slurm jobs with comprehensive resource specification and intelligent job optimization. Accepts script files and resource requirements, then submits them to the Slurm scheduler with advanced parameter validation and optimization.

**Parameters**:
- `script_path` (str): Path to the job script file
- `cores` (int): Number of CPU cores to request
- `memory` (str, optional): Memory allocation (e.g., "32GB")
- `time_limit` (str, optional): Maximum job runtime (e.g., "24:00:00")
- `job_name` (str, optional): Custom job name for identification
- `partition` (str, optional): Target partition/queue for job submission

**Returns**: Job submission confirmation with job ID, resource allocation details, and scheduling information.

### `check_job_status`
**Description**: Check comprehensive Slurm job status with advanced monitoring, performance insights, and intelligent analysis. Provides detailed status information with performance metrics and optimization recommendations.

**Parameters**:
- `job_id` (str): Slurm job ID to check status for

**Returns**: Complete job status including state, resource utilization, performance metrics, and queue position analysis.

### `cancel_slurm_job`
**Description**: Cancel running or queued Slurm jobs with comprehensive cleanup and resource management. Provides intelligent job termination with resource cleanup and status verification.

**Parameters**:
- `job_id` (str): Slurm job ID to cancel
- `reason` (str, optional): Cancellation reason for logging and tracking

**Returns**: Cancellation confirmation with cleanup status and resource release information.

### `list_slurm_jobs`
**Description**: List and analyze all Slurm jobs with comprehensive filtering, sorting, and status analysis. Provides detailed job inventory with performance insights and resource utilization metrics.

**Parameters**:
- `user` (str, optional): Filter jobs by specific username
- `state` (str, optional): Filter by job state (RUNNING, PENDING, COMPLETED, etc.)
- `partition` (str, optional): Filter by partition/queue name

**Returns**: Comprehensive job listing with status, resource usage, performance metrics, and queue analysis.

### `get_slurm_info`
**Description**: Get comprehensive Slurm cluster information including node status, resource availability, and system performance metrics with intelligent cluster analysis and optimization insights.

**Parameters**: None required

**Returns**: Complete cluster status including node information, resource availability, queue statistics, and performance analysis.

### `get_job_details`
**Description**: Get detailed information about a specific Slurm job including resource utilization, performance metrics, and comprehensive job lifecycle analysis.

**Parameters**:
- `job_id` (str): Slurm job ID to get detailed information for

**Returns**: Comprehensive job details including resource usage, performance metrics, timing information, and efficiency analysis.

### `get_job_output`
**Description**: Retrieve output files and logs from completed or running Slurm jobs with intelligent log analysis and error detection capabilities.

**Parameters**:
- `job_id` (str): Slurm job ID to retrieve output from
- `output_type` (str, optional): Type of output to retrieve (stdout, stderr, both)

**Returns**: Job output content with log analysis, error detection, and performance insights.

### `get_queue_info`
**Description**: Get comprehensive queue and partition information with intelligent load analysis, performance metrics, and optimization recommendations for job scheduling.

**Parameters**:
- `partition` (str, optional): Specific partition to analyze

**Returns**: Complete queue analysis including load metrics, wait times, resource availability, and scheduling optimization insights.

### `submit_array_job`
**Description**: Submit Slurm array jobs for parallel task execution with intelligent resource distribution and optimization. Supports large-scale parameter sweeps and parallel workflows.

**Parameters**:
- `script_path` (str): Path to the array job script
- `array_spec` (str): Array specification (e.g., "1-100" or "1-100:2")
- `cores_per_task` (int): CPU cores per array task
- `memory_per_task` (str, optional): Memory per array task
- `job_name` (str, optional): Base name for array job

**Returns**: Array job submission confirmation with job IDs, resource allocation, and task distribution details.

### `get_node_info`
**Description**: Get detailed information about cluster nodes including hardware specifications, resource availability, and performance metrics with intelligent node analysis.

**Parameters**:
- `node_name` (str, optional): Specific node to analyze

**Returns**: Comprehensive node information including hardware specs, resource usage, performance metrics, and availability status.

### `allocate_slurm_nodes`
**Description**: Allocate compute nodes for interactive sessions with intelligent resource selection and optimization. Provides dedicated node access for development and analysis.

**Parameters**:
- `nodes` (int): Number of nodes to allocate
- `cores_per_node` (int, optional): CPU cores per node
- `memory_per_node` (str, optional): Memory per node
- `time_limit` (str, optional): Allocation duration
- `partition` (str, optional): Target partition for allocation

**Returns**: Node allocation confirmation with access details, resource specifications, and connection information.

### `deallocate_slurm_nodes`
**Description**: Deallocate previously allocated compute nodes with comprehensive cleanup and resource management. Ensures proper resource release and accounting.

**Parameters**:
- `allocation_id` (str): Allocation ID to deallocate

**Returns**: Deallocation confirmation with cleanup status and resource release verification.

### `get_allocation_status`
**Description**: Check status of interactive node allocations with comprehensive resource monitoring and usage analysis. Provides allocation health and efficiency metrics.

**Parameters**:
- `allocation_id` (str): Allocation ID to check status for

**Returns**: Complete allocation status including resource usage, performance metrics, and efficiency analysis.

## Examples

### 1. Job Submission and Monitoring
```
I need to submit a Python simulation script to Slurm with 16 cores and 32GB memory, then monitor its progress until completion.
```

**Tools called:**
- `submit_slurm_job` - Submit job with resource specification
- `check_job_status` - Monitor job progress and performance

### 2. Array Job Management
```
Submit an array job for parameter sweep analysis with 100 tasks, each requiring 4 cores and 8GB memory, then check the overall progress.
```

**Tools called:**
- `submit_array_job` - Submit parallel array job
- `list_slurm_jobs` - Monitor array job progress
- `get_job_details` - Get detailed array job information

### 3. Interactive Session Management
```
Allocate 2 compute nodes with 8 cores each for an interactive analysis session, then deallocate when finished.
```

**Tools called:**
- `allocate_slurm_nodes` - Allocate interactive nodes
- `get_node_info` - Check node status and resources
- `deallocate_slurm_nodes` - Clean up allocated resources

### 4. Job Management and Cleanup
```
I have a long-running job that needs to be cancelled, and I want to retrieve the output from a completed job before cleaning up.
```

**Tools called:**
- `cancel_slurm_job` - Cancel running job with cleanup
- `get_job_output` - Retrieve completed job outputs
- `get_job_details` - Get final job performance metrics

### 5. Allocation Status and Monitoring
```
Check the status of my current interactive allocation and monitor its resource usage efficiency.
```

**Tools called:**
- `get_allocation_status` - Monitor allocation efficiency
- `get_node_info` - Check node resource usage
- `deallocate_slurm_nodes` - Clean up when finished

### 6. Comprehensive Cluster Analysis
```
Analyze the current cluster queue status, identify bottlenecks, and suggest optimal resource allocation for my pending jobs.
```

**Tools called:**
- `get_slurm_info` - Get cluster status and capacity
- `get_queue_info` - Analyze queue performance and bottlenecks
- `list_slurm_jobs` - Review pending job queue and priorities