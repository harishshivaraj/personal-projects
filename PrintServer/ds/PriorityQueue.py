
from abc import ABC, abstractmethod


class PriorityQueueAbstract(ABC):

    @abstractmethod
    def insert(self, value): pass

    @abstractmethod
    def get_highest(self): pass

    @abstractmethod
    def pop_highest(self): pass

    @abstractmethod
    def is_empty(self): pass

    @abstractmethod
    def length(self): pass


class PriorityQueue(PriorityQueueAbstract):

    def __init__(self):
        super().__init__()

    def insert(self):
        pass

    def get_highest(self):
        pass

    def pop_highest(self):
        pass

    def is_empty(self):
        pass

    def length(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()



