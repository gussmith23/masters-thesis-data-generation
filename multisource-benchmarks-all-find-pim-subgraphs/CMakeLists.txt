file(GLOB_RECURSE multisource_benchmarks "${BENCHMARKS_DIR}/MultiSource/Benchmarks/*preopt*.bc")
add_benchmark_group("multisource-benchmarks-all-find-pim-subgraphs"
                    "${multisource_benchmarks}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    "") # TODO no parser for now.

