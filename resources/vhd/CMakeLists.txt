project(PVMHDMLL NONE)
cmake_minimum_required(VERSION 3.3)
include(cmake/vhdl_macros.cmake)
execute_process(COMMAND ghdl -v OUTPUT_VARIABLE GHDL_VERSION_STRING)
if($GHDL_VERSION_STRING STREQUAL "")
    message(FATAL_ERROR "GHDL not found")
else()
    message(STATUS "Found ${GHDL_VERSION_STRING}")
endif()
execute_process(COMMAND gtkwave --version OUTPUT_VARIABLE GTKWAVE_VERSION_STRING)
if($GTKWAVE_VERSION_STRING STREQUAL "")
    message(FATAL_ERROR "GTKWAVE not found")
else()
    message(STATUS "Found ${GTKWAVE_VERSION_STRING}")
    set(VCD_VIEWER gtkwave)
endif()
enable_testing()
set(CTEST_OUTPUT_ON_FAILURE 1)
add_custom_target(runtest COMMAND ${CMAKE_CTEST_COMMAND} --verbose --build-run-dir=${CMAKE_CURRENT_BINARY_DIR})

add_vhdl_source(bnf.vhd bnf)
add_vhdl_source(pipe_reg.vhd pipe_reg)
add_vhdl_source(decision_box.vhd decision_box)
add_vhdl_source(combiner.vhd combiner)
add_vhdl_source(classifier.vhd classifier)
add_vhdl_source(tb/debug_func.vhd debug_func)

add_testbench_source(tb/tb_basic_comparator.vhd tb_basic_comparator)
add_testbench_source(tb/tb_parallel_comparator.vhd tb_parallel_comparator)
add_testbench_source(tb/tb_decision_box_int.vhd tb_decision_box_int)
add_testbench_source(tb/tb_decision_box_fp.vhd tb_decision_box_fp)
add_testbench_source(tb/tb_combiner.vhd tb_combiner)
add_testbench_source(tb/tb_classifier.vhd tb_classifier)

add_dependencies(decision_box pipe_reg)
add_dependencies(combiner pipe_reg)
add_dependencies(classifier decision_box bnf combiner)
add_dependencies(tb_basic_comparator decision_box debug_func)
add_dependencies(tb_parallel_comparator decision_box debug_func)
add_dependencies(tb_decision_box_fp decision_box debug_func)
add_dependencies(tb_decision_box_int decision_box debug_func)
add_dependencies(tb_combiner combiner)
add_dependencies(tb_classifier classifier)

add_custom_target(list ALL COMMAND ${CMAKE_VHDL_COMPILER} -d DEPENDS ${VHDL_MODULE} ${VHDL_TEST_MODULE})
