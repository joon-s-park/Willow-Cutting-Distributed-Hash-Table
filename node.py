"""
AUTHORS: Joon Sung Park, Jacob Carstenson
DATE: 2016-4-08

"""

class Node(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.key) + ", " + str(self.value)

    def getKey(self):
        return self.key
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
    
######################################################

if __name__ == "__main__":

    n1 = Node(1, "jeff")
    n2 = Node(2, "lauri")
    n3 = Node(3, "alex")
    n4 = Node(4, "rachel")

    print n1
    print n2
    print n3
    print n4