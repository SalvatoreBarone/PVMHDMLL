from anytree import Node, RenderTree

class TreeModel:
    def __init__(self, root_node):
        self.__root_node = root_node

    def print(self):
        print(RenderTree(self.__root_node))   

    @staticmethod
    def float_to_hex(f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    @staticmethod
    def double_to_hex(f):
        return hex(struct.unpack('<Q', struct.pack('<d', f))[0])