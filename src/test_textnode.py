import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This text is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This text is bold")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev", "alt": "This is an image"})
        
if __name__ == "__main__":
    unittest.main()