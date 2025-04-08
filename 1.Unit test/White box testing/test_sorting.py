import unittest
from sorting import sort_numbers

class TestSorting(unittest.TestCase):
    def test_sort_numbers(self):
        self.assertEqual(sort_numbers([3, 1, 2]), [1, 2, 3])
        self.assertEqual(sort_numbers([]), None)

if __name__ == "__main__":
    unittest.main()
