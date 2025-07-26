"""
Tests for ArXiv MCP Server implementation.
"""

import pytest
import sys
import os
import json
from unittest.mock import AsyncMock, patch
from io import StringIO

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import server


class TestServerTools:
    """Test MCP server tool implementations"""

    @pytest.mark.asyncio
    async def test_search_arxiv_tool(self):
        """Test search_arxiv tool"""
        expected_result = {"success": True, "papers": [{"id": "test"}]}

        with patch(
            "mcp_handlers.search_arxiv_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            # Access the underlying function from the MCP tool
            result = await server.search_arxiv_tool.fn("machine learning", 10)

            assert result == expected_result
            mock_handler.assert_called_once_with("machine learning", 10)

    @pytest.mark.asyncio
    async def test_search_arxiv_tool_default_params(self):
        """Test search_arxiv tool with default parameters"""
        expected_result = {"success": True, "papers": []}

        with patch(
            "mcp_handlers.search_arxiv_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_arxiv_tool.fn()

            assert result == expected_result
            mock_handler.assert_called_once_with("cs.AI", 5)

    @pytest.mark.asyncio
    async def test_get_recent_papers_tool(self):
        """Test get_recent_papers tool"""
        expected_result = {"success": True, "papers": [{"recent": True}]}

        with patch(
            "mcp_handlers.get_recent_papers_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.get_recent_papers_tool.fn("cs.LG", 15)

            assert result == expected_result
            mock_handler.assert_called_once_with("cs.LG", 15)

    @pytest.mark.asyncio
    async def test_get_recent_papers_tool_default_params(self):
        """Test get_recent_papers tool with default parameters"""
        expected_result = {"success": True, "papers": []}

        with patch(
            "mcp_handlers.get_recent_papers_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.get_recent_papers_tool.fn()

            assert result == expected_result
            mock_handler.assert_called_once_with("cs.AI", 5)

    @pytest.mark.asyncio
    async def test_search_papers_by_author_tool(self):
        """Test search_papers_by_author tool"""
        expected_result = {"success": True, "author": "John Doe", "papers": []}

        with patch(
            "mcp_handlers.search_papers_by_author_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_papers_by_author_tool.fn("John Doe", 20)

            assert result == expected_result
            mock_handler.assert_called_once_with("John Doe", 20)

    @pytest.mark.asyncio
    async def test_search_papers_by_author_tool_default_params(self):
        """Test search_papers_by_author tool with default parameters"""
        expected_result = {"success": True, "author": "Jane Smith", "papers": []}

        with patch(
            "mcp_handlers.search_papers_by_author_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_papers_by_author_tool.fn("Jane Smith")

            assert result == expected_result
            mock_handler.assert_called_once_with("Jane Smith", 10)

    @pytest.mark.asyncio
    async def test_search_by_title_tool(self):
        """Test search_by_title tool"""
        expected_result = {"success": True, "title_results": []}

        with patch(
            "mcp_handlers.search_by_title_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_by_title_tool.fn("neural networks", 5)

            assert result == expected_result
            mock_handler.assert_called_once_with("neural networks", 5)

    @pytest.mark.asyncio
    async def test_search_by_abstract_tool(self):
        """Test search_by_abstract tool"""
        expected_result = {"success": True, "abstract_results": []}

        with patch(
            "mcp_handlers.search_by_abstract_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_by_abstract_tool.fn("deep learning", 8)

            assert result == expected_result
            mock_handler.assert_called_once_with("deep learning", 8)

    @pytest.mark.asyncio
    async def test_search_by_subject_tool(self):
        """Test search_by_subject tool"""
        expected_result = {"success": True, "subject": "cs.AI", "papers": []}

        with patch(
            "mcp_handlers.search_by_subject_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_by_subject_tool.fn("cs.AI", 12)

            assert result == expected_result
            mock_handler.assert_called_once_with("cs.AI", 12)

    @pytest.mark.asyncio
    async def test_search_date_range_tool(self):
        """Test search_date_range tool"""
        expected_result = {"success": True, "date_range_results": []}

        with patch(
            "mcp_handlers.search_date_range_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_date_range_tool.fn(
                "2024-01-01", "2024-12-31", "cs.AI", 50
            )

            assert result == expected_result
            mock_handler.assert_called_once_with(
                "2024-01-01", "2024-12-31", "cs.AI", 50
            )

    @pytest.mark.asyncio
    async def test_search_date_range_tool_default_params(self):
        """Test search_date_range tool with default parameters"""
        expected_result = {"success": True, "date_range_results": []}

        with patch(
            "mcp_handlers.search_date_range_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.search_date_range_tool.fn("2024-01-01", "2024-12-31")

            assert result == expected_result
            mock_handler.assert_called_once_with("2024-01-01", "2024-12-31", "", 20)

    @pytest.mark.asyncio
    async def test_get_paper_details_tool(self):
        """Test get_paper_details tool"""
        expected_result = {"success": True, "paper": {"id": "2401.12345"}}

        with patch(
            "mcp_handlers.get_paper_details_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.get_paper_details_tool.fn("2401.12345")

            assert result == expected_result
            mock_handler.assert_called_once_with("2401.12345")

    @pytest.mark.asyncio
    async def test_export_to_bibtex_tool(self):
        """Test export_to_bibtex tool"""
        papers_json = json.dumps([{"id": "test_paper"}])
        expected_result = {"success": True, "bibtex": "@article{...}"}

        with patch(
            "mcp_handlers.export_to_bibtex_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.export_to_bibtex_tool.fn(papers_json)

            assert result == expected_result
            mock_handler.assert_called_once_with(papers_json)

    @pytest.mark.asyncio
    async def test_find_similar_papers_tool(self):
        """Test find_similar_papers tool"""
        expected_result = {"success": True, "similar_papers": []}

        with patch(
            "mcp_handlers.find_similar_papers_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.find_similar_papers_tool.fn("2401.12345", 15)

            assert result == expected_result
            mock_handler.assert_called_once_with("2401.12345", 15)

    @pytest.mark.asyncio
    async def test_find_similar_papers_tool_default_params(self):
        """Test find_similar_papers tool with default parameters"""
        expected_result = {"success": True, "similar_papers": []}

        with patch(
            "mcp_handlers.find_similar_papers_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.find_similar_papers_tool.fn("2401.12345")

            assert result == expected_result
            mock_handler.assert_called_once_with("2401.12345", 10)

    @pytest.mark.asyncio
    async def test_download_paper_pdf_tool(self):
        """Test download_paper_pdf tool"""
        expected_result = {"success": True, "download_path": "/tmp/paper.pdf"}

        with patch(
            "mcp_handlers.download_paper_pdf_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.download_paper_pdf_tool.fn("2401.12345", "/tmp/")

            assert result == expected_result
            mock_handler.assert_called_once_with("2401.12345", "/tmp/")

    @pytest.mark.asyncio
    async def test_download_paper_pdf_tool_no_path(self):
        """Test download_paper_pdf tool without download path"""
        expected_result = {"success": True, "download_path": "./paper.pdf"}

        with patch(
            "mcp_handlers.download_paper_pdf_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.download_paper_pdf_tool.fn("2401.12345")

            assert result == expected_result
            mock_handler.assert_called_once_with("2401.12345", None)

    @pytest.mark.asyncio
    async def test_get_pdf_url_tool(self):
        """Test get_pdf_url tool"""
        expected_result = {
            "success": True,
            "pdf_url": "https://arxiv.org/pdf/2401.12345.pdf",
        }

        with patch(
            "mcp_handlers.get_pdf_url_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.get_pdf_url_tool.fn("2401.12345")

            assert result == expected_result
            mock_handler.assert_called_once_with("2401.12345")

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_tool(self):
        """Test download_multiple_pdfs tool"""
        arxiv_ids_json = json.dumps(["2401.12345", "2401.12346"])
        expected_result = {"success": True, "downloads": 2}

        with patch(
            "mcp_handlers.download_multiple_pdfs_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.download_multiple_pdfs_tool.fn(
                arxiv_ids_json, "/tmp/", 5
            )

            assert result == expected_result
            mock_handler.assert_called_once_with(arxiv_ids_json, "/tmp/", 5)

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_tool_default_params(self):
        """Test download_multiple_pdfs tool with default parameters"""
        arxiv_ids_json = json.dumps(["2401.12345"])
        expected_result = {"success": True, "downloads": 1}

        with patch(
            "mcp_handlers.download_multiple_pdfs_handler", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = expected_result

            result = await server.download_multiple_pdfs_tool.fn(arxiv_ids_json)

            assert result == expected_result
            mock_handler.assert_called_once_with(arxiv_ids_json, None, 3)


class TestServerMain:
    """Test server main function and startup logic"""

    def test_main_stdio_transport(self):
        """Test main function with stdio transport"""
        with patch.dict(os.environ, {"MCP_TRANSPORT": "stdio"}):
            with patch("server.mcp.run") as mock_run:
                with patch("sys.exit") as mock_exit:
                    with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                        server.main()

                        mock_run.assert_called_once_with(transport="stdio")
                        mock_exit.assert_not_called()

                        # Check stderr output
                        stderr_output = mock_stderr.getvalue()
                        assert "Starting stdio transport" in stderr_output

    def test_main_sse_transport(self):
        """Test main function with SSE transport"""
        with patch.dict(
            os.environ,
            {
                "MCP_TRANSPORT": "sse",
                "MCP_SSE_HOST": "127.0.0.1",
                "MCP_SSE_PORT": "9000",
            },
        ):
            with patch("server.mcp.run") as mock_run:
                with patch("sys.exit") as mock_exit:
                    with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                        server.main()

                        mock_run.assert_called_once_with(
                            transport="sse", host="127.0.0.1", port=9000
                        )
                        mock_exit.assert_not_called()

                        # Check stderr output
                        stderr_output = mock_stderr.getvalue()
                        assert "Starting SSE on 127.0.0.1:9000" in stderr_output

    def test_main_sse_transport_default_host_port(self):
        """Test main function with SSE transport using default host and port"""
        with patch.dict(os.environ, {"MCP_TRANSPORT": "sse"}, clear=True):
            with patch("server.mcp.run") as mock_run:
                with patch("sys.exit") as mock_exit:
                    with patch("sys.stderr", new_callable=StringIO):
                        server.main()

                        mock_run.assert_called_once_with(
                            transport="sse", host="0.0.0.0", port=8000
                        )
                        mock_exit.assert_not_called()

    def test_main_default_transport(self):
        """Test main function with no transport specified (defaults to stdio)"""
        with patch.dict(os.environ, {}, clear=True):
            with patch("server.mcp.run") as mock_run:
                with patch("sys.exit") as mock_exit:
                    with patch("sys.stderr", new_callable=StringIO):
                        server.main()

                        mock_run.assert_called_once_with(transport="stdio")
                        mock_exit.assert_not_called()

    def test_main_exception_handling(self):
        """Test main function exception handling"""
        with patch("server.mcp.run") as mock_run:
            mock_run.side_effect = Exception("Server startup failed")

            with patch("sys.exit") as mock_exit:
                with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                    server.main()

                    mock_exit.assert_called_once_with(1)

                    # Check error output
                    stderr_output = mock_stderr.getvalue()
                    assert "Server startup failed" in stderr_output

    def test_main_invalid_port_number(self):
        """Test main function with invalid port number"""
        with patch.dict(
            os.environ, {"MCP_TRANSPORT": "sse", "MCP_SSE_PORT": "not_a_number"}
        ):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stderr", new_callable=StringIO):
                    server.main()

                    mock_exit.assert_called_once_with(1)


class TestServerConfiguration:
    """Test server configuration and initialization"""

    def test_server_initialization(self):
        """Test that MCP server is properly initialized"""
        assert server.mcp is not None
        assert hasattr(server.mcp, "tool")
        assert hasattr(server.mcp, "run")

    @patch("dotenv.load_dotenv")
    def test_environment_loading(self, mock_load_dotenv):
        """Test that environment variables are loaded"""
        # Re-import to trigger environment loading
        import importlib

        importlib.reload(server)
        mock_load_dotenv.assert_called()

    def test_logging_configuration(self):
        """Test that logging is properly configured"""
        import logging

        logger = logging.getLogger("server")
        assert logger.level <= logging.INFO

    def test_path_configuration(self):
        """Test that sys.path is properly configured"""
        # Check that current directory is in sys.path
        current_dir = os.path.dirname(server.__file__)
        assert current_dir in sys.path

    def test_sys_path_insert(self):
        """Test sys.path modification"""
        # Check that current directory is in sys.path (should be done by module import)
        import sys
        import os

        current_dir = os.path.dirname(server.__file__)
        # The path should have been inserted when server module was loaded
        assert any(current_dir in path for path in sys.path)
