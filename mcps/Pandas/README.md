# Pandas MCP - Advanced Data Analysis for LLMs


## Description

Pandas MCP is a Model Context Protocol server that enables LLMs to perform advanced data analysis and manipulation using the powerful Pandas library, featuring comprehensive statistical analysis, data cleaning and transformation, time series operations, multi-format data I/O (CSV, Excel, JSON, Parquet, HDF5), and intelligent data quality assessment for seamless data science workflows.



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
    "pandas-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
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
    "pandas-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Code</b></summary>

Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.

```sh
claude mcp add pandas-mcp -- uvx iowarp-mcps pandas
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.

```json
{
  "mcpServers": {
    "pandas-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "pandas"]
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
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Pandas run pandas-mcp --help
```

**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Pandas run pandas-mcp --help
```

**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Pandas run pandas-mcp --help
```

</details>

## Capabilities

### `load_data`
**Description**: Load data from various file formats (CSV, Excel, JSON, Parquet) with intelligent format detection, encoding handling, and comprehensive data type inference for seamless data processing.

**Parameters**:
- `file_path` (str): Absolute path to the data file
- `file_format` (str, optional): File format specification (auto-detected if not provided)
- `encoding` (str, optional): Character encoding (auto-detected if not provided)

**Returns**: Loaded DataFrame with metadata, data types, and loading statistics.

### `save_data`
**Description**: Save DataFrame to multiple file formats with intelligent formatting, compression options, and performance optimization for efficient data export and sharing.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame to save
- `file_path` (str): Output file path with format extension
- `format` (str, optional): Output format (CSV, Excel, JSON, Parquet)
- `compression` (str, optional): Compression method for size optimization

**Returns**: Save confirmation with file size, format details, and performance metrics.

### `statistical_summary`
**Description**: Generate comprehensive statistical analysis including descriptive statistics, distribution analysis, and data quality metrics with intelligent insights and recommendations.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame for statistical analysis
- `columns` (list, optional): Specific columns to analyze

**Returns**: Complete statistical summary with descriptive statistics, distribution analysis, and data quality insights.

### `correlation_analysis`
**Description**: Perform comprehensive correlation analysis using multiple methods (Pearson, Spearman, Kendall) with significance testing and visualization recommendations for relationship discovery.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame for correlation analysis
- `method` (str, optional): Correlation method (pearson, spearman, kendall)
- `columns` (list, optional): Specific columns for correlation analysis

**Returns**: Correlation matrix with significance levels, strength interpretation, and visualization recommendations.

### `hypothesis_testing`
**Description**: Conduct statistical hypothesis testing including t-tests, ANOVA, chi-square tests, and normality testing with comprehensive result interpretation and statistical insights.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame for hypothesis testing
- `test_type` (str): Type of statistical test to perform
- `columns` (list): Columns involved in the test
- `alpha` (float, optional): Significance level (default: 0.05)

**Returns**: Test results with p-values, test statistics, conclusions, and interpretation guidance.

### `handle_missing_data`
**Description**: Intelligent missing data handling with multiple imputation strategies, pattern analysis, and data quality assessment for robust data preprocessing.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame with missing values
- `strategy` (str): Imputation strategy (mean, median, mode, forward_fill, backward_fill, drop)
- `columns` (list, optional): Specific columns to process

**Returns**: Processed DataFrame with missing data handled and imputation summary report.

### `clean_data`
**Description**: Comprehensive data cleaning including outlier detection and removal, duplicate handling, data type optimization, and quality validation for analysis-ready datasets.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame to clean
- `remove_outliers` (bool, optional): Whether to detect and remove outliers
- `remove_duplicates` (bool, optional): Whether to remove duplicate rows
- `optimize_types` (bool, optional): Whether to optimize data types

**Returns**: Cleaned DataFrame with quality report, outlier analysis, and optimization details.

### `groupby_operations`
**Description**: Advanced grouping and aggregation operations with multiple aggregation functions, statistical analysis, and intelligent insights for categorical data analysis.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame for grouping operations
- `group_columns` (list): Columns to group by
- `agg_columns` (list): Columns to aggregate
- `agg_functions` (list): Aggregation functions to apply

**Returns**: Grouped results with aggregation summary, statistical insights, and comparative analysis.

### `merge_datasets`
**Description**: Intelligent dataset merging and joining with multiple join strategies, relationship validation, and data quality assessment for comprehensive data integration.

**Parameters**:
- `left_data` (DataFrame): Left DataFrame for merging
- `right_data` (DataFrame): Right DataFrame for merging
- `join_type` (str): Type of join (inner, outer, left, right)
- `on_columns` (list): Columns to join on

**Returns**: Merged DataFrame with join statistics, relationship analysis, and data quality assessment.

### `pivot_table`
**Description**: Create comprehensive pivot tables with multi-level indexing, multiple aggregation functions, and statistical analysis for cross-tabulation and summary reporting.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame for pivot table creation
- `index` (list): Columns for row indexing
- `columns` (list): Columns for column indexing
- `values` (list): Columns for aggregation
- `aggfunc` (str, optional): Aggregation function

**Returns**: Pivot table with statistical summary, cross-tabulation analysis, and formatting recommendations.

### `time_series_operations`
**Description**: Advanced time series analysis including resampling, rolling windows, lag features, and temporal pattern analysis for time-based data insights.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame with time series data
- `date_column` (str): Column containing datetime information
- `operation` (str): Time series operation (resample, rolling, lag, decompose)
- `frequency` (str, optional): Resampling frequency

**Returns**: Time series analysis results with temporal patterns, trends, and statistical insights.

### `validate_data`
**Description**: Comprehensive data validation with business rule checking, constraint validation, and data quality assessment for reliable analysis and reporting.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame to validate
- `rules` (dict): Validation rules and constraints
- `columns` (list, optional): Specific columns to validate

**Returns**: Validation report with rule compliance, quality metrics, and issue identification.

### `filter_data`
**Description**: Advanced data filtering with complex conditions, range filtering, and pattern matching for precise data subset selection and analysis.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame to filter
- `conditions` (dict): Filtering conditions and criteria
- `columns` (list, optional): Specific columns for filtering

**Returns**: Filtered DataFrame with filtering summary and subset statistics.

### `optimize_memory`
**Description**: Intelligent memory optimization with data type conversion, categorical encoding, and storage efficiency analysis for large dataset processing.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame to optimize
- `categorical_threshold` (int, optional): Threshold for categorical conversion

**Returns**: Memory-optimized DataFrame with optimization report and efficiency metrics.

### `profile_data`
**Description**: Generate comprehensive data profiling report including data quality assessment, statistical analysis, pattern recognition, and recommendation insights.

**Parameters**:
- `data` (DataFrame): Pandas DataFrame to profile
- `detailed` (bool, optional): Whether to include detailed analysis

**Returns**: Complete data profile with quality metrics, statistical analysis, and actionable insights.

## Examples

### 1. Data Loading and Profiling
```
I have a large CSV file with sales data that I need to load and get a comprehensive profile including data types, missing values, and basic statistics.
```

**Tools called:**
- `load_data` - Load CSV file with intelligent format detection
- `profile_data` - Get comprehensive data profile and quality metrics
- `statistical_summary` - Generate descriptive statistics and distributions

### 2. Data Cleaning and Quality Assessment
```
My dataset has missing values and outliers that need to be handled. I also want to remove duplicates and validate the data quality.
```

**Tools called:**
- `handle_missing_data` - Impute missing values with appropriate strategies
- `clean_data` - Remove outliers, duplicates, and optimize data types
- `validate_data` - Apply business rules and data quality checks

### 3. Statistical Analysis and Correlation
```
Analyze the relationships between different variables in my dataset and perform hypothesis testing to validate my assumptions.
```

**Tools called:**
- `correlation_analysis` - Calculate correlation matrices with different methods
- `hypothesis_testing` - Perform t-tests, ANOVA, and normality tests
- `statistical_summary` - Generate comprehensive statistical insights

### 4. Data Transformation and Aggregation
```
I need to group my sales data by region and product category, then create pivot tables for cross-analysis and merge with customer data.
```

**Tools called:**
- `groupby_operations` - Group data and perform multiple aggregations
- `pivot_table` - Create pivot tables with multi-level indexing
- `merge_datasets` - Join datasets using different merge strategies

### 5. Time Series Analysis and Filtering
```
Analyze my time series data by resampling to different frequencies, calculating rolling averages, and filtering specific date ranges.
```

**Tools called:**
- `time_series_operations` - Resample, rolling windows, and lag features
- `filter_data` - Apply complex time-based filtering conditions
- `statistical_summary` - Analyze time series patterns and trends

### 6. Data Export and Memory Optimization
```
Optimize memory usage of my large dataset and export the cleaned data to multiple formats for different teams.
```

**Tools called:**
- `optimize_memory` - Reduce memory usage with dtype optimization
- `save_data` - Export to CSV, Excel, Parquet, and JSON formats
- `profile_data` - Verify optimization results and final data quality

