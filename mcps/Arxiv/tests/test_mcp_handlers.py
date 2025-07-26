"""
Tests for ArXiv MCP handlers.
"""

import pytest
import sys
import os
import json
from unittest.mock import AsyncMock, patch

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import mcp_handlers


class TestSearchHandlers:
    """Test search-related MCP handlers"""

    @pytest.mark.asyncio
    async def test_search_arxiv_handler_success(self):
        """Test successful search_arxiv handler"""
        expected_result = {"success": True, "papers": [{"id": "test"}]}

        with patch("mcp_handlers.search_arxiv", new_callable=AsyncMock) as mock_search:
            mock_search.return_value = expected_result

            result = await mcp_handlers.search_arxiv_handler("machine learning", 10)

            assert result == expected_result
            mock_search.assert_called_once_with("machine learning", 10)

    @pytest.mark.asyncio
    async def test_search_arxiv_handler_default_params(self):
        """Test search_arxiv handler with default parameters"""
        expected_result = {"success": True, "papers": []}

        with patch("mcp_handlers.search_arxiv", new_callable=AsyncMock) as mock_search:
            mock_search.return_value = expected_result

            result = await mcp_handlers.search_arxiv_handler()

            assert result == expected_result
            mock_search.assert_called_once_with("cs.AI", 5)

    @pytest.mark.asyncio
    async def test_search_arxiv_handler_exception(self):
        """Test search_arxiv handler exception handling"""
        with patch("mcp_handlers.search_arxiv", new_callable=AsyncMock) as mock_search:
            mock_search.side_effect = ValueError("API Error")

            result = await mcp_handlers.search_arxiv_handler("test")

            assert result["isError"] is True
            assert "API Error" in json.loads(result["content"][0]["text"])["error"]
            assert result["_meta"]["tool"] == "search_arxiv"
            assert result["_meta"]["error"] == "ValueError"

    @pytest.mark.asyncio
    async def test_get_recent_papers_handler_success(self):
        """Test successful get_recent_papers handler"""
        expected_result = {"success": True, "papers": [{"recent": True}]}

        with patch(
            "mcp_handlers.get_recent_papers", new_callable=AsyncMock
        ) as mock_recent:
            mock_recent.return_value = expected_result

            result = await mcp_handlers.get_recent_papers_handler("cs.LG", 15)

            assert result == expected_result
            mock_recent.assert_called_once_with("cs.LG", 15)

    @pytest.mark.asyncio
    async def test_get_recent_papers_handler_exception(self):
        """Test get_recent_papers handler exception handling"""
        with patch(
            "mcp_handlers.get_recent_papers", new_callable=AsyncMock
        ) as mock_recent:
            mock_recent.side_effect = ConnectionError("Network error")

            result = await mcp_handlers.get_recent_papers_handler()

            assert result["isError"] is True
            assert "Network error" in json.loads(result["content"][0]["text"])["error"]
            assert result["_meta"]["tool"] == "get_recent_papers"
            assert result["_meta"]["error"] == "ConnectionError"

    @pytest.mark.asyncio
    async def test_search_papers_by_author_handler_success(self):
        """Test successful search_papers_by_author handler"""
        expected_result = {"success": True, "author": "John Doe", "papers": []}

        with patch(
            "mcp_handlers.search_papers_by_author", new_callable=AsyncMock
        ) as mock_author:
            mock_author.return_value = expected_result

            result = await mcp_handlers.search_papers_by_author_handler("John Doe", 20)

            assert result == expected_result
            mock_author.assert_called_once_with("John Doe", 20)

    @pytest.mark.asyncio
    async def test_search_by_title_handler_success(self):
        """Test successful search_by_title handler"""
        expected_result = {"success": True, "title_results": []}

        with patch(
            "mcp_handlers.search_by_title", new_callable=AsyncMock
        ) as mock_title:
            mock_title.return_value = expected_result

            result = await mcp_handlers.search_by_title_handler("neural networks", 5)

            assert result == expected_result
            mock_title.assert_called_once_with("neural networks", 5)

    @pytest.mark.asyncio
    async def test_search_by_abstract_handler_success(self):
        """Test successful search_by_abstract handler"""
        expected_result = {"success": True, "abstract_results": []}

        with patch(
            "mcp_handlers.search_by_abstract", new_callable=AsyncMock
        ) as mock_abstract:
            mock_abstract.return_value = expected_result

            result = await mcp_handlers.search_by_abstract_handler("deep learning", 8)

            assert result == expected_result
            mock_abstract.assert_called_once_with("deep learning", 8)

    @pytest.mark.asyncio
    async def test_search_by_subject_handler_success(self):
        """Test successful search_by_subject handler"""
        expected_result = {"success": True, "subject": "cs.AI", "papers": []}

        with patch(
            "mcp_handlers.search_by_subject", new_callable=AsyncMock
        ) as mock_subject:
            mock_subject.return_value = expected_result

            result = await mcp_handlers.search_by_subject_handler("cs.AI", 12)

            assert result == expected_result
            mock_subject.assert_called_once_with("cs.AI", 12)

    @pytest.mark.asyncio
    async def test_search_date_range_handler_success(self):
        """Test successful search_date_range handler"""
        expected_result = {"success": True, "date_range_results": []}

        with patch(
            "mcp_handlers.search_date_range", new_callable=AsyncMock
        ) as mock_date:
            mock_date.return_value = expected_result

            result = await mcp_handlers.search_date_range_handler(
                "2024-01-01", "2024-12-31", "cs.AI", 50
            )

            assert result == expected_result
            mock_date.assert_called_once_with("2024-01-01", "2024-12-31", "cs.AI", 50)

    @pytest.mark.asyncio
    async def test_search_date_range_handler_default_params(self):
        """Test search_date_range handler with default parameters"""
        expected_result = {"success": True, "date_range_results": []}

        with patch(
            "mcp_handlers.search_date_range", new_callable=AsyncMock
        ) as mock_date:
            mock_date.return_value = expected_result

            result = await mcp_handlers.search_date_range_handler(
                "2024-01-01", "2024-12-31"
            )

            assert result == expected_result
            mock_date.assert_called_once_with("2024-01-01", "2024-12-31", "", 20)


