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
    def __init__(self, pmml_file_name):
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
            for segment in segmentation.findall("pmml:Segment", self.__namespaces):
                tree_model_root = segment.find("pmml:TreeModel", self.__namespaces).find("pmml:Node", self.__namespaces)
                tree = self.__get_tree_model("tree_1", tree_model_root)
                self.__trees.append(tree)
        else:
            tree_model_root = root.find("pmml:TreeModel", self.__namespaces).find("pmml:Node", self.__namespaces)
            tree = self.__get_tree_model("tree_1", tree_model_root)
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
            if child.find("pmml:Interval", self.__namespaces) is None:
                continue
            features.append(child.attrib['name'])

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
                    classes.append(element.attrib['value'])
                    

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
        self.__get_tree_nodes_recursively( tree_name, tree_model_root, tree)
        return TreeModel(tree)

    """
    @brief Recoursively scan a parsed pmml tree model, building the internal data structure needed to generate HDL

    @param  tree_name
            The distinctive name of a tree model

    @param  element_tree_node
            The root node of the tree, from the parsed pmml object

    @param  parent_tree_node
            The root node of the tree, from the anytree object that will hold the data structure needed to generate HDL

    """
    def __get_tree_nodes_recursively(self, tree_name, element_tree_node, parent_tree_node):
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
                feature         = predicate.attrib['field']
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
                new_tree_node = Node('Node_' + child.attrib['id'], parent = parent_tree_node, score = child.attrib['score'], boolean_expression = boolean_expression)
            else:
                # if the considered node is a not leaf (it has pmml:Node children), we will go on with recursion
                new_tree_node = Node('Node_' + child.attrib['id'], parent = parent_tree_node, feature = "", operator = "", threshold_value = "", boolean_expression = boolean_expression)
                self.__get_tree_nodes_recursively(tree_name, child, new_tree_node)
