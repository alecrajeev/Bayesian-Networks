import numpy as np
from HashNode import HashNode


class HashTable(object):
    """
    This is the Hash Table object that is used to quickly find objects.
    """

    def __init__(self, table_size):
        self.size = table_size
        self.table = [None] * table_size
        self.list_of_ints = []
        self.key_count = 0


    def put(self, key, value):
        index_of_hash_table = self.hash_function(key)

        node = HashNode(key, value)
        self.key_count += 1

        temp = self.table[index_of_hash_table]
        if temp is None:
            self.table[index_of_hash_table] = node
        else:
            temp.add_node(node)

    def get(self, key):
        index_of_hash_table = self.hash_function(key)

        if self.table[index_of_hash_table] is None:
            return -1

        # handles collisions with separate chaining
        node = self.table[index_of_hash_table]
        if node.key == key:
            return node.value

        while node.key != key:
            node = node.next
            if node is None:
                return -1

        if node.key == key:
            return node.value

        print "hash table problem"
        return -1

    def hash_function(self, key):

        key_index = 0

        for i in xrange(0, len(key)):
            key_index += ord(key[i])

        key_index *= ord(key[0])
        key_index *= ord(key[len(key) - 1])
        key_index /= ord(key[len(key) / 2])

        key_index = key_index % self.size

        if key_index < 0:
            key_index += self.size

        return key_index


    def dump(self):
        """
        Prints out all the symbols
        """
        for i in xrange(0, self.size):
            if not(self.table[i] is None):
                node = self.table[i]
                while not(node is None):
                    print node.key
                    print node.value
                    node = node.next

