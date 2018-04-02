add_benchmark_group("multisource-applications-c-find-pim-subgraphs"
                    "${multisource_applications_c}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    "") # TODO no parser for now.
