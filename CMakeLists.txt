cmake_minimum_required(VERSION 3.0)
project(results)

find_package(LLVM REQUIRED CONFIG)

# Build https://github.com/gussmith23/llvm-pim-passes to get these passes.
set(PASS_LIBS_DIR "" CACHE PATH "Path to LLVM passes") 
if("${PASS_LIBS_DIR}" STREQUAL "")
  message(FATAL_ERROR "PASS_LIBS_DIR unset")
  return()
endif()

set(BENCHMARKS_DIR "" CACHE PATH "Root directory to search for monolithic .bc files") 
if("${BENCHMARKS_DIR}" STREQUAL "")
  message(FATAL_ERROR "BENCHMARKS_DIR unset")
  return()
endif()

# TODO finding this not too useful for now.
# See https://github.com/gussmith23/llvm-benchmarks
# and https://github.com/gussmith23/test-suite/commit/b39d483ae23f685f50af8535761d1ce0bea7cf4a
#if(NOT all_benchmarks)
#  message(STATUS "Collecting benchmarks...")
#  file(GLOB_RECURSE all_benchmarks "${BENCHMARKS_DIR}/*preopt*.bc")
#  list(LENGTH all_benchmarks num_benchmarks)
#  message(STATUS "Found ${num_benchmarks} benchmarks.")
#endif()

# Collect useful groups of benchmarks/applications.
# Just C benchmarks from MultiSource/Applications
set(multisource_applications_c
    "${BENCHMARKS_DIR}/MultiSource/Applications/sgefa/sgefa.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/aha/aha.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/lua/lua.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/ClamAV/clamscan.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/ALAC/encode/alacconvert-encode.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/ALAC/decode/alacconvert-decode.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/Burg/burg.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/lemon/lemon.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/oggenc/oggenc.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/JM/ldecod/ldecod.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/JM/lencod/lencod.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/treecc/treecc.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/sqlite3/sqlite3.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/obsequi/Obsequi.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/viterbi/viterbi.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/spiff/spiff.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/SPASS/SPASS.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/siod/siod.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/SIBsim4/SIBsim4.0.0.preopt.bc"
    "${BENCHMARKS_DIR}/MultiSource/Applications/d/make_dparser.0.0.preopt.bc"
    )

# These application/benchmark groups were selected because they had the most
# initial PIM patterns. It seems like a somewhat diverse sample, so i stuck with
# it.
set(multisource_applications_selected
  "${BENCHMARKS_DIR}/MultiSource/Applications/JM/lencod/lencod.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/ClamAV/clamscan.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/oggenc/oggenc.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/JM/ldecod/ldecod.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/ALAC/decode/alacconvert-decode.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/ALAC/encode/alacconvert-encode.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/SIBsim4/SIBsim4.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/sqlite3/sqlite3.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/SPASS/SPASS.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Applications/obsequi/Obsequi.0.0.preopt.bc"
  )
set(multisource_benchmarks_selected
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/7zip/7zip-benchmark.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/Prolangs-C/TimberWolfMC/timberwolfmc.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/ASCI_Purple/SMG2000/smg2000.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/MiBench/consumer-jpeg/consumer-jpeg.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/mediabench/jpeg/jpeg-6a/cjpeg.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/DOE-ProxyApps-C++/CLAMR/CLAMR.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/MallocBench/espresso/espresso.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/mafft/pairlocalalign.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/Prolangs-C/agrep/agrep.0.0.preopt.bc"
  "${BENCHMARKS_DIR}/MultiSource/Benchmarks/MallocBench/gs/gs.0.0.preopt.bc"
  )

# Use this function to create a new group of benchmarks to be run.
# target_name: name of the target
# benchmarks_filepaths: the benchmarks to run on. Use all_benchmarks to run on
#   all benchmarks.
# pass_flag: the opt flag indicating which pass to run, e.g. -loop-unroll.
# pass_lib: the library containing the pass, to be loaded into opt via -load.
#   Use the variable PASS_LIBS_DIR to refer to the folder containing the pass
#   libraries.
# extra_flags: Extra flags to pass to opt. These can be used to send flags to
#   your pass.
function(add_benchmark_group 
    target_name 
    benchmarks_filepaths 
    pass_flag 
    pass_lib
    extra_flags 
    summarizer_script # A script which generates a summary output file
    )
  set(benchmark_outputs "") 
  foreach(benchmark_filepath ${benchmarks_filepaths})
    get_filename_component(benchmark_filename ${benchmark_filepath} NAME)
    set(output_filename "${benchmark_filename}.out.txt")
    add_custom_command(OUTPUT ${output_filename}
                        COMMAND ${LLVM_TOOLS_BINARY_DIR}/opt -load "${pass_lib}" 
                                "${pass_flag}" -analyze "${benchmark_filepath}"
                                "${extra_flags}" 
                                  > "${output_filename}" 2>/dev/null)
    list(APPEND benchmark_outputs ${output_filename})
  endforeach()
  add_custom_target("${target_name}_results" 
                    DEPENDS ${benchmark_outputs}
                            ${pass_lib}
                            ${benchmark_filepaths})
  if(NOT "${summarizer_script}" STREQUAL "")
    # I really don't think thisi s the best way to do this
    set(summary_filename "${target_name}_summary.txt")
    add_custom_command(OUTPUT "${summary_filename}"
                        DEPENDS "${benchmark_outputs}"
                        COMMAND python "${summarizer_script}" ${benchmark_outputs} 
                                  > "${summary_filename}")
    add_custom_target("${target_name}_summary" 
                      DEPENDS "${summary_filename}" 
                              "${summarizer_script}")
  endif()
  
  # TODO definitely a cleaner way to do this.
  # If we're generating a summary, the main target can depend only on the
  # summary. Otherwise, we depend on the results.
  if(NOT "${summarizer_script}" STREQUAL "")
    add_custom_target(${target_name}
                      DEPENDS "${target_name}_summary")
  else()
    add_custom_target(${target_name}
                      DEPENDS "${target_name}_results")
  endif()  
endfunction(add_benchmark_group)

add_subdirectory(./find-ld-ld-op-st_multisource-applications-selected)
add_subdirectory(./find-ld-ld-op-st_multisource-benchmarks-selected)

#add_subdirectory(./multisource-applications-all-find-pim-subgraphs)
add_subdirectory(./multisource-applications-selected-find-pim-subgraphs)
#add_subdirectory(./multisource-applications-c-find-pim-subgraphs)
#add_subdirectory(./multisource-benchmarks-all-find-pim-subgraphs)
add_subdirectory(./multisource-benchmarks-selected-find-pim-subgraphs)
