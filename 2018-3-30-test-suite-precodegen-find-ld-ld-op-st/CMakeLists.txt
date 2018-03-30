# Hand-picked benchmarks.
set(benchmarks "${BENCHMARKS_DIR}/MultiSource/Benchmarks/7zip/7zip-benchmark.0.0.preopt.bc")

file(GLOB_RECURSE multisource_benchmarks "${BENCHMARKS_DIR}/MultiSource/Benchmarks/*preopt*.bc")
add_benchmark_group("2018-3-30" "${multisource_benchmarks}" "-find-ld-ld-op-st" "${PASS_LIBS_DIR}/libLdLdOpSt.so")

