file(GLOB_RECURSE multisource_benchmarks "${BENCHMARKS_DIR}/MultiSource/Benchmarks/*preopt*.bc")
add_benchmark_group("multisource-benchmarks-find-ld-ld-op-st"
                    "${multisource_benchmarks}"
                    "-find-ld-ld-op-st"
                    "${PASS_LIBS_DIR}/libLdLdOpSt.so"
                    "${CMAKE_SOURCE_DIR}/utils/parse-find-ld-ld-op-st-results.py")
