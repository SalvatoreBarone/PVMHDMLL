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
                data_type = ""
                for feature in features:
                    if feature["name"] == node.feature:
                        if feature["type"] == "double" or feature["type"] == "float":
                            data_type = "float"
                            boxes.append({  "name"      : node.name, 
                                "feature"   : node.feature,
                                "data_type" : data_type,
                                "operator"  : node.operator, 
                                "threshold" : str(self.float_to_hex(float(node.threshold_value)))[2:]})
                        elif feature["type"] == "integer":
                            data_type = "int"
                            boxes.append({  "name"      : node.name, 
                                            "feature"   : node.feature,
                                            "data_type" : data_type,
                                            "operator"  : node.operator, 
                                            "threshold" : str(hex(int(node.threshold_value)))[2:]})
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