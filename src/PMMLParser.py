"""
Copyright 2020-2021 Salvatore Barone <salvatore.barone@unina.it>

This file is part of PVMHDMLL

This is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or any later version.

This is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
import sys
from xml.etree import ElementTree
from anytree import Node
from .TreeModel import *

class PMMLParser:
    __namespaces = {'pmml': 'http://www.dmg.org/PMML-4_1'}

    """
    @brief Constructor function

    @param  pmml_file_name
            Path of the PMML file to be parsed
    """
    def __init__(self, pmml_file_name, print_trees):
        self.__trees    = []
        self.__features = []
        self.__classes  = []

        tree = ElementTree.parse(pmml_file_name)
        root = tree.getroot()

        self.__get_classes(root, self.__classes)
        self.__get_features(root, self.__features)
        
        segmentation = root.find("pmml:MiningModel/pmml:Segmentation", self.__namespaces)
        if segmentation is not None:
            # The prediction model is based upon single decision tree
            tree_id = 0
            for segment in segmentation.findall("pmml:Segment", self.__namespaces):
                tree_model_root = segment.find("pmml:TreeModel", self.__namespaces).find("pmml:Node", self.__namespaces)
                tree = self.__get_tree_model(str(tree_id), tree_model_root)
                self.__trees.append(tree)
                if print_trees:
                  tree.print()
                tree_id += 1
        else:
            tree_model_root = root.find("pmml:TreeModel", self.__namespaces).find("pmml:Node", self.__namespaces)
            tree = self.__get_tree_model("0", tree_model_root)
            if print_trees:
              tree.print()
            self.__trees.append(tree)

    def get_classes(self):
        return self.__classes

    def get_features(self):
        return self.__features

    def get_trees(self):
        return self.__trees

    """
    @brief Scan the DataDictionary section of the PMML file for features

    @param  root
            The root node of the parsed PMML file
    @param  features
            List of features
    """
    def __get_features(self, root, features):
        for child in root.find("pmml:DataDictionary", self.__namespaces).findall('pmml:DataField', self.__namespaces):
            interval = child.find("pmml:Interval", self.__namespaces)
            if interval is None:
                continue
            data_type = "double" if child.attrib['dataType'] == "double" else "int"
            features.append({
              "name" : child.attrib['name'].replace('-','_'), 
              "type" : data_type,
              "min"  : interval.attrib['leftMargin'],
              "max"  : interval.attrib['rightMargin']})

    """
    @brief Scan the DataDictionary section of the PMML file for classes

    @param  root
            The root node of the parsed PMML file
    @param  classes
            List of classes
    """
    def __get_classes(self, root, classes):
        for child in root.find("pmml:DataDictionary", self.__namespaces).findall('pmml:DataField', self.__namespaces):
            if child.find("pmml:Interval", self.__namespaces) is None:
                for element in child.findall("pmml:Value", self.__namespaces):
                    classes.append(element.attrib['value'].replace('-','_'))
                    

    """
    @brief Get a tree model from the parsed PMML file

    @param  tree_name
            The distinctive name of a tree model

    @param  tree_model_root
            The root node of the tree, from the parsed PMML object

    @return The root node of the tree, from the anytree object that will hold the data structure needed to generate HDL

    """
    def __get_tree_model(self, tree_name, tree_model_root):
        tree = Node('Node_' + tree_model_root.attrib['id'], feature = "", operator = "", threshold_value = "", boolean_expression = "")
        self.__get_tree_nodes_recursively(tree_model_root, tree)
        return TreeModel(tree_name, tree)

    """
    @brief Recoursively scan a parsed pmml tree model, building the internal data structure needed to generate HDL

    @param  element_tree_node
            The root node of the tree, from the parsed pmml object

    @param  parent_tree_node
            The root node of the tree, from the anytree object that will hold the data structure needed to generate HDL

    """
    def __get_tree_nodes_recursively(self, element_tree_node, parent_tree_node):
        children = element_tree_node.findall("pmml:Node", self.__namespaces);
        if len(children) > 2:
            print("Only binary trees are supported. Aborting")
            sys.exit(2)

        for child in children: 
            boolean_expression = parent_tree_node.boolean_expression
            if boolean_expression:
                boolean_expression += " & "
            predicate = child.find("pmml:SimplePredicate", self.__namespaces)

            if predicate is None:
                print("Predicate is None")
            else:
                feature         = predicate.attrib['field'].replace('-','_')
                operator        = predicate.attrib['operator']
                threshold_value = predicate.attrib['value']
                """
                The features to be compared against the treshold, the comparison operator and the threshold value itself
                are stored in the parent node (which became a full decision box) whether the comparator is in the
                following Q column.
                Consequently, also a boolean expression to reach the node will be computed progressively.
                Boolean expressions of leaf node will be used to define assertion functions in HDL.

                ---------------------------------------------
                Q                    ~Q
                equal 	            notEqual 	
                lessThan 	        greaterOrEqual 	
                greaterThan         lessOrEqual 	     	
                """
                if operator in ('equal','lessThan','greaterThan'):
                    parent_tree_node.feature         = feature
                    parent_tree_node.operator        = operator
                    parent_tree_node.threshold_value = threshold_value
                    boolean_expression += parent_tree_node.name
                else:
                    boolean_expression += "~" + parent_tree_node.name

            if child.find("pmml:Node", self.__namespaces) is None:
                # if the considered node is a leaf (it has no pmml:Node children), we are interested in the class that the node belongs to
                new_tree_node = Node('Node_' + child.attrib['id'], parent = parent_tree_node, score = child.attrib['score'].replace('-','_'), boolean_expression = boolean_expression)
            else:
                # if the considered node is a not leaf (it has pmml:Node children), we will go on with recursion
                new_tree_node = Node('Node_' + child.attrib['id'], parent = parent_tree_node, feature = "", operator = "", threshold_value = "", boolean_expression = boolean_expression)
                self.__get_tree_nodes_recursively(child, new_tree_node)

