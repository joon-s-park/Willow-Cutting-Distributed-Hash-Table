"""
AUTHORS: Joon Sung Park, Jacob Carstenson
DATE: 2016-4-08

"""

class DataStructure(object):

    def __init__(self):
        self.root = None
        self.size = 0

    # __str__ supports print operation for printing out.
    def __str__(self):
        raise NotImplementedError

    def length(self):
        return self.size

    # __len__ supports len(BST) operation for getting the length of BST
    def __len__(self):
        return self.size

    # overwrites the value if the key already exists
    def put(self, key, value):
        raise NotImplementedError

    # __setitem__ supports [] operator for assignments
    # ex: BST['x'] = 1984
    # overwrites the value if the key already exists
    def __setitem__(self, key, value):
        self.put(key, value)

    # returns None if item not found
    def get(self, key):
        raise NotImplementedError

    def _objectGet(self, key):
        raise NotImplementedError

    # __getitem__ supports [] operator for lookup
    # ex: BST['y'] = 2016
    # returns None if item not found
    def __getitem__(self, key):
        return self.get(key)

    # __contains__ supports in operation for seeing if the key already exists
    # ex: x in BST
    def __contains__(self, key):
        if self.get(key):
            return True
        else: 
            return False
    
    # error if the key is not found. Otherwise does not return anything.
    def delete(self, key):
    	raise NotImplementedError

    # error if the key is not found
    def __delitem__(self, key):
    	self.delete(key)

    def getRootNode(self):
        return self.root

    def getAllNode(self):
        raise NotImplementedError
