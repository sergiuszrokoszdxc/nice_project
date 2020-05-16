class Stoper:
    def __init__(self, memory, function):
        """Store values returned by chosen function in fixed length memory.

        Parameters
        ----------
        memory : Memory
            fixed length memory / must be iterable and implement add method with one parameter
        function : function
            any function accepting positional and keyword arguments and returning values
        """
        self.memory = memory
        self.function = function
    def stop(self, *args, **kwargs):
        """Store value returned by function.
        Can supply positional and keyword arguments to the wrapped function
        """
        value = self.function(*args, **kwargs)
        self.memory = self.memory.add(value)
    def get_stored(self):
        """Return values stored in memory.

        Returns
        -------
        list
            list of values stored in memory
        """
        return list(self.memory)