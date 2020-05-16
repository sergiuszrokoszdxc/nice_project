import unittest

from nice_project.utils.memory import Memory

class TestMemory(unittest.TestCase):
    def test_length(self):
        """Test if have max size specified in constructor"""
        mem1 = Memory(3)
        self.assertEqual(len(mem1), 0, "new memory should be empty")
        mem1 = mem1.add(0)
        self.assertEqual(len(mem1), 1, "should have 1 element")
        mem1 = mem1.add(0)
        self.assertEqual(len(mem1), 2, "should have 2 elements")
        mem1 = mem1.add(0)
        self.assertEqual(len(mem1), 3, "should have 3 elements")
        mem1 = mem1.add(0)
        self.assertEqual(len(mem1), 3, "should stay 3 elements long")
        mem2 = Memory(2)
        mem2 = mem2.add(0)
        mem2 = mem2.add(0)
        mem2 = mem2.add(0)
        self.assertEqual(len(mem2), 2, "should have no more than 2 elements")

    def test_recover(self):
        """Test if store elements in order"""
        mem = Memory(3)
        mem = mem.add(0)
        mem = mem.add(1)
        mem = mem.add(2)
        for x, y in zip(mem, (2, 1, 0)):
            self.assertEqual(x, y, f"should be stored in reverse order")

if __name__ == "__main__":
    unittest.main()