# Test Coverage Improvement Plan for IOWarp MCPs

Based on my analysis of the codebase, here's a comprehensive plan to boost test coverage across all MCP modules:

## Current State Analysis

**MCPs with Tests (11 total):**
1. **Adios** - 46.9% coverage (src: 8 files, tests: 5 files) ⚠️ Missing mcp_handlers.py tests
2. **Pandas** - Has coverage report (src: 11 files, tests: 2 files) ⚠️ Implementation modules untested  
3. **Arxiv** - (src: 7 files, tests: 6 files) ✅ Good coverage
4. **Compression** - (src: 3 files, tests: 3 files) ✅ Good coverage
5. **Darshan** - (src: 3 files, tests: 2 files) ⚠️ Missing server.py tests
6. **HDF5** - (src: 6 files, tests: 3 files) ⚠️ Missing capability tests
7. **lmod** - (src: 3 files, tests: 2 files) ⚠️ Missing server.py tests
8. **Parallel_Sort** - (src: 8 files, tests: 7 files) ✅ Good coverage
9. **Plot** - (src: 3 files, tests: 5 files) ✅ Excellent coverage
10. **Slurm** - (src: 14 files, tests: 6 files) ⚠️ Many implementation modules untested
11. **parquet** - (src: 6 files, tests: 4 files) ✅ Good coverage

**MCPs without Tests (3 total):**
- **Chronolog** - No tests directory
- **Jarvis** - No tests directory  
- **Node_Hardware** - No tests directory

## Priority Improvement Plan

### Phase 1: High Priority - Critical Coverage Gaps

1. **Create missing test directories:**
   - `/mcps/Chronolog/tests/`
   - `/mcps/Jarvis/tests/`
   - `/mcps/Node_Hardware/tests/`

2. **Fix major coverage gaps in existing MCPs:**
   - **Adios**: Add tests for `mcp_handlers.py` and `server.py`
   - **Pandas**: Add tests for all 10 implementation modules
   - **Slurm**: Add tests for 8 missing implementation modules
   - **HDF5**: Add tests for 3 missing capability modules

### Phase 2: Medium Priority - Complete Coverage

3. **Add missing capability tests:**
   - **Darshan**: Test `server.py`
   - **lmod**: Test `server.py`
   - **HDF5**: Test `inspect_hdf5.py`, `preview_hdf5.py`, `read_all_hdf5.py`

### Phase 3: Low Priority - Edge Cases & Integration

4. **Enhance existing tests:**
   - Add error handling tests
   - Add integration tests
   - Add performance tests where applicable

## Implementation Strategy

### For Each MCP Module:

1. **Test Structure Pattern:**
   ```
   tests/
   ├── __init__.py
   ├── test_server.py          # Server functionality
   ├── test_mcp_handlers.py    # MCP handlers
   ├── test_<capability>.py    # Each capability module
   └── test_integration.py     # End-to-end tests
   ```

2. **Test Coverage Targets:**
   - **Minimum**: 80% line coverage
   - **Target**: 90%+ line coverage
   - **Focus Areas**: Error handling, edge cases, integration points

3. **Test Categories:**
   - **Unit Tests**: Individual function testing
   - **Integration Tests**: MCP server interaction
   - **Error Tests**: Exception handling
   - **Mock Tests**: External dependency mocking

### Quality Checks Required:

After implementing tests, run:
```bash
uv run ruff format --check .
uv run mypy src/ --ignore-missing-imports --show-error-codes --no-error-summary
uv run ruff check --output-format=github .
uv run pip-audit
```

## Detailed Coverage Analysis by MCP

### Adios MCP (Current: 46.9%)
**Source Files:**
- `src/implementation/bp5_attributes.py` ✅ Tested
- `src/implementation/bp5_read_variable_at_step.py` ✅ Tested
- `src/implementation/bp5_list.py` ✅ Tested
- `src/implementation/bp5_inspect_variables.py` ✅ Tested
- `src/implementation/bp5_inspect_variables_at_step.py` ✅ Tested
- `src/server.py` ❌ **Not tested**
- `src/mcp_handlers.py` ❌ **Not tested** (0% coverage)

**Action Required:** Add `test_server.py` and `test_mcp_handlers.py`

