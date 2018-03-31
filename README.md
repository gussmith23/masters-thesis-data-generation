This repository generates the results for my MS thesis. It is set up as follows.

Every set of results gets its own directory in the root directory. Inside each of these directories is a CMakeLists.txt which calls the custom function `add_benchmark_group`. This function registers the results set with CMake. It takes the set of benchmarks to run on, the LLVM pass(es) to run, and an optional Python script to "summarize" the results and output a summary text file. I currently use the summarize feature to parse the results and generate LaTeX tables.

Note that, if you do `mkdir build && cmake .. <cmake flags> && make <my result set target>` (which is how CMake builds seem to be done by default), all the results will end up in the build directory. The source remains essentially empty other than CMakeLists.txt files which set up each result set. I recognize that this is strange, but it's a consequence of using CMake for something that isn't exactly code compilation.

## Dependencies
- My [LLVM passes](https://github.com/gussmith23/llvm-pim-passes). Build this repo, and then pass the path to the build/pass-libs dir as `-DPASS_LIBS_DIR`.
- Build LLVM's test-suite project into "monolithic" IR files. [This commit](https://github.com/gussmith23/test-suite/commit/b39d483ae23f685f50af8535761d1ce0bea7cf4a) in my fork of test-suite should help you do this. The project must be built, and then the path to the build folder should be passed as `-DBENCHMARKS_DIR`.
- The Python files were made for Python 2.7 on Linux. Hopefully they should work for Python 3, but they might not be cross-platform.

## Generating Result Sets
```shell
cmake -DBENCHMARKS_DIR=<path/to/test-suite/build> -DPASS_LIBS_DIR=<path/to/llvm-pim-passes/build/pass-libs> ..
make <result set name>
```
