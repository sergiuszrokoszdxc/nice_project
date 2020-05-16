from itertools import chain

class Memory:
    def __init__(self, size):
        """Strore history of specific length.

        New elements are appended in front of sequence.
        When sequence is full, adding new element will
        cause oldest one to be forgotten.

        Parameters
        ----------
        size : int
            how many elements can be stored
        """
        self.size = size
        self.container = tuple()

    def add(self, element):
        """Get new Memory object with updated history.

        Parameters
        ----------
        element : any
            element to be added

        Returns
        -------
        Memory
            memory with updated state.
        """
        new = Memory(self.size)
        if self.__len__() < self.size:
            new_container = tuple(i for i in chain((element,), self.container))
        else:
            new_container = tuple(i for i in chain((element,), self.container[:-1]))
        new.container = new_container
        return new

    def __len__(self):
        """Get current number of elements stored.

        Returns
        -------
        int
            number of elements
        """
        return len(self.container)

    def __iter__(self):
        """Get stored elements as iterator.

        Returns
        -------
        tuple_iterator
            iterator of stored elements
        """
        return self.container.__iter__()