class TestPaperDetailsHandlers:
    """Test paper details and similar papers handlers"""

    @pytest.mark.asyncio
    async def test_get_paper_details_handler_success(self):
        """Test successful get_paper_details handler"""
        expected_result = {"success": True, "paper": {"id": "2401.12345"}}

        with patch(
            "mcp_handlers.get_paper_details", new_callable=AsyncMock
        ) as mock_details:
            mock_details.return_value = expected_result

            result = await mcp_handlers.get_paper_details_handler("2401.12345")

            assert result == expected_result
            mock_details.assert_called_once_with("2401.12345")

    @pytest.mark.asyncio
    async def test_get_paper_details_handler_exception(self):
        """Test get_paper_details handler exception handling"""
        with patch(
            "mcp_handlers.get_paper_details", new_callable=AsyncMock
        ) as mock_details:
            mock_details.side_effect = Exception("Paper not found")

            result = await mcp_handlers.get_paper_details_handler("invalid_id")

            assert result["isError"] is True
            assert (
                "Paper not found" in json.loads(result["content"][0]["text"])["error"]
            )
            assert result["_meta"]["tool"] == "get_paper_details"

    @pytest.mark.asyncio
    async def test_find_similar_papers_handler_success(self):
        """Test successful find_similar_papers handler"""
        expected_result = {"success": True, "similar_papers": []}

        with patch(
            "mcp_handlers.find_similar_papers", new_callable=AsyncMock
        ) as mock_similar:
            mock_similar.return_value = expected_result

            result = await mcp_handlers.find_similar_papers_handler("2401.12345", 15)

            assert result == expected_result
            mock_similar.assert_called_once_with("2401.12345", 15)

    @pytest.mark.asyncio
    async def test_find_similar_papers_handler_exception(self):
        """Test find_similar_papers handler exception handling"""
        with patch(
            "mcp_handlers.find_similar_papers", new_callable=AsyncMock
        ) as mock_similar:
            mock_similar.side_effect = RuntimeError("Reference paper not found")

            result = await mcp_handlers.find_similar_papers_handler("invalid_id", 10)

            assert result["isError"] is True
            assert (
                "Reference paper not found"
                in json.loads(result["content"][0]["text"])["error"]
            )
            assert result["_meta"]["error"] == "RuntimeError"


