from itertools import chain

class Memory:
    def __init__(self, size):
        self.size = size
        self.container = tuple()

    def add(self, element):
        new = Memory(self.size)
        if self.__len__() < self.size:
            new_container = tuple(i for i in chain((element,), self.container))
        else:
            new_container = tuple(i for i in chain((element,), self.container[:-1]))
        new.container = new_container
        return new

    def __len__(self):
        return len(self.container)

    def __iter__(self):
        return self.container.__iter__()