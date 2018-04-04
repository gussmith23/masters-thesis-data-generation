add_benchmark_group("multisource-benchmarks-selected-find-pim-subgraphs"
                    "${multisource_benchmarks_selected}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    ""
                    "${CMAKE_SOURCE_DIR}/utils/parse-find-pim-subgraphs-results.py")

