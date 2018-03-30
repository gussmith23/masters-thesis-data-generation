all:
	find /home/mdl/hfs5022/llvm/projects/test-suite/build -regex '.*preopt.*\.bc'
	find /home/mdl/hfs5022/llvm/projects/test-suite/build -regex '.*preopt.*\.bc' -print0 | xargs -0 -I{} sh -c '/home/mdl/hfs5022/llvm/build/bin/opt -load /home/mdl/hfs5022/2018-spring-llvm-passes/build/pass-libs/libLdLdOpSt.so -find-ld-ld-op-st -analyze "$$1" > "$$(basename $$1).out.txt"' -- {}

clean:
	rm *.out.txt
