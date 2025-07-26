import pytest
import os
import tempfile
import sys
from unittest.mock import patch

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from capabilities.compression_base import compress_file


@pytest.fixture
def sample_file():
    # create a temporary file with some content
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content\n" * 100)
    yield f.name
    os.unlink(f.name)


# test successful compression of a file
@pytest.mark.asyncio
async def test_compress_success(sample_file):
    result = await compress_file(sample_file)
    assert isinstance(result, dict)
    assert not result["isError"]
    assert result["_meta"]["tool"] == "compress_file"
    assert os.path.exists(result["_meta"]["compressed_file"])
    os.unlink(result["_meta"]["compressed_file"])


# test compression of non-existent file
@pytest.mark.asyncio
async def test_compress_nonexistent_file():
    with pytest.raises(Exception) as exc_info:
        await compress_file("nonexistent_file.txt")
    assert "File not found" in str(exc_info.value)


# test compression of empty file
@pytest.mark.asyncio
async def test_compress_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("")
    try:
        result = await compress_file(f.name)
        assert isinstance(result, dict)
        assert not result["isError"]
        assert result["_meta"]["tool"] == "compress_file"
        # Empty file should still compress successfully
        assert os.path.exists(result["_meta"]["compressed_file"])
        os.unlink(result["_meta"]["compressed_file"])
    finally:
        os.unlink(f.name)


# test compression with permission error
@pytest.mark.asyncio
async def test_compress_permission_error():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")

    try:
        # Mock open to raise PermissionError
        with patch(
            "builtins.open", side_effect=PermissionError("Permission denied: test")
        ):
            with pytest.raises(Exception) as exc_info:
                await compress_file(f.name)
            assert "Permission denied" in str(exc_info.value)
    finally:
        if os.path.exists(f.name):
            os.unlink(f.name)


# test compression with generic exception during file operations
@pytest.mark.asyncio
async def test_compress_generic_error():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")

    try:
        # Mock gzip.open to raise a generic exception
        with patch("gzip.open", side_effect=OSError("Disk full")):
            with pytest.raises(Exception) as exc_info:
                await compress_file(f.name)
            assert "Compression failed" in str(exc_info.value)
    finally:
        if os.path.exists(f.name):
            os.unlink(f.name)


# test compression with zero-byte file specifically
@pytest.mark.asyncio
async def test_compress_zero_byte_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        pass  # Create completely empty file

    try:
        result = await compress_file(f.name)
        assert isinstance(result, dict)
        assert not result["isError"]
        assert result["_meta"]["original_size"] == 0
        assert result["_meta"]["compression_ratio"] == 0.0
        assert os.path.exists(result["_meta"]["compressed_file"])
        os.unlink(result["_meta"]["compressed_file"])
    finally:
        os.unlink(f.name)


# test logging output during successful compression
@pytest.mark.asyncio
async def test_compress_logging():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content for logging\n" * 10)

    try:
        with patch("capabilities.compression_base.logger") as mock_logger:
            result = await compress_file(f.name)

            # Verify info logging was called for successful compression
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            assert "Successfully compressed" in call_args
            assert f.name in call_args

            os.unlink(result["_meta"]["compressed_file"])
    finally:
        os.unlink(f.name)


# test error logging for file not found
@pytest.mark.asyncio
async def test_compress_error_logging_file_not_found():
    with patch("capabilities.compression_base.logger") as mock_logger:
        with pytest.raises(Exception):
            await compress_file("nonexistent_file.txt")

        # Verify error logging was called
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args[0][0]
        assert "File not found" in call_args


# test error logging for permission error
@pytest.mark.asyncio
async def test_compress_error_logging_permission():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")

    try:
        with patch("capabilities.compression_base.logger") as mock_logger:
            with patch(
                "builtins.open", side_effect=PermissionError("Permission denied")
            ):
                with pytest.raises(Exception):
                    await compress_file(f.name)

                # Verify error logging was called
                mock_logger.error.assert_called_once()
                call_args = mock_logger.error.call_args[0][0]
                assert "Permission denied" in call_args
    finally:
        if os.path.exists(f.name):
            os.unlink(f.name)


# test error logging for generic error
@pytest.mark.asyncio
async def test_compress_error_logging_generic():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("test content")

    try:
        with patch("capabilities.compression_base.logger") as mock_logger:
            with patch("gzip.open", side_effect=OSError("Generic error")):
                with pytest.raises(Exception):
                    await compress_file(f.name)

                # Verify error logging was called
                mock_logger.error.assert_called_once()
                call_args = mock_logger.error.call_args[0][0]
                assert "Compression failed" in call_args
    finally:
        if os.path.exists(f.name):
            os.unlink(f.name)
