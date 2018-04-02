file(GLOB_RECURSE multisource_applications "${BENCHMARKS_DIR}/MultiSource/Applications/*preopt*.bc")
add_benchmark_group("multisource-applications-find-ld-ld-op-st"
                    "${multisource_applications}"
                    "-find-ld-ld-op-st"
                    "${PASS_LIBS_DIR}/libLdLdOpSt.so"
                    ""
                    "${CMAKE_SOURCE_DIR}/utils/parse-find-ld-ld-op-st-results.py")

