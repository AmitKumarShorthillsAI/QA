'''unittest (built-in module) based testing'''
# import unittest
# from calculator import add

# class TestCalculator(unittest.TestCase):
#     def test_add(self):
#         self.assertEqual(add(2, 3), 5)
#         self.assertEqual(add(-1, 1), 0)

# if __name__ == "__main__":
#     unittest.main()

'''pytest (3rd party framework) based testing'''
from calculator import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

