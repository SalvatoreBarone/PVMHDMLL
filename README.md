# PVMHDMLL
This strange-named python tool allows you to automatically generate VHDL implementations for decision-tree and random forest classifiers directly from PMML files.

## Install requirements
```
pip3 install -r requirements.txt
```
## Run the tool
```
pvmhdmll [-h] -i input.pmml -o output_directory

```
   -h: print the help screen.
   -i:  specify the input PMML file to be converted in VHDL.
   -o: specify the output directory in which VHDL source file will be generated.
You MUST define ALL the mentioned parameters.

Starting from the provided PMML file, the PVMHDMLL tool will generate all the VHDL code needed to implement the classifier model (either random forest or single tree) within the target folder. 
In addition, it will generate a CMakeLists file and a bash script to compile and run unit tests with GHDL (obviously, you need GHDL in order to run unit testing). 
The tool can also generate a testbench for the generated classifier, to which you need to provide an oracle. Please, see the following section for details on how to define the oracle.

## Test oracle


