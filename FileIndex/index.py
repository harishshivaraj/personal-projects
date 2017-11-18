
from sys import stdout
from document import Color


class Node:

    def __init__(self, payload, sentence, filename):
        self.left = None
        self.right = None
        self.count = 1

        self.__payload = payload
        self.__document = set([filename])
        self.__sentences = set([sentence])

    @property
    def payload(self):
        return self.__payload

    @property
    def document(self):
        return self.__document

    @property
    def sentence(self):
        return self.__sentences

    def __str__(self):
        output = "\n"
        output += "{0}{1:<10}{2}" .format(Color.BLUE, str(self.payload), Color.ENDC)
        output += "{0}({1}){2}\n" .format \
                  (Color.RED, ', '.join(str(x) for x in self.document), Color.ENDC)

        for s in set(self.sentence):
            output += "{0:<10}{1}\n" .format(" ", str(s))
        return output

    def __repr__(self):
        return "node({0} {1} {2})" % (self.left, self.payload, self.right)


class AVLIndex:

    balance_it = 0

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def insert(self, payload, sentence, filename):
        if self.node is None:
            self.node = Node(payload, sentence, filename)
            self.node.left = AVLIndex()
            self.node.right = AVLIndex()

        elif payload < self.node.payload:
            self.node.left.insert(payload, sentence, filename)

        elif payload > self.node.payload:
            self.node.right.insert(payload, sentence, filename)

        elif payload == self.node.payload:
            self.node.count += 1
            self.node.sentence.add(sentence)
            self.node.document.add(filename)

        else:
            print "ERROR: no match " + payload

        self.balance_it += 1

        if self.balance_it % 10 == 0:
            self.rebalance()

    def rebalance(self):
        self.refresh_heights()
        self.refresh_balances()

        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.refresh_heights()
                    self.refresh_balances()

                self.rotate_right()
                self.refresh_heights()
                self.refresh_balances()

            if self.balance < -1:
                if self.balance < -1:
                    if self.node.right.balance > 0:
                        self.node.right.rotate_right()
                        self.refresh_heights()
                        self.refresh_balances()

                    self.rotate_left()
                    self.refresh_heights()
                    self.refresh_balances()

    def refresh_heights(self):
        if self.node:
            if self.node.left:
                self.node.left.refresh_heights()
            if self.node.right:
                self.node.right.refresh_heights()

            self.height = 1 + max(self.node.left.height, self.node.right.height)
        else:
            self.height = -1

    def refresh_balances(self):
        if self.node:
            if self.node.left:
                self.node.left.refresh_balances()
            if self.node.right:
                self.node.right.refresh_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def rotate_right(self):
        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def rotate_left(self):
        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def traverse(self):
        if self.node is None:
            return
        self.node.left.traverse()
        stdout.write(str(self.node))
        stdout.flush()
        self.node.right.traverse()







