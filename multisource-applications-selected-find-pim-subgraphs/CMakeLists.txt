add_benchmark_group("multisource-applications-selected-find-pim-subgraphs"
                    "${multisource_applications_selected}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    ""
                    "${CMAKE_SOURCE_DIR}/utils/parse-find-pim-subgraphs-results.py")

