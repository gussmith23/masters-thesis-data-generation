set(multisource_applications
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/JM/lencod/lencod.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/ClamAV/clamscan.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/oggenc/oggenc.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/JM/ldecod/ldecod.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/ALAC/decode/alacconvert-decode.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/ALAC/encode/alacconvert-encode.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/SIBsim4/SIBsim4.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/sqlite3/sqlite3.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/SPASS/SPASS.0.0.preopt.bc"
  "/home/mdl/hfs5022/llvm/projects/test-suite/build-release/MultiSource/Applications/obsequi/Obsequi.0.0.preopt.bc"
  )
add_benchmark_group("multisource-applications-some-find-pim-subgraphs"
                    "${multisource_applications}"
                    "-find-pim-subgraphs"
                    "${PASS_LIBS_DIR}/libPimSubgraphs.so"
                    "") # TODO no parser for now.