class TestExportHandlers:
    """Test export and utility handlers"""

    @pytest.mark.asyncio
    async def test_export_to_bibtex_handler_success(self):
        """Test successful export_to_bibtex handler"""
        papers = [{"id": "test_paper", "title": "Test"}]
        papers_json = json.dumps(papers)
        expected_result = {"success": True, "bibtex": "@article{...}"}

        with patch(
            "mcp_handlers.export_to_bibtex", new_callable=AsyncMock
        ) as mock_export:
            mock_export.return_value = expected_result

            result = await mcp_handlers.export_to_bibtex_handler(papers_json)

            assert result == expected_result
            mock_export.assert_called_once_with(papers)

    @pytest.mark.asyncio
    async def test_export_to_bibtex_handler_invalid_json(self):
        """Test export_to_bibtex handler with invalid JSON"""
        invalid_json = "not valid json"

        result = await mcp_handlers.export_to_bibtex_handler(invalid_json)

        assert result["isError"] is True
        assert (
            "Invalid JSON format" in json.loads(result["content"][0]["text"])["error"]
        )
        assert result["_meta"]["error"] == "JSONDecodeError"

    @pytest.mark.asyncio
    async def test_export_to_bibtex_handler_non_list(self):
        """Test export_to_bibtex handler with non-list input"""
        non_list_json = json.dumps({"not": "a list"})

        result = await mcp_handlers.export_to_bibtex_handler(non_list_json)

        assert result["isError"] is True
        assert (
            "Expected a list of papers"
            in json.loads(result["content"][0]["text"])["error"]
        )
        assert result["_meta"]["error"] == "ValueError"

    @pytest.mark.asyncio
    async def test_export_to_bibtex_handler_export_exception(self):
        """Test export_to_bibtex handler with export function exception"""
        papers = [{"id": "test_paper"}]
        papers_json = json.dumps(papers)

        with patch(
            "mcp_handlers.export_to_bibtex", new_callable=AsyncMock
        ) as mock_export:
            mock_export.side_effect = Exception("Export failed")

            result = await mcp_handlers.export_to_bibtex_handler(papers_json)

            assert result["isError"] is True
            assert "Export failed" in json.loads(result["content"][0]["text"])["error"]


class TestDownloadHandlers:
    """Test PDF download handlers"""

    @pytest.mark.asyncio
    async def test_download_paper_pdf_handler_success(self):
        """Test successful download_paper_pdf handler"""
        expected_result = {"success": True, "download_path": "/tmp/paper.pdf"}

        with patch(
            "mcp_handlers.download_paper_pdf", new_callable=AsyncMock
        ) as mock_download:
            mock_download.return_value = expected_result

            result = await mcp_handlers.download_paper_pdf_handler(
                "2401.12345", "/tmp/"
            )

            assert result == expected_result
            mock_download.assert_called_once_with("2401.12345", "/tmp/")

    @pytest.mark.asyncio
    async def test_download_paper_pdf_handler_no_path(self):
        """Test download_paper_pdf handler without download path"""
        expected_result = {"success": True, "download_path": "./paper.pdf"}

        with patch(
            "mcp_handlers.download_paper_pdf", new_callable=AsyncMock
        ) as mock_download:
            mock_download.return_value = expected_result

            result = await mcp_handlers.download_paper_pdf_handler("2401.12345")

            assert result == expected_result
            mock_download.assert_called_once_with("2401.12345", None)

    @pytest.mark.asyncio
    async def test_download_paper_pdf_handler_exception(self):
        """Test download_paper_pdf handler exception handling"""
        with patch(
            "mcp_handlers.download_paper_pdf", new_callable=AsyncMock
        ) as mock_download:
            mock_download.side_effect = Exception("Download failed")

            result = await mcp_handlers.download_paper_pdf_handler("invalid_id")

            assert result["isError"] is True
            assert (
                "Download failed" in json.loads(result["content"][0]["text"])["error"]
            )
            assert result["_meta"]["tool"] == "download_paper_pdf"

    @pytest.mark.asyncio
    async def test_get_pdf_url_handler_success(self):
        """Test successful get_pdf_url handler"""
        expected_result = {
            "success": True,
            "pdf_url": "https://arxiv.org/pdf/2401.12345.pdf",
        }

        with patch("mcp_handlers.get_pdf_url", new_callable=AsyncMock) as mock_url:
            mock_url.return_value = expected_result

            result = await mcp_handlers.get_pdf_url_handler("2401.12345")

            assert result == expected_result
            mock_url.assert_called_once_with("2401.12345")

    @pytest.mark.asyncio
    async def test_get_pdf_url_handler_exception(self):
        """Test get_pdf_url handler exception handling"""
        with patch("mcp_handlers.get_pdf_url", new_callable=AsyncMock) as mock_url:
            mock_url.side_effect = Exception("URL generation failed")

            result = await mcp_handlers.get_pdf_url_handler("invalid_id")

            assert result["isError"] is True
            assert (
                "URL generation failed"
                in json.loads(result["content"][0]["text"])["error"]
            )
            assert result["_meta"]["tool"] == "get_pdf_url"

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_handler_success(self):
        """Test successful download_multiple_pdfs handler"""
        arxiv_ids = ["2401.12345", "2401.12346"]
        arxiv_ids_json = json.dumps(arxiv_ids)
        expected_result = {"success": True, "downloads": 2}

        with patch(
            "mcp_handlers.download_multiple_pdfs", new_callable=AsyncMock
        ) as mock_multi:
            mock_multi.return_value = expected_result

            result = await mcp_handlers.download_multiple_pdfs_handler(
                arxiv_ids_json, "/tmp/", 5
            )

            assert result == expected_result
            mock_multi.assert_called_once_with(arxiv_ids, "/tmp/", 5)

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_handler_default_params(self):
        """Test download_multiple_pdfs handler with default parameters"""
        arxiv_ids = ["2401.12345"]
        arxiv_ids_json = json.dumps(arxiv_ids)
        expected_result = {"success": True, "downloads": 1}

        with patch(
            "mcp_handlers.download_multiple_pdfs", new_callable=AsyncMock
        ) as mock_multi:
            mock_multi.return_value = expected_result

            result = await mcp_handlers.download_multiple_pdfs_handler(arxiv_ids_json)

            assert result == expected_result
            mock_multi.assert_called_once_with(arxiv_ids, None, 3)

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_handler_invalid_json(self):
        """Test download_multiple_pdfs handler with invalid JSON"""
        invalid_json = "not valid json"

        result = await mcp_handlers.download_multiple_pdfs_handler(invalid_json)

        assert result["isError"] is True
        assert (
            "Invalid JSON format" in json.loads(result["content"][0]["text"])["error"]
        )
        assert result["_meta"]["error"] == "JSONDecodeError"

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_handler_non_list(self):
        """Test download_multiple_pdfs handler with non-list input"""
        non_list_json = json.dumps({"not": "a list"})

        result = await mcp_handlers.download_multiple_pdfs_handler(non_list_json)

        assert result["isError"] is True
        assert (
            "Expected a list of ArXiv IDs"
            in json.loads(result["content"][0]["text"])["error"]
        )
        assert result["_meta"]["error"] == "ValueError"

    @pytest.mark.asyncio
    async def test_download_multiple_pdfs_handler_download_exception(self):
        """Test download_multiple_pdfs handler with download function exception"""
        arxiv_ids = ["2401.12345"]
        arxiv_ids_json = json.dumps(arxiv_ids)

        with patch(
            "mcp_handlers.download_multiple_pdfs", new_callable=AsyncMock
        ) as mock_multi:
            mock_multi.side_effect = Exception("Bulk download failed")

            result = await mcp_handlers.download_multiple_pdfs_handler(arxiv_ids_json)

            assert result["isError"] is True
            assert (
                "Bulk download failed"
                in json.loads(result["content"][0]["text"])["error"]
            )
            assert result["_meta"]["tool"] == "download_multiple_pdfs"


