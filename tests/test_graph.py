import unittest
from src.graph import get_load_order

class TestGraph(unittest.TestCase):
    def test_load_order(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        order = get_load_order(graph)
        self.assertEqual(order, ["D", "B", "C", "A"])

if __name__ == "__main__":
    unittest.main()