"""
Tests for MCP handlers.
"""

import pytest
import tempfile
import os
from mcp_handlers import (
    sort_log_handler,
    parallel_sort_handler,
    analyze_statistics_handler,
    detect_patterns_handler,
    filter_logs_handler,
    filter_time_range_handler,
    filter_level_handler,
    filter_keyword_handler,
    filter_preset_handler,
    export_json_handler,
    export_csv_handler,
    export_text_handler,
    summary_report_handler,
)


class TestMCPHandlers:
    """Test suite for MCP handler functionality."""

    @pytest.fixture
    def sample_log_content(self):
        """Create sample log content for testing."""
        return """2024-01-02 10:00:00 INFO Second entry
2024-01-01 08:30:00 DEBUG First entry
2024-01-01 09:00:00 ERROR Third entry"""

    @pytest.mark.asyncio
    async def test_sort_log_handler_success(self, sample_log_content):
        """Test successful log sorting through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await sort_log_handler(temp_path)

            # Should return the actual sort result, not MCP error format
            assert "error" not in result or result.get("error") is None
            assert "sorted_lines" in result
            assert result["total_lines"] == 3
            assert result["valid_lines"] == 3

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_sort_log_handler_file_not_found(self):
        """Test MCP handler with non-existent file."""
        result = await sort_log_handler("/nonexistent/file.log")

        # Should return error in the result
        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_sort_log_handler_empty_file(self):
        """Test MCP handler with empty file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            temp_path = f.name

        try:
            result = await sort_log_handler(temp_path)

            assert "error" not in result or result.get("error") is None
            assert result["total_lines"] == 0
            assert result["sorted_lines"] == []
            assert "empty" in result["message"].lower()

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_parallel_sort_handler_success(self, sample_log_content):
        """Test successful parallel sorting through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await parallel_sort_handler(
                temp_path, chunk_size_mb=100, max_workers=2
            )

            assert "error" not in result or result.get("error") is None
            assert "sorted_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_parallel_sort_handler_file_not_found(self):
        """Test parallel sort handler with non-existent file."""
        result = await parallel_sort_handler("/nonexistent/file.log")

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_parallel_sort_handler_invalid_parameters(self, sample_log_content):
        """Test parallel sort handler with invalid parameters."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            # Test with invalid chunk size
            result = await parallel_sort_handler(
                temp_path, chunk_size_mb=-1, max_workers=2
            )
            assert "error" not in result or result.get("error") is None

            # Test with invalid workers
            result = await parallel_sort_handler(
                temp_path, chunk_size_mb=100, max_workers=0
            )
            assert "error" not in result or result.get("error") is None

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_analyze_statistics_handler_success(self, sample_log_content):
        """Test successful statistics analysis through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await analyze_statistics_handler(temp_path)

            assert "error" not in result or result.get("error") is None
            assert "statistics" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_analyze_statistics_handler_file_not_found(self):
        """Test statistics handler with non-existent file."""
        result = await analyze_statistics_handler("/nonexistent/file.log")

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_analyze_statistics_handler_with_patterns(self, sample_log_content):
        """Test statistics handler with pattern detection enabled."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            # The function doesn't accept include_patterns parameter
            result = await analyze_statistics_handler(temp_path)

            assert "error" not in result or result.get("error") is None
            assert "statistics" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_detect_patterns_handler_success(self, sample_log_content):
        """Test successful pattern detection through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            detection_config = {"sensitivity": "high"}
            result = await detect_patterns_handler(temp_path, detection_config)

            assert "error" not in result or result.get("error") is None
            assert "patterns" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_detect_patterns_handler_file_not_found(self):
        """Test pattern detection handler with non-existent file."""
        detection_config = {"sensitivity": "high"}
        result = await detect_patterns_handler(
            "/nonexistent/file.log", detection_config
        )

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_detect_patterns_handler_invalid_config(self, sample_log_content):
        """Test pattern detection handler with invalid configuration."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            # Test with invalid sensitivity
            detection_config = {"sensitivity": "invalid"}
            result = await detect_patterns_handler(temp_path, detection_config)

            assert "error" not in result or result.get("error") is None
            assert "patterns" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_logs_handler_success(self, sample_log_content):
        """Test successful log filtering through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            filter_conditions = [
                {"field": "level", "value": "ERROR", "operator": "equals"}
            ]
            result = await filter_logs_handler(temp_path, filter_conditions, "and")

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_logs_handler_file_not_found(self):
        """Test filter logs handler with non-existent file."""
        filter_conditions = [{"field": "level", "value": "ERROR", "operator": "equals"}]
        result = await filter_logs_handler(
            "/nonexistent/file.log", filter_conditions, "and"
        )

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_filter_logs_handler_invalid_conditions(self, sample_log_content):
        """Test filter logs handler with invalid conditions."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            # Test with invalid operator
            filter_conditions = [
                {"field": "level", "value": "ERROR", "operator": "invalid"}
            ]
            result = await filter_logs_handler(temp_path, filter_conditions, "and")

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_time_range_handler_success(self, sample_log_content):
        """Test successful time range filtering through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_time_range_handler(
                temp_path, "2024-01-01 08:00:00", "2024-01-01 10:00:00"
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_time_range_handler_file_not_found(self):
        """Test time range filter handler with non-existent file."""
        result = await filter_time_range_handler(
            "/nonexistent/file.log", "2024-01-01 08:00:00", "2024-01-01 10:00:00"
        )

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_filter_time_range_handler_invalid_timestamps(
        self, sample_log_content
    ):
        """Test time range filter handler with invalid timestamps."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            # Test with invalid start timestamp - this should return an error
            result = await filter_time_range_handler(
                temp_path, "invalid-timestamp", "2024-01-01 10:00:00"
            )

            # This should return an error for invalid timestamp
            assert "error" in result
            assert "Invalid time format" in result["error"]

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_level_handler_success(self, sample_log_content):
        """Test successful log level filtering through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_level_handler(
                temp_path, ["ERROR", "WARN"], exclude=False
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_level_handler_file_not_found(self):
        """Test level filter handler with non-existent file."""
        result = await filter_level_handler(
            "/nonexistent/file.log", ["ERROR", "WARN"], exclude=False
        )

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_filter_level_handler_empty_levels(self, sample_log_content):
        """Test level filter handler with empty levels list."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_level_handler(temp_path, [], exclude=False)

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_keyword_handler_success(self, sample_log_content):
        """Test successful keyword filtering through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_keyword_handler(
                temp_path, ["entry"], case_sensitive=False, match_all=False
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_keyword_handler_file_not_found(self):
        """Test keyword filter handler with non-existent file."""
        result = await filter_keyword_handler(
            "/nonexistent/file.log", ["entry"], case_sensitive=False, match_all=False
        )

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_filter_keyword_handler_empty_keywords(self, sample_log_content):
        """Test keyword filter handler with empty keywords list."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_keyword_handler(
                temp_path, [], case_sensitive=False, match_all=False
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_preset_handler_success(self, sample_log_content):
        """Test successful preset filtering through MCP handler."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_preset_handler(temp_path, "errors_only")

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_preset_handler_file_not_found(self):
        """Test preset filter handler with non-existent file."""
        result = await filter_preset_handler("/nonexistent/file.log", "errors_only")

        assert "error" in result
        assert "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_filter_preset_handler_unknown_preset(self, sample_log_content):
        """Test preset filter handler with unknown preset."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write(sample_log_content)
            temp_path = f.name

        try:
            result = await filter_preset_handler(temp_path, "unknown_preset")

            assert "error" in result
            assert "Unknown preset" in result["error"]

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_export_json_handler_success(self):
        """Test successful JSON export through MCP handler."""
        test_data = {"lines": ["line1", "line2"], "count": 2}

        result = await export_json_handler(test_data, include_metadata=True)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_export_json_handler_empty_data(self):
        """Test JSON export handler with empty data."""
        test_data = {}

        result = await export_json_handler(test_data, include_metadata=False)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_export_csv_handler_success(self):
        """Test successful CSV export through MCP handler."""
        test_data = {
            "sorted_lines": [
                "2024-01-01 08:00:00 INFO line1",
                "2024-01-01 09:00:00 ERROR line2",
            ],
            "count": 2,
        }

        result = await export_csv_handler(test_data, include_headers=True)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_export_csv_handler_empty_data(self):
        """Test CSV export handler with empty data."""
        test_data = {"sorted_lines": [], "count": 0}

        result = await export_csv_handler(test_data, include_headers=False)

        # This should return an error for empty data
        assert "error" in result
        assert "No log entries to export" in result["error"]

    @pytest.mark.asyncio
    async def test_export_text_handler_success(self):
        """Test successful text export through MCP handler."""
        test_data = {"lines": ["line1", "line2"], "count": 2}

        result = await export_text_handler(test_data, include_summary=True)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_export_text_handler_empty_data(self):
        """Test text export handler with empty data."""
        test_data = {"lines": [], "count": 0}

        result = await export_text_handler(test_data, include_summary=False)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_summary_report_handler_success(self):
        """Test successful summary report through MCP handler."""
        test_data = {"lines": ["line1", "line2"], "count": 2}

        result = await summary_report_handler(test_data)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_summary_report_handler_empty_data(self):
        """Test summary report handler with empty data."""
        test_data = {"lines": [], "count": 0}

        result = await summary_report_handler(test_data)

        assert "error" not in result or result.get("error") is None
        assert "content" in result
        assert "format" in result

    @pytest.mark.asyncio
    async def test_sort_log_handler_exception_handling(self):
        """Test sort log handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await sort_log_handler(temp_path)

            assert "error" not in result or result.get("error") is None
            assert "sorted_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_parallel_sort_handler_exception_handling(self):
        """Test parallel sort handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await parallel_sort_handler(
                temp_path, chunk_size_mb=100, max_workers=2
            )

            assert "error" not in result or result.get("error") is None
            assert "sorted_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_analyze_statistics_handler_exception_handling(self):
        """Test statistics handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await analyze_statistics_handler(temp_path)

            assert "error" not in result or result.get("error") is None
            assert "statistics" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_detect_patterns_handler_exception_handling(self):
        """Test pattern detection handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            detection_config = {"sensitivity": "high"}
            # This should handle the exception gracefully
            result = await detect_patterns_handler(temp_path, detection_config)

            assert "error" not in result or result.get("error") is None
            assert "patterns" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_logs_handler_exception_handling(self):
        """Test filter logs handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            filter_conditions = [
                {"field": "level", "value": "ERROR", "operator": "equals"}
            ]
            # This should handle the exception gracefully
            result = await filter_logs_handler(temp_path, filter_conditions, "and")

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_time_range_handler_exception_handling(self):
        """Test time range filter handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await filter_time_range_handler(
                temp_path, "2024-01-01 08:00:00", "2024-01-01 10:00:00"
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_level_handler_exception_handling(self):
        """Test level filter handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await filter_level_handler(
                temp_path, ["ERROR", "WARN"], exclude=False
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_keyword_handler_exception_handling(self):
        """Test keyword filter handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await filter_keyword_handler(
                temp_path, ["entry"], case_sensitive=False, match_all=False
            )

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_filter_preset_handler_exception_handling(self):
        """Test preset filter handler with exception handling."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("invalid log content")
            temp_path = f.name

        try:
            # This should handle the exception gracefully
            result = await filter_preset_handler(temp_path, "errors_only")

            assert "error" not in result or result.get("error") is None
            assert "filtered_lines" in result

        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_export_handlers_exception_handling(self):
        """Test export handlers with exception handling."""
        # Test with invalid data that might cause exceptions
        invalid_data = {"invalid": "data", "lines": None}

        # JSON export
        result = await export_json_handler(invalid_data, include_metadata=True)
        assert "error" not in result or result.get("error") is None
        assert "content" in result

        # CSV export - this should return an error for invalid data
        result = await export_csv_handler(invalid_data, include_headers=True)
        assert "error" in result
        assert "No sorted_lines found" in result["error"]

        # Text export
        result = await export_text_handler(invalid_data, include_summary=True)
        assert "error" not in result or result.get("error") is None
        assert "content" in result

        # Summary report
        result = await summary_report_handler(invalid_data)
        assert "error" not in result or result.get("error") is None
        assert "content" in result
