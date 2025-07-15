cmake_minimum_required(VERSION 3.10)
project(MathAnalysisMCP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)

# Source files
set(SOURCES
    src/main.cpp
    src/mcp_server.cpp
    src/math_operations.cpp
    src/json.cpp
)

# Create executable
add_executable(math_analysis_server ${SOURCES})

# Compiler flags
target_compile_options(math_analysis_server PRIVATE -Wall -Wextra -O2)

# Link math library
target_link_libraries(math_analysis_server m)

# Set output directory
set_target_properties(math_analysis_server PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)