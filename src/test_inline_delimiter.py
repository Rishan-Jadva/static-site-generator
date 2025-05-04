import unittest

from inline_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def test_extract_images(self):
        text = "Dummy text ![alt text](url text) Dummy text"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [
            ("alt text", "url text")
        ])
    
    def test_extract_multiple_images(self):
        text = "Dummy text ![alt text](url text) Dummy text ![alt text](url text) Dummy text ![alt text](url text) Dummy text"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [
            ("alt text", "url text"),
            ("alt text", "url text"),
            ("alt text", "url text")
        ])
    
    def test_extract_links(self):
        text = "Dummy text [text](url text) Dummy text"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("text", "url text")
        ])
    
    def test_extract_multiple_links(self):
        text = "Dummy text [text](url text) Dummy text [text](url text) Dummy text [text](url text) Dummy text"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [
            ("text", "url text"),
            ("text", "url text"),
            ("text", "url text")
        ])
    
    def test_extract_links_not_images(self):
        text = "Dummy text ![image alt text](image url text) [link text](link url text)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("link text", "link url text")
        ], matches)


if __name__ == "__main__":
    unittest.main()