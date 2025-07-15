# Math Analysis MCP

A Model Context Protocol (MCP) server implemented in C++ that provides mathematical analysis capabilities including statistics, linear algebra, and numerical analysis.

## Features

- **Statistical Analysis**: Calculate mean, median, mode, standard deviation, variance, and other descriptive statistics
- **Linear Algebra**: Matrix multiplication, matrix-vector multiplication, dot product, transpose, and determinant
- **Numerical Analysis**: Polynomial fitting, numerical differentiation, and numerical integration
- **High Performance**: Implemented in C++ for efficient mathematical computations

## Building

```bash
cd math-analysis-mcp
mkdir -p build
cd build
cmake ..
make
```

## Usage

Run the MCP server:

```bash
./build/math_analysis_server
```

## Demo

Run the demo script to see all tools in action:

```bash
python demo_cpp.py
```

The demo script will:
1. Start the C++ MCP server
2. Initialize the MCP connection
3. List available tools
4. Test each tool with sample data
5. Display the results
6. Stop the server

## Tools

### calculate_statistics
Calculate comprehensive statistics for a dataset including mean, median, mode, standard deviation, variance, min, max, and range.

### multiply_matrices
Multiply two matrices using standard matrix multiplication algorithm.

### multiply_matrix_vector
Multiply a matrix by a vector to produce a resulting vector.

### polynomial_fit
Fit a polynomial of specified degree to data points using least squares method.

### numerical_differentiate
Compute numerical derivative of discrete data points using finite difference methods.

## Dependencies

- C++17 compatible compiler
- CMake 3.10 or higher
- Standard math library (linked automatically)

## Architecture

The server implements a custom JSON parser and MCP protocol handler, providing:

- JSON-RPC 2.0 protocol compliance
- Tool registration and discovery
- Parameter validation
- Error handling and reporting
- High-performance mathematical operations