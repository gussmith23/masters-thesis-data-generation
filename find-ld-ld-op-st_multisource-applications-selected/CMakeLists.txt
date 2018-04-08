add_benchmark_group("find-ld-ld-op-st_multisource-applications-selected"
                    "${multisource_applications_selected}"
                    "-find-ld-ld-op-st"
                    "${PASS_LIBS_DIR}/libLdLdOpSt.so"
                    ""
                    "${CMAKE_SOURCE_DIR}/utils/parse-find-ld-ld-op-st-results.py")