class TestErrorHandling:
    """Test error handling patterns across all handlers"""

    @pytest.mark.asyncio
    async def test_consistent_error_structure(self):
        """Test that all handlers return consistent error structure"""
        handlers_and_exceptions = [
            (mcp_handlers.search_arxiv_handler, "mcp_handlers.search_arxiv"),
            (mcp_handlers.get_recent_papers_handler, "mcp_handlers.get_recent_papers"),
            (mcp_handlers.search_by_title_handler, "mcp_handlers.search_by_title"),
            (
                mcp_handlers.search_by_abstract_handler,
                "mcp_handlers.search_by_abstract",
            ),
            (mcp_handlers.search_by_subject_handler, "mcp_handlers.search_by_subject"),
            (mcp_handlers.get_paper_details_handler, "mcp_handlers.get_paper_details"),
            (
                mcp_handlers.find_similar_papers_handler,
                "mcp_handlers.find_similar_papers",
            ),
            (
                mcp_handlers.download_paper_pdf_handler,
                "mcp_handlers.download_paper_pdf",
            ),
            (mcp_handlers.get_pdf_url_handler, "mcp_handlers.get_pdf_url"),
        ]

        for handler, mock_target in handlers_and_exceptions:
            with patch(mock_target, new_callable=AsyncMock) as mock_func:
                mock_func.side_effect = Exception("Test error")

                # Call handler with minimal required arguments
                if handler == mcp_handlers.search_date_range_handler:
                    result = await handler("2024-01-01", "2024-12-31")
                elif handler in [
                    mcp_handlers.search_by_title_handler,
                    mcp_handlers.search_by_abstract_handler,
                    mcp_handlers.search_papers_by_author_handler,
                ]:
                    result = await handler("test query")
                else:
                    result = await handler("test_id")

                # Verify consistent error structure
                assert result["isError"] is True
                assert "content" in result
                assert len(result["content"]) == 1
                assert "text" in result["content"][0]
                assert "_meta" in result
                assert "tool" in result["_meta"]
                assert "error" in result["_meta"]

                # Verify error message is properly JSON encoded
                error_data = json.loads(result["content"][0]["text"])
                assert "error" in error_data
                assert "Test error" in error_data["error"]
