import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.LINK, url="https://boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_url_noteq(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, url="https://dev.boot")
        self.assertNotEqual(node, node2)

    def test_url_not_given(self):
        node = TextNode("This is a link node", TextType.LINK, url=None)
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_different_text_type(self):
        node = TextNode("This is a text node?", TextType.TEXT)
        node2 = TextNode("This is a text node?", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
if __name__ == "__main__":
    unittest.main()