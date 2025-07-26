"""
Unit tests for mcp_handlers module.

Covers:
 - list_resources() returning correct resource count
 - call_tool dispatch for filter_csv, list_hdf5, node_hardware
 - Unknown‑tool error handling
 - Error handling paths and exception cases
 - Async handler functions
"""

import os
import sys
import json
import pytest
import tempfile
import h5py

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import mcp_handlers


def test_list_resources():
    print("\n=== Running test_list_resources ===")
    res = mcp_handlers.list_resources()
    print("Resources returned:", res)
    assert res["_meta"]["count"] == 3


def test_call_tool_filter(tmp_path):
    print("\n=== Running test_call_tool_filter ===")
    csv = tmp_path / "t.csv"
    csv.write_text("id,value\n1,10\n2,100\n")
    params = {"tool": "filter_csv", "csv_path": str(csv), "threshold": 50}
    print(f"Calling filter_csv with params: {params}")
    result = mcp_handlers.call_tool("filter_csv", params)
    print("Raw handler result:", result)
    data = json.loads(result["content"][0]["text"])
    print("Parsed JSON data:", data)
    assert data[0]["value"] == 100


def test_call_tool_list_hdf5(tmp_path):
    print("\n=== Running test_call_tool_list_hdf5 ===")
    d = tmp_path / "d"
    d.mkdir()
    (d / "x.hdf5").write_text("")
    params = {"tool": "list_hdf5", "directory": str(d)}
    print(f"Calling list_hdf5 with params: {params}")
    res = mcp_handlers.call_tool("list_hdf5", params)
    print("Raw handler result:", res)
    files = json.loads(res["content"][0]["text"])
    print("Parsed file list:", files)
    assert len(files) == 1


def test_call_tool_node_hardware():
    print("=== Running test_call_tool_node_hardware ===")
    result = mcp_handlers.call_tool("node_hardware", {"tool": "node_hardware"})
    print("Raw result:", result)
    data = json.loads(result["content"][0]["text"])
    print("Parsed data:", data)
    import os
    import psutil

    logical = psutil.cpu_count(logical=True) or os.cpu_count()
    physical = psutil.cpu_count(logical=False)
    print(f"Expected logical={logical}, physical={physical}")
    assert data["logical_cores"] == logical
    assert data["physical_cores"] == physical


def test_unknown_tool():
    print("\n=== Running test_unknown_tool ===")
    with pytest.raises(Exception) as excinfo:
        mcp_handlers.call_tool("bad", {})
    print("Caught exception:", excinfo.value)


def test_call_tool_filter_missing_params():
    """Test filter_csv with missing parameters."""
    print("\n=== Running test_call_tool_filter_missing_params ===")

    # Test missing csv_path
    result = mcp_handlers.call_tool("filter_csv", {"threshold": 50})
    print("Missing csv_path result:", result)
    assert result["isError"] is True
    assert (
        "Missing required parameters"
        in json.loads(result["content"][0]["text"])["error"]
    )

    # Test missing threshold
    result = mcp_handlers.call_tool("filter_csv", {"csv_path": "test.csv"})
    print("Missing threshold result:", result)
    assert result["isError"] is True
    assert (
        "Missing required parameters"
        in json.loads(result["content"][0]["text"])["error"]
    )


