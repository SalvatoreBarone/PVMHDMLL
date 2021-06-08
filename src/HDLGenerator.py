from .TreeModel import *
from jinja2 import Environment, FileSystemLoader
from distutils.dir_util import copy_tree, mkpath
from distutils.file_util import copy_file


class HDLGenerator:
    __source_dir = "./resources/vhd/"
    __cmake_dir = "cmake/"
    __tb_dir = "tb/"
    __cmakelist_template_file = "CMakeLists.txt.template"
    __build_script_file = "build.sh"
    __bnf_source = "bnf.vhd"
    __decision_box_source = "decision_box.vhd"
    __decision_tree_template_file = "decision_tree.vhd.template"
    __tb_decision_tree_template_file = "tb_decision_tree.vhd.template"
    

    def __init__(self, features, classes, trees):
        self.__features = features
        self.__classes = classes
        self.__trees = trees

    def generate(self, destination):
        entities = []
        mkpath(destination)
        copy_tree(self.__source_dir + self.__cmake_dir, destination + "/" + self.__cmake_dir)
        copy_tree(self.__source_dir + self.__tb_dir, destination + "/" + self.__tb_dir)
        copy_file(self.__source_dir + self.__build_script_file, destination)
        copy_file(self.__source_dir + self.__bnf_source, destination)
        copy_file(self.__source_dir + self.__decision_box_source, destination)

        file_loader = FileSystemLoader(self.__source_dir)
        env = Environment(loader=file_loader)

        # Generating tree entities
        template = env.get_template(self.__decision_tree_template_file)
        for tree in self.__trees:
            entities.append("decision_tree_" + tree.get_name())
            output = template.render(
                tree_name = tree.get_name(),
                features  = self.__features,
                classes = self.__classes,
                decision_boxes = tree.get_decision_boxes(self.__features),
                assertion_functions = tree.get_assertion_functions(self.__classes))
            out_file = open(destination + "/" + "decision_tree_" + tree.get_name() + ".vhd","w")
            out_file.write(output)
            out_file.close()
        
        # Generating the CMakeList file for compilation purpose
        template = env.get_template(self.__cmakelist_template_file)
        output = template.render(entities = entities)
        out_file = open(destination + "/" + "CMakeLists.txt","w")
        out_file.write(output)
        out_file.close()

