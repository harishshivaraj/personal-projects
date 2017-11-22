
class DoubleLinkedList:

    class Node:

        left = None
        payload = None
        right = None

        def __init__(self, payload):
            self.payload = payload

        def __str__(self):
            return str(self.payload)

        def __repr__(self):
            return "node(%s)" % self

        def __eq__(self, other):
            return self.payload == other.payload

    head = None
    tail = None
    size = 0

    def __init__(self):
        pass

    def insert(self, payload):
        if self.head is None:
            self.head = self.Node(payload)
            self.tail = self.head
        else:
            self.tail = self.insert_node(self.head, payload)
        self.size += 1

    def insert_node(self, head_pointer, payload):
        if head_pointer.right is None:
            new_node = self.Node(payload)
            head_pointer.right = new_node
            new_node.left = head_pointer
            return new_node
        else:
            return self.insert_node(head_pointer.right, payload)

    def delete(self, value):
        node_to_del = self.find(value)
        if node_to_del:
            if not node_to_del.right:
                self.tail = node_to_del.left
                node_to_del.left.right = None
            elif not node_to_del.left:
                self.head = node_to_del.right
                node_to_del.right.left = None
            else:
                node_to_del.left.right = node_to_del.right
                node_to_del.right.left = node_to_del.left
            del node_to_del
            self.size -= 1
            return True
        return False

    def find(self, value):
        for n in self:
            if n == self.Node(value):
                return n
        return None

    def __reversed__(self):
        temp = self.tail
        while temp:
            yield temp
            temp = temp.left

    def __iter__(self):
        temp = self.head
        while temp is not None:
            yield temp
            temp = temp.right

    def __str__(self):
        return str([n.payload for n in self])

    def __repr__(self):
        pass

    def __getitem__(self, item):
        if not isinstance(item, slice):
            if item == 0:
                return self.head
            elif item == self.size-1:
                return self.tail
            elif 0 < item < self.size:
                temp = self.head
                for i in range(0, item, 1):
                    temp = temp.right
                return temp
            else:
                raise IndexError("list index out of range")
        else:
            pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass


def main():
    dl = DoubleLinkedList()
    dl.insert(10)
    dl.insert(20)
    dl.insert(30)
    dl.insert(40)
    dl.insert(50)

    print(dl[1])
    # print(dl.size)
    # print(dl)
    # print(dl.find(40))
    # print(dl.delete(20))
    # print(dl.size)


if __name__ == "__main__":
    main()

