cmake_minimum_required(VERSION 3.20)
project(SentientQuantumArchitecture
    VERSION 8.0.0
    DESCRIPTION "SQA v8.0 — Cognitive Neural Overlay, A1 Filing System, Nexus Node Stack"
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# --- Dependencies -----------------------------------------------------------
find_package(nlohmann_json 3.11 REQUIRED)
find_package(spdlog REQUIRED)
find_package(pybind11 REQUIRED)

# --- Core static library (CNO + A1FS + NNS) --------------------------------
add_library(sqa_core STATIC
    src/cno/cognitive_neural_overlay.cpp
    src/cno/symbolic_processor.cpp
    src/cno/appraisal_engine.cpp
    src/cno/attention_module.cpp
    src/cno/creativity_engine.cpp
    src/a1fs/a1_filing_system.cpp
    src/a1fs/knowledge_vault.cpp
    src/a1fs/memory_node.cpp
    src/a1fs/consolidation_engine.cpp
    src/nns/nexus_node_stack.cpp
    src/nns/processing_node.cpp
    src/nns/feedback_controller.cpp
    src/config_loader.cpp
)

target_include_directories(sqa_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_link_libraries(sqa_core PUBLIC
    nlohmann_json::nlohmann_json
    spdlog::spdlog
)

# --- pybind11 Python module -------------------------------------------------
pybind11_add_module(sqa_engine bindings/sqa_module.cpp)
target_link_libraries(sqa_engine PRIVATE sqa_core)

# --- Tests ------------------------------------------------------------------
option(SQA_BUILD_TESTS "Build SQA tests" ON)
if(SQA_BUILD_TESTS)
    enable_testing()
    find_package(GTest REQUIRED)

    add_executable(sqa_tests
        tests/test_cno.cpp
        tests/test_a1fs.cpp
        tests/test_nns.cpp
        tests/test_config.cpp
    )
    target_link_libraries(sqa_tests PRIVATE sqa_core GTest::gtest GTest::gtest_main)
    add_test(NAME sqa_tests COMMAND sqa_tests)
endif()

# --- Install ----------------------------------------------------------------
install(TARGETS sqa_engine DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)