def test_list_hdf5_files_sync_error():
    """Test list_hdf5_files_sync error handling."""
    print("\n=== Running test_list_hdf5_files_sync_error ===")

    # Test with non-existent directory
    result = mcp_handlers.list_hdf5_files_sync("nonexistent_directory")
    print("Error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] == "FileNotFoundError"


def test_filter_csv_sync_file_not_found():
    """Test filter_csv_sync with non-existent file."""
    print("\n=== Running test_filter_csv_sync_file_not_found ===")

    result = mcp_handlers.filter_csv_sync("nonexistent.csv", 50.0)
    print("File not found result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] == "FileNotFoundError"
    assert "File not found" in json.loads(result["content"][0]["text"])["error"]


def test_filter_csv_sync_value_error(tmp_path):
    """Test filter_csv_sync with invalid data types."""
    print("\n=== Running test_filter_csv_sync_value_error ===")

    # Create CSV with non-numeric values
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text("id,value\n1,abc\n2,def\n3,100\n")

    result = mcp_handlers.filter_csv_sync(str(csv_file), 50.0)
    print("Value error result:", result)
    # Should succeed but skip invalid rows
    assert "isError" not in result or not result.get("isError")
    data = json.loads(result["content"][0]["text"])
    assert len(data) == 1  # Only the row with value 100 should be included
    assert data[0]["value"] == 100.0


def test_filter_csv_sync_general_error(tmp_path):
    """Test filter_csv_sync with general error (permission denied simulation)."""
    print("\n=== Running test_filter_csv_sync_general_error ===")

    # Create a file and then make directory instead (this should cause an error)
    csv_file = tmp_path / "directory.csv"
    csv_file.mkdir()  # Create as directory instead of file

    result = mcp_handlers.filter_csv_sync(str(csv_file), 50.0)
    print("General error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] in ["IsADirectoryError", "PermissionError"]


def test_node_hardware_sync_error(monkeypatch):
    """Test node_hardware_sync error handling."""
    print("\n=== Running test_node_hardware_sync_error ===")

    # Mock psutil to raise an exception
    def mock_cpu_count(logical=True):
        raise RuntimeError("Mocked CPU count error")

    monkeypatch.setattr("psutil.cpu_count", mock_cpu_count)

    result = mcp_handlers.node_hardware_sync()
    print("Hardware error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] == "RuntimeError"


@pytest.mark.asyncio
async def test_list_hdf5_files_async_success(tmp_path):
    """Test async list_hdf5_files function."""
    print("\n=== Running test_list_hdf5_files_async_success ===")

    # Create test directory with HDF5 files
    d = tmp_path / "async_test"
    d.mkdir()
    (d / "test1.h5").write_text("")
    (d / "test2.hdf5").write_text("")

    result = await mcp_handlers.list_hdf5_files(str(d))
    print("Async list result:", result)
    assert isinstance(result, list)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_list_hdf5_files_async_error():
    """Test async list_hdf5_files error handling."""
    print("\n=== Running test_list_hdf5_files_async_error ===")

    result = await mcp_handlers.list_hdf5_files("nonexistent_async_dir")
    print("Async error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] == "FileNotFoundError"


@pytest.mark.asyncio
async def test_inspect_hdf5_handler_success():
    """Test async inspect_hdf5_handler function."""
    print("\n=== Running test_inspect_hdf5_handler_success ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create a test HDF5 file
        with h5py.File(fname, "w") as f:
            f.create_dataset("test_data", data=[1, 2, 3])
            f.create_group("test_group")

        result = await mcp_handlers.inspect_hdf5_handler(fname)
        print("Inspect success result:", result)
        assert "result" in result
        assert "DATASET /test_data" in result["result"]
        assert "GROUP   /test_group/" in result["result"]

    finally:
        os.unlink(fname)


@pytest.mark.asyncio
async def test_inspect_hdf5_handler_error():
    """Test async inspect_hdf5_handler error handling."""
    print("\n=== Running test_inspect_hdf5_handler_error ===")

    result = await mcp_handlers.inspect_hdf5_handler("nonexistent.h5")
    print("Inspect error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] in ["OSError", "FileNotFoundError"]


@pytest.mark.asyncio
async def test_preview_hdf5_handler_success():
    """Test async preview_hdf5_handler function."""
    print("\n=== Running test_preview_hdf5_handler_success ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create a test HDF5 file
        with h5py.File(fname, "w") as f:
            f.create_dataset("test_data", data=list(range(20)))

        result = await mcp_handlers.preview_hdf5_handler(fname, 5)
        print("Preview success result:", result)
        assert "test_data" in result
        assert len(result["test_data"]) == 5
        assert result["test_data"] == [0, 1, 2, 3, 4]

    finally:
        os.unlink(fname)


@pytest.mark.asyncio
async def test_preview_hdf5_handler_error():
    """Test async preview_hdf5_handler error handling."""
    print("\n=== Running test_preview_hdf5_handler_error ===")

    result = await mcp_handlers.preview_hdf5_handler("nonexistent.h5")
    print("Preview error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] in ["OSError", "FileNotFoundError"]


@pytest.mark.asyncio
async def test_read_all_hdf5_handler_success():
    """Test async read_all_hdf5_handler function."""
    print("\n=== Running test_read_all_hdf5_handler_success ===")

    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        fname = tmp.name

    try:
        # Create a test HDF5 file
        with h5py.File(fname, "w") as f:
            f.create_dataset("test_data", data=[1, 2, 3, 4, 5])
            f.create_dataset("other_data", data=[10, 20])

        result = await mcp_handlers.read_all_hdf5_handler(fname)
        print("Read all success result:", result)
        assert "test_data" in result
        assert "other_data" in result
        assert result["test_data"] == [1, 2, 3, 4, 5]
        assert result["other_data"] == [10, 20]

    finally:
        os.unlink(fname)


@pytest.mark.asyncio
async def test_read_all_hdf5_handler_error():
    """Test async read_all_hdf5_handler error handling."""
    print("\n=== Running test_read_all_hdf5_handler_error ===")

    result = await mcp_handlers.read_all_hdf5_handler("nonexistent.h5")
    print("Read all error result:", result)
    assert result["isError"] is True
    assert result["_meta"]["error"] in ["OSError", "FileNotFoundError"]
