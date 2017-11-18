#! /usr/bin/python

from glob import glob
from document import Document
from index import AVLIndex

PATH = "./TestDocs/*.txt"


def main():

    index = AVLIndex()

    for file_path in glob(PATH):
        d = Document(file_path)
        index = d.index(index)
        d.close()

    index.traverse()


if __name__ == "__main__":
    main()
