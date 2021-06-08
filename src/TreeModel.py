from anytree import Node, RenderTree, PreOrderIter
import struct

class TreeModel:
    def __init__(self, root_node):
        self.__root_node = root_node

    def print(self):
        print(RenderTree(self.__root_node))

    def get_decision_boxes(self):
        boxes = []
        for node in PreOrderIter(self.__root_node):
            if any(node.children):
                #boxes.append(TreeModel.DecisionBox(node.name, node.feature, node.operator, node.threshold_value))
                boxes.append({  "name"      : node.name, 
                                "feature"   : node.feature, 
                                "operator"  : node.operator, 
                                "threshold" : str(self.double_to_hex(float(node.threshold_value)))[2:]})
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
        return assertion_function

    def get_assertion_functions(self, classes):
        functions = []
        for class_name in classes:
            functions.append({class_name : self.get_assertion(class_name)})
        return functions

    @staticmethod
    def float_to_hex(f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    @staticmethod
    def double_to_hex(f):
        return hex(struct.unpack('<Q', struct.pack('<d', f))[0])