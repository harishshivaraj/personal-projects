
from codecs import open
from string import punctuation
from os import path


class Color:
    RED = '\033[1;31m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'


class Content:

    __content = None
    __sentences = []

    def __init__(self, content):
        self.__content = content
        self.__normalise()
        for s in self.__content.split('.'):
            if len(s) > 1:
                self.__sentences.append(Sentence(s))

    def __normalise(self):
        deli_chars = list(punctuation) + [u'\u201d', u'\u2019', u'\u2018', u'\u201e', u'\u201c', '\n', '\r\n']
        deli_chars.remove('.')

        for ch in deli_chars:
            self.__content = self.__content.replace(ch, '')

        self.lower()

        return self

    def lower(self):
        self.__content = self.__content.lower()
        return self

    def strip(self):
        self.__content = self.__content.strip()
        return self

    @property
    def sentences(self):
        return self.__sentences


class Sentence:

    __sentence = None
    __words = None

    def __init__(self, sentence):
        self.__sentence = sentence
        self.__normalise()
        self.__words = self.__sentence.split(' ')

    def __normalise(self):
        self.__sentence = self.__sentence.strip()
        return self

    def highlight(self, word):
        if word in self.__sentence:
            return self.__sentence.replace(word, "%s%s%s" % (Color.YELLOW, word, Color.ENDC))

    def __str__(self):
        return self.__sentence

    @property
    def words(self):
        for w in self.__words:
            w = w.strip()
            if w == ' ':
                continue
            if len(w) < 3:
                continue
            yield w


class Document:

    __index = None
    __file = None
    __fh = None
    __content = None

    def __init__(self, filepath):
        self.__file = filepath
        self.__filename = path.basename(self.__file)
        self.__fh = open(self.__file, encoding='utf-8')
        self.__content = Content(self.__fh.read())

    def index(self, index):
        self.__index = index
        for s in self.__content.sentences:
            for w in s.words:
                self.__index.insert(w, s.highlight(w), self.__filename)
        return self.__index

    def close(self):
        if not self.__fh.closed:
            self.__fh.close()

    @property
    def indexed(self):
        return self.__index is not None
