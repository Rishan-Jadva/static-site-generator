import unittest

from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Hello World!")
        node2 = HTMLNode("p", "Hello World!")
        self.assertEqual(node, node2)
    
    def test_empty_eq(self):
        node = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node, node2)
    
    def test_child_noteq(self):
        child = HTMLNode("p", "Hello, I am a child!")
        parent = HTMLNode("div", None, child)
        child2 = HTMLNode("p", "Hello, I am a child too!")
        parent2 = HTMLNode("div", None, child2)
        self.assertNotEqual(parent, parent2)

    def test_props_to_html(self):
        node = HTMLNode("a", None, None, {"href":"https://boot.dev", "target":"_blank"})
        self.assertEqual(" href=\"https://boot.dev\" target=\"_blank\"", node.props_to_html())

    def test_repr(self):
        node = HTMLNode("img", None, None, {"src":"/images.png"})
        self.assertEqual("HTMLNode(tag = img, value = None, children = None, props = {'src': '/images.png'})", repr(node))

    def test_leafnode_creation(self):
        leaf = LeafNode("div", "Hello!")
        self.assertEqual("LeafNode(tag = div, value = Hello!, props = None)", repr(leaf))
    
    def test_leaf_to_html_a(self):
        leaf = LeafNode("a", "Click Me!", {"href": "https://boot.dev"})
        self.assertEqual(leaf.to_html(), "<a href=\"https://boot.dev\">Click Me!</a>")

    def test_leaf_no_tag(self):
        leaf = LeafNode(None, "My Text!")
        self.assertEqual(leaf.to_html(), "My Text!")

    
if __name__ == "__main__":
    unittest.main()