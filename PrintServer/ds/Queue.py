from LinkedList import DoubleLinkedList

class Queue:

    size = None
    queue = None

    def __init__(self, size):
        self.size = size
        self.queue = DoubleLinkedList()

    def enqueue(self, value):
        self.queue

    def dequeue(self):
        pass

    def peek(self):
        pass

    def isfull(self):
        pass

    def isemty(self):
        pass

    def __str__(self):
        return ""

    def __iter__(self):
        pass


def main():
    q = Queue(10)
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    q.enqueue(40)
    q.enqueue(50)

    print(q)


if __name__ == "__main__":
    main()
