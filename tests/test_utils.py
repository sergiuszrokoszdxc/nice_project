import unittest

import unittest.mock

from nice_project.utils.memory import Memory
from nice_project.utils.stoper import Stoper


class TestMemory(unittest.TestCase):
    def test_len(self):
        """len() should return number of elements stored"""
        mem = Memory(3)
        self.assertEqual(len(mem), 0)
        mem = mem.add(0)
        self.assertEqual(len(mem), 1)
        mem = mem.add(0)
        self.assertEqual(len(mem), 2)
        mem = mem.add(0)
        self.assertEqual(len(mem), 3)

    def test_max_size(self):
        """Should store only limited number of elements"""
        mem = Memory(3)
        mem = mem.add(0)
        mem = mem.add(0)
        mem = mem.add(0)
        self.assertEqual(len(mem), 3)
        mem = mem.add(0)
        self.assertEqual(len(mem), 3)

    def test_iter(self):
        """Iter should return iterable of elements in reversed order"""
        mem = Memory(3)
        mem = mem.add(0)
        mem = mem.add(1)
        mem = mem.add(2)
        for x, y in zip(mem, (2, 1, 0)):
            self.assertEqual(x, y)


class TestStoper(unittest.TestCase):
    def test_stop_envoke_add(self):
        """stop() method should envoke add() method od field memory and pass
        value returned by function field"""
        memory = unittest.mock.Mock()

        def fun():
            return unittest.mock.DEFAULT
        function = fun
        stoper = Stoper(memory=memory, function=function)
        stoper.stop()
        memory.add.assert_called_with(unittest.mock.DEFAULT)

    def test_stop_pass_to_function(self):
        """stop() method should pass positional and keyword arguments to
         invoked function field"""
        memory = unittest.mock.Mock()
        function = unittest.mock.Mock()
        stoper = Stoper(memory=memory, function=function)
        stoper.stop("1", foo="bar")
        function.assert_called_with("1", foo="bar")

    def test_get_stored(self):
        """get_stored_should return list(memory)"""
        memory = unittest.mock.MagicMock()
        memory.__iter__.return_value = [unittest.mock.DEFAULT]
        function = None
        stoper = Stoper(memory=memory, function=function)
        stored = stoper.get_stored()
        self.assertEqual(stored, [unittest.mock.DEFAULT])
