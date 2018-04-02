file(GLOB_RECURSE multisource_applications "${BENCHMARKS_DIR}/MultiSource/Applications/*preopt*.bc")
add_benchmark_group("multisource-applications-all-find-pim-subgraphs"
                    "${multisource_applications}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    ""
                    "") # TODO no parser for now.

