from .TreeModel import *
from jinja2 import Environment, FileSystemLoader
from distutils.dir_util import copy_tree, mkpath
from distutils.file_util import copy_file


class HDLGenerator:
    __source_dir = "./resources/"
    # VHDL sources
    __vhdl_cmake_dir = "vhd/cmake/"
    __vhdl_tb_dir = "vhd/tb/"
    __vhdl_cmakelist_template_file = "vhd/CMakeLists.txt"
    __vhdl_build_script_file = "vhd/build.sh"
    __vhdl_bnf_source = "vhd/bnf.vhd"
    __vhdl_reg_source = "vhd/pipe_reg.vhd"
    __vhdl_decision_box_source = "vhd/decision_box.vhd"
    __vhdl_combiner_source = "vhd/combiner.vhd"
    __vhdl_model_template_file = "vhd/classifier.vhd.template"
    __vhdl_tb_model_template_file = "vhd/tb_classifier.vhd.template"
    # C++ sources
    __cc_source_template_file = "cc/classifier.cc.template"
    __cc_header_template_file = "cc/classifier.h.template"
    __cc_tb_generator_template_file = "cc/tb_generator.cc.template"
    __cc_debug_template_file = "cc/debug.cc.template"
    __cc_cmakelist_file = "cc/CMakeLists.txt"
    __cc_build_script_file = "cc/generate_tb.sh"

    def __init__(self, features, classes, trees):
        self.__features = features
        self.__classes = classes
        self.__trees = trees

    def generate(self, destination):
        file_loader = FileSystemLoader(self.__source_dir)
        env = Environment(loader=file_loader)
        mkpath(destination)
        mkpath(destination + "/vhd")
        mkpath(destination + "/cc")

        copy_tree(self.__source_dir + self.__vhdl_cmake_dir, destination + "/" + self.__vhdl_cmake_dir)
        copy_tree(self.__source_dir + self.__vhdl_tb_dir, destination + "/" + self.__vhdl_tb_dir)
        copy_file(self.__source_dir + self.__vhdl_cmakelist_template_file, destination + "/vhd/")
        copy_file(self.__source_dir + self.__vhdl_build_script_file, destination + "/vhd/")
        copy_file(self.__source_dir + self.__vhdl_bnf_source, destination + "/vhd/")
        copy_file(self.__source_dir + self.__vhdl_reg_source, destination + "/vhd/")
        copy_file(self.__source_dir + self.__vhdl_decision_box_source, destination + "/vhd/")
        copy_file(self.__source_dir + self.__vhdl_combiner_source, destination + "/vhd/")
        copy_file(self.__source_dir + self.__cc_cmakelist_file, destination + "/cc/")
        copy_file(self.__source_dir + self.__cc_build_script_file, destination + "/cc/")
        trees = []
        for tree in self.__trees:
            dict_tree = { "name"       : tree.get_name(),
                          "boxes"      : tree.get_decision_boxes(self.__features),
                          "assertions" : tree.get_assertion_functions(self.__classes)}
            trees.append(dict_tree)

        ########################################################################
        # VHD sources generation
        template = env.get_template(self.__vhdl_model_template_file)
        output = template.render(trees = trees, features  = self.__features, classes = self.__classes)
        out_file = open(destination + "/vhd/classifier.vhd","w")
        out_file.write(output)
        out_file.close()
        template = env.get_template(self.__vhdl_tb_model_template_file)
        output = template.render(features  = self.__features, classes = self.__classes)
        out_file = open(destination + "/vhd/tb/tb_classifier.vhd","w")
        out_file.write(output)
        out_file.close()
                
        ########################################################################
        # C++ sources generation
        template = env.get_template(self.__cc_source_template_file)
        output = template.render(trees = trees, features  = self.__features, classes = self.__classes)
        out_file = open(destination + "/cc/classifier.cc","w")
        out_file.write(output)
        out_file.close()
        template = env.get_template(self.__cc_header_template_file)
        output = template.render(features  = self.__features, classes = self.__classes)
        out_file = open(destination + "/cc/classifier.h","w")
        out_file.write(output)
        out_file.close()
        template = env.get_template(self.__cc_tb_generator_template_file)
        output = template.render(features  = self.__features, classes = self.__classes)
        out_file = open(destination + "/cc/tb_generator.cc","w")
        out_file.write(output)
        out_file.close()
        template = env.get_template(self.__cc_debug_template_file)
        output = template.render(features  = self.__features, classes = self.__classes)
        out_file = open(destination + "/cc/debug.cc","w")
        out_file.write(output)
        out_file.close()
        
