project(model_oracle)
cmake_minimum_required(VERSION 3.3)
set (CMAKE_CXX_STANDARD 11)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY                     ${CMAKE_BINARY_DIR}/libs)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY                     ${CMAKE_BINARY_DIR}/libs)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY                      ${CMAKE_BINARY_DIR}/bin)
set(ORACLES_DESTINATION_DIRECTORY                  ${CMAKE_CURRENT_LIST_DIR}/..)

add_executable(tb_generator tb_generator.cc classifier.cc)
add_executable(debug debug.cc classifier.cc)
target_compile_definitions(debug PUBLIC DEBUG)

add_custom_target(
  oracle_files ALL
  WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}
  COMMAND echo "Please, wait. This may take a while..."
  COMMAND ./tb_generator > ${ORACLES_DESTINATION_DIRECTORY}/vhd/tb_classifier.txt 
  DEPENDS tb_generator
  VERBATIM)