### Pandas MCP (Has coverage report)
**Source Files:**
- `src/implementation/memory_optimization.py` ❌ **Not tested**
- `src/implementation/data_profiling.py` ❌ **Not tested**
- `src/implementation/transformations.py` ❌ **Not tested**
- `src/implementation/time_series.py` ❌ **Not tested**
- `src/implementation/validation.py` ❌ **Not tested**
- `src/implementation/data_io.py` ❌ **Not tested**
- `src/implementation/pandas_statistics.py` ❌ **Not tested**
- `src/implementation/filtering.py` ❌ **Not tested**
- `src/implementation/data_cleaning.py` ❌ **Not tested**
- `src/implementation/output_formatter.py` ❌ **Not tested**
- `src/server.py` ✅ Tested

**Action Required:** Add tests for all 10 implementation modules

### Slurm MCP (Large module)
**Source Files:**
- `src/implementation/array_jobs.py` ❌ **Not tested**
- `src/implementation/cluster_info.py` ❌ **Not tested**
- `src/implementation/job_cancellation.py` ❌ **Not tested**
- `src/implementation/job_details.py` ❌ **Not tested**
- `src/implementation/job_listing.py` ❌ **Not tested**
- `src/implementation/job_output.py` ❌ **Not tested**
- `src/implementation/job_status.py` ❌ **Not tested**
- `src/implementation/job_submission.py` ❌ **Not tested**
- `src/implementation/node_info.py` ❌ **Not tested**
- `src/implementation/queue_info.py` ❌ **Not tested**
- `src/implementation/slurm_handler.py` ❌ **Not tested**
- `src/implementation/utils.py` ❌ **Not tested**
- `src/implementation/node_allocation.py` ✅ Tested
- `src/server.py` ✅ Tested

**Action Required:** Add tests for 12 missing implementation modules

### HDF5 MCP
**Source Files:**
- `src/capabilities/hdf5_list.py` ✅ Tested
- `src/capabilities/inspect_hdf5.py` ❌ **Not tested**
- `src/capabilities/preview_hdf5.py` ❌ **Not tested**
- `src/capabilities/read_all_hdf5.py` ❌ **Not tested**
- `src/mcp_handlers.py` ✅ Tested
- `src/server.py` ✅ Tested

**Action Required:** Add tests for 3 missing capability modules

### Node_Hardware MCP (No tests)
**Source Files (12 files):**
- `src/capabilities/cpu_info.py` ❌ **Not tested**
- `src/capabilities/disk_info.py` ❌ **Not tested**
- `src/capabilities/gpu_info.py` ❌ **Not tested**
- `src/capabilities/hardware_summary.py` ❌ **Not tested**
- `src/capabilities/memory_info.py` ❌ **Not tested**
- `src/capabilities/network_info.py` ❌ **Not tested**
- `src/capabilities/performance_monitor.py` ❌ **Not tested**
- `src/capabilities/process_info.py` ❌ **Not tested**
- `src/capabilities/remote_node_info.py` ❌ **Not tested**
- `src/capabilities/sensor_info.py` ❌ **Not tested**
- `src/capabilities/system_info.py` ❌ **Not tested**
- `src/capabilities/utils.py` ❌ **Not tested**

**Action Required:** Create complete test suite

### Chronolog MCP (No tests)
**Source Files:**
- `src/chronomcp/capabilities/record_handler.py` ❌ **Not tested**
- `src/chronomcp/capabilities/retrieve_handler.py` ❌ **Not tested**
- `src/chronomcp/capabilities/start_handler.py` ❌ **Not tested**
- `src/chronomcp/capabilities/stop_handler.py` ❌ **Not tested**
- `src/chronomcp/server.py` ❌ **Not tested**

**Action Required:** Create complete test suite

### Jarvis MCP (No tests)
**Source Files:**
- `src/capabilities/jarvis_handler.py` ❌ **Not tested**
- `src/server.py` ❌ **Not tested**

**Action Required:** Create complete test suite

## Estimated Impact

- **Current**: ~47% average coverage
- **After Phase 1**: ~75% average coverage  
- **After Phase 2**: ~85% average coverage
- **After Phase 3**: ~90%+ average coverage

## Testing Commands

### Run Coverage Analysis
```bash
uv run pytest tests/ -v --tb=short --cov=src --cov-report=xml --cov-report=html --cov-report=term
```

### Quality Checks
```bash
uv run ruff format --check .
uv run mypy src/ --ignore-missing-imports --show-error-codes --no-error-summary
uv run ruff check --output-format=github .
uv run pip-audit
```

This plan prioritizes the most critical gaps first, ensuring robust testing across all MCP modules while maintaining code quality standards.