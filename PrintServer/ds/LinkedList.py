
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
            return True

    head = None
    tail = None

    def __init__(self):
        pass

    def insert(self, payload):
        if self.head is None:
            self.head = self.Node(payload)
            self.tail = self.head
        else:
            self.tail = self.insert_node(self.head, payload)

    def insert_node(self, head_pointer, payload):
        if head_pointer.right is None:
            new_node = self.Node(payload)
            head_pointer.right = new_node
            new_node.left = head_pointer
            return new_node
        else:
            self.insert_node(head_pointer.right, payload)

    def delete(self, value):
        pass

    def __iter__(self):
        temp = self.head
        while temp is not None:
            yield temp
            temp = temp.right

    def __str__(self):
        pass

    def __repr__(self):
        pass


def main():
    dl = DoubleLinkedList()
    dl.insert(10)
    dl.insert(20)

    for n in dl:
        print(n)


if __name__ == "__main__":
    main()

