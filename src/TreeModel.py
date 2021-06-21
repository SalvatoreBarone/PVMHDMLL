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
from anytree import RenderTree, PreOrderIter
from pyeda.inter import *
import struct

class TreeModel:
    def __init__(self, name, root_node):
        self.__name = name;
        self.__root_node = root_node

    def get_name(self):
        return self.__name

    def print(self):
        print(RenderTree(self.__root_node))

    def get_decision_boxes(self, features):
        boxes = []
        for node in PreOrderIter(self.__root_node):
            if any(node.children):
                #search for the data-type of the feature
                for feature in features:
                    if feature["name"] == node.feature:
                        c_operator = ""
                        if node.operator == "greaterThan":
                          c_operator = ">"
                        elif node.operator == "lessThan":
                          c_operator = "<"
                        else: 
                          c_operator = "=="
                        if feature["type"] == "double":
                            boxes.append({  "name"      : node.name, 
                                "feature"       : node.feature,
                                "data_type"     : feature["type"],
                                "operator"      : node.operator,
                                "c_operator"    : c_operator,
                                "threshold"     : str(node.threshold_value),
                                "threshold_hex" : str(self.double_to_hex(float(node.threshold_value)))[2:]})
                        else:
                            boxes.append({  "name"          : node.name, 
                                            "feature"       : node.feature,
                                            "data_type"     : feature["type"],
                                            "operator"      : node.operator,
                                            "c_operator"    : c_operator,
                                            "threshold"     : str(node.threshold_value),
                                            "threshold_hex" : str(hex(int(node.threshold_value)))[2:]})
        return boxes

    def get_leaves(self):
        leaves = []
        for node in PreOrderIter(self.__root_node):
            if not any(node.children):
                leaves.append({ "name"       : node.name,
                                "score"      : node.score,
                                "expression" : node.boolean_expression})
        return leaves

    def get_assertion(self, class_name):
        assertion_function = ""
        leaves = self.get_leaves()
        for leaf in leaves:
            if leaf["score"] == class_name:
                if assertion_function:
                    assertion_function += " | "
                assertion_function += "(" + leaf["expression"] + ")"
        if not assertion_function:
            assertion_function = "'0'"
        else:
            assertion_function = str(espresso_exprs(expr(assertion_function))[0] ).replace("~", "not ").replace("Or","func_or").replace("And","func_and")
        return assertion_function

    def get_assertion_functions(self, classes):
        functions = []
        for class_name in classes:
            functions.append({  "class"      : class_name,
                                "expression" : self.get_assertion(class_name)})
        return functions

    @staticmethod
    def float_to_hex(f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    @staticmethod
    def double_to_hex(f):
        return hex(struct.unpack('<Q', struct.pack('<d', f))[0])