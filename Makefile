all: deps

deps: get-submodules

clean:
	rm -r lib_orig/c4/build
	rm -r lib_customMain/c4/build

c4_orig: lib_orig/c4/build/src/libc4/libc4.dylib

c4_customMain: lib_customMain/c4/build/src/libc4/libc4.dylib

lib_orig/c4/build/src/libc4/libc4.dylib:
	@which cmake > /dev/null
	cd lib_orig/c4 && mkdir -p build
	cd lib_orig/c4/build && cmake ..
	( cd lib_orig/c4/build && make ) 2>&1 | tee c4_out.txt;

lib_customMain/c4/build/src/libc4/libc4.dylib:
	@which cmake > /dev/null
	cd lib_customMain/c4 && mkdir -p build
	cd lib_customMain/c4/build && cmake ..
	( cd lib_customMain/c4/build && make ) 2>&1 | tee c4_out.txt;

get-submodules:
	git submodule init
	git submodule update

