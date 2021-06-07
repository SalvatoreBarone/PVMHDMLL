#import pandas as pd
#import numpy as np
from xml.etree import ElementTree
from anytree import Node, RenderTree

from .ModelFeature import *
from .TreeNode import *

class PMMLParser:
    __namespaces = {'pmml': 'http://www.dmg.org/PMML-4_1'}

    def __init__(self, pmml_file_name):
        
    
        print(pmml_file_name)
        tree = ElementTree.parse(pmml_file_name)
        root = tree.getroot()
        self.__get_data_fields(root)

        self.__tree = Node("root")
        root_elem = self.__tree
        self.__get_tree_nodes(root.find("pmml:TreeModel", self.__namespaces), root_elem)
        for pre, fill, node in RenderTree(self.__tree):
            print("%s%s" % (pre, node.name))


    def __get_data_fields(self, root):
        for child in root.find("pmml:DataDictionary", self.__namespaces).findall('pmml:DataField', self.__namespaces):
            print(child.tag, child.attrib)
            #for field in child:
            #    print("\t", field.tag, field.attrib)

    def __get_tree_nodes(self, element_tree_node, parent_tree_node, recursion_level = 1):
        print(' ' * recursion_level, element_tree_node.tag, element_tree_node.attrib)
        for child in element_tree_node.findall("pmml:Node", self.__namespaces):
            new_tree_node = Node(child.attrib['id'], parent=parent_tree_node)
            self.__get_tree_nodes(child, new_tree_node, recursion_level + 1)

