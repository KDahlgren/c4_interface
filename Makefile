all: deps

deps: get-submodules c4

clean:
	rm -rf lib/c4/build

c4: lib/c4/build/src/libc4/libc4.dylib

lib/c4/build/src/libc4/libc4.dylib:
	@which cmake > /dev/null
	cd lib/c4 && mkdir -p build
	cd lib/c4/build && cmake ..
	cd lib/c4/build && make

get-submodules:
	git submodule init
	git submodule update

