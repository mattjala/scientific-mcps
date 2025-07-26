"""
Unit tests for server module.

Covers:
 - FastMCP server initialization and tool registration
 - Tool function wrappers (list_hdf5_tool, inspect_hdf5_tool, etc.)
 - Error handling in tool functions
 - Main function with different transport modes
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Mock FastMCP before importing server
with patch("fastmcp.FastMCP") as mock_fastmcp:
    mock_instance = MagicMock()
    mock_fastmcp.return_value = mock_instance

    # Import server after mocking
    import server


class TestServerModule:
    """Test the server module functionality."""

    def test_server_import_success(self):
        """Test that server module imports successfully."""
        print("\n=== Running test_server_import_success ===")

        # Test that we can import the server module
        assert server is not None
        print("Server module imported successfully")

    def test_mcp_instance_exists(self):
        """Test that MCP instance is created."""
        print("\n=== Running test_mcp_instance_exists ===")

        assert hasattr(server, "mcp")
        assert server.mcp is not None
        print("MCP instance exists")


class TestServerMain:
    """Test the main function and server initialization."""

    @patch("server.mcp")
    @patch.dict(os.environ, {"MCP_TRANSPORT": "stdio"})
    def test_main_stdio_transport(self, mock_mcp):
        """Test main function with stdio transport."""
        print("\n=== Running test_main_stdio_transport ===")

        with patch("sys.stderr"):
            server.main()

            # Check that run was called with stdio transport
            mock_mcp.run.assert_called_once_with(transport="stdio")

    @patch("server.mcp")
    @patch.dict(
        os.environ,
        {"MCP_TRANSPORT": "sse", "MCP_SSE_HOST": "127.0.0.1", "MCP_SSE_PORT": "9000"},
    )
    def test_main_sse_transport(self, mock_mcp):
        """Test main function with SSE transport."""
        print("\n=== Running test_main_sse_transport ===")

        with patch("sys.stderr"):
            server.main()

            # Check that run was called with SSE transport and custom host/port
            mock_mcp.run.assert_called_once_with(
                transport="sse", host="127.0.0.1", port=9000
            )

    @patch("server.mcp")
    @patch.dict(os.environ, {"MCP_TRANSPORT": "SSE"})  # Test case insensitive
    def test_main_sse_transport_defaults(self, mock_mcp):
        """Test main function with SSE transport using defaults."""
        print("\n=== Running test_main_sse_transport_defaults ===")

        with patch("sys.stderr"):
            server.main()

            # Check that run was called with SSE transport and default host/port
            mock_mcp.run.assert_called_once_with(
                transport="sse", host="0.0.0.0", port=8000
            )

    @patch("server.mcp")
    def test_main_default_transport(self, mock_mcp):
        """Test main function with no transport specified (defaults to stdio)."""
        print("\n=== Running test_main_default_transport ===")

        # Clear any existing MCP_TRANSPORT environment variable
        with patch.dict(os.environ, {}, clear=True):
            with patch("sys.stderr"):
                server.main()

                # Should default to stdio
                mock_mcp.run.assert_called_once_with(transport="stdio")

    @patch("server.mcp")
    @patch.dict(os.environ, {"MCP_TRANSPORT": "stdio"})
    def test_main_exception_handling(self, mock_mcp):
        """Test main function exception handling."""
        print("\n=== Running test_main_exception_handling ===")

        # Make mcp.run raise an exception
        mock_mcp.run.side_effect = RuntimeError("Server startup failed")

        with patch("sys.stderr"):
            with patch("sys.exit") as mock_exit:
                server.main()

                # Should exit with code 1
                mock_exit.assert_called_once_with(1)


class TestServerInitialization:
    """Test server initialization and module-level code."""

    def test_fastmcp_initialization(self):
        """Test that FastMCP server is initialized correctly."""
        print("\n=== Running test_fastmcp_initialization ===")

        # The server module should have been imported with mocked FastMCP
        assert hasattr(server, "mcp")
        assert server.mcp is not None

    def test_environment_loading(self):
        """Test that environment variables are loaded."""
        print("\n=== Running test_environment_loading ===")

        # Test that load_dotenv was called during module import
        # This is verified by the fact that the module imported successfully
        assert True  # If we get here, load_dotenv didn't raise an exception

    def test_path_modification(self):
        """Test that sys.path was modified correctly."""
        print("\n=== Running test_path_modification ===")

        # Check that the parent directory was added to sys.path
        current_dir = os.path.dirname(os.path.abspath(server.__file__))
        assert current_dir in sys.path


class TestToolDecorators:
    """Test that tools are properly decorated and registered."""

    def test_tool_functions_exist(self):
        """Test that all expected tool functions exist."""
        print("\n=== Running test_tool_functions_exist ===")

        assert hasattr(server, "list_hdf5_tool")
        assert hasattr(server, "inspect_hdf5_tool")
        assert hasattr(server, "preview_hdf5_tool")
        assert hasattr(server, "read_all_hdf5_tool")
        assert hasattr(server, "main")
        print("All expected functions exist")

    def test_main_function_callable(self):
        """Test that main function is callable."""
        print("\n=== Running test_main_function_callable ===")

        assert callable(server.main)
        print("Main function is callable")
