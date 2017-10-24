# Installation

1. cd PyC4/
2. python setup.py

# Running programs

1. Designate the path to the driver. 
2. First argument after the call to the driver script is the path to input overlog program.
3. Second argument after the call to the driver script is the path to the table list for the specified overlog program.


For example, run the following command from examples/test/ :

```
python ../../src/drivers/pyc4.py ./myTest.olg ./tableListStr_myTest.data 
```

# Tips
1. For C4 debugging, you'll have to manually flip the defines in the C4 submodule code.
2. The run scripts in examples/simplog_sanity_tests/ demonstrates the process of passing programs to PyC4.
3. PyC4 requires the last (rightmost) input file is the tables list.
4. You can list as many overlog programs as you want between the driver script and the table list.
5. Searching the evaluation results on stdout for "Submitting subprog" reveals the exact order and input contents of all install_str calls associated with a particular C4 run.

# building with cmake

```
git submodule update --init --recursive

# install c4 dependencies
dnf install cmake gcc apr-devel apr-util-devel flex bison sqlite-devel

cmake .
make

python src/drivers/pyc4.py examples/test/myTest.olg examples/test/tableListStr_myTest.data
```
