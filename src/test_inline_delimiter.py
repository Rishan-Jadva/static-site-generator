import unittest

from inline_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_split_nodes_len(self):
        node = TextNode("I am **bold**, I am _italicized_, I am `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
    
    def test_multi_split(self):
        node = TextNode("I am **bold**, I am _italicized_, I am `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        newer_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual([
            TextNode("I am ", TextType.TEXT, None), 
            TextNode("bold", TextType.BOLD, None), 
            TextNode(", I am ", TextType.TEXT, None),
            TextNode("italicized", TextType.ITALIC, None),
            TextNode(", I am `code`", TextType.TEXT, None)
        ], newer_nodes)
    
if __name__ == "__main__":
    unittest.main()