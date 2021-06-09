# PVMHDMLL
This strange-named python tool allows you to automatically generate VHDL implementations for decision-tree and random forest classifiers directly from PMML files.

## Install requirements
```
pip3 install -r requirements.txt
```
## Running the tool
```
pvmhdmll [-h] -i input.pmml -o output_directory

```
  - -h: print the help screen.
  - -i:  specify the input PMML file to be converted in VHDL.
  - -o: specify the output directory in which VHDL source file will be generated.
  .
You MUST define ALL the mentioned parameters.

Starting from the provided PMML file, the PVMHDMLL tool will generate all the VHDL code needed to implement the classifier model (either random forest or single tree) within the target folder. 
In addition, it will generate 
 - a CMakeLists file and a bash script to compile and run unit tests with GHDL (obviously, you need GHDL in order to run unit testing);
 - a C++ implementation of the classifier.

The VHDL and C++ implementations will be places under the ``vhd`` and ``cc`` subdirectories of the target folder, respectively.

## Testbenches and oracles
The PVMHDMLL tool also generates a VHDL testbench for the generated classifier. In order to perform unit testing, you need to provide an oracle file to the testbenche.

In order to generate an oracle file, you can use the C++ implementation the tool generates. It's easy: run the ``generate_tb.sh`` script within the ``cc`` directory. That's all!