add_benchmark_group("multisource-applications-c-find-pim-subgraphs"
                    "${multisource_applications_c}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    "-pi=and,or,xor"
                    "${CMAKE_SOURCE_DIR}/utils/parse-find-pim-subgraphs-results.py")
