import unittest

from inline_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_split_nodes_image_case1(self):
        node = TextNode("whatever ![alt](url)", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case2(self):
        node = TextNode("![alt](url) whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" whatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_image_case3(self):
        node = TextNode("![alt](url)", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case4(self):
        node = TextNode("whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_image_case5(self):
        node = TextNode("whatever ![alt](url) whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" whatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_image_case6(self):
        node = TextNode("![alt](url) whatever ![alt2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" whatever ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case7(self):
        node = TextNode("![alt](url)![alt2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("alt2", TextType.IMAGE, "url2")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case8(self):
        node = TextNode("whateverwhatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whateverwhatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_image_case9(self):
        node = TextNode("![alt](url)![alt2](url2)whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("alt2", TextType.IMAGE, "url2"),
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_image_case10(self):
        node = TextNode("whatever![alt](url)![alt2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("alt2", TextType.IMAGE, "url2")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case11(self):
        node = TextNode("![alt](url)whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_image_case12(self):
        node = TextNode("whatever![alt](url)", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case13(self):
        node = TextNode("![alt](url)whatever![alt2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("whatever", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2")
        ], split_nodes_image([node]))

    def test_split_nodes_image_case14(self):
        node = TextNode("whatever![alt](url)whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_image([node]))

    def test_split_nodes_link_case1(self):
        node = TextNode("whatever [text](url)", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever ", TextType.TEXT),
            TextNode("text", TextType.LINK, "url")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case2(self):
        node = TextNode("[text](url) whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url"),
            TextNode(" whatever", TextType.TEXT)
        ], split_nodes_link([node]))

    def test_split_nodes_link_case3(self):
        node = TextNode("[text](url)", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case4(self):
        node = TextNode("whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_link([node]))

    def test_split_nodes_link_case5(self):
        node = TextNode("whatever [text](url) whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever ", TextType.TEXT),
            TextNode("text", TextType.LINK, "url"),
            TextNode(" whatever", TextType.TEXT)
        ], split_nodes_link([node]))

    def test_split_nodes_link_case6(self):
        node = TextNode("[text](url) whatever [text2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url"),
            TextNode(" whatever ", TextType.TEXT),
            TextNode("text2", TextType.LINK, "url2")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case7(self):
        node = TextNode("[text](url)[text2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url"),
            TextNode("text2", TextType.LINK, "url2")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case8(self):
        node = TextNode("whateverwhatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whateverwhatever", TextType.TEXT)
        ], split_nodes_link([node]))

    def test_split_nodes_link_case9(self):
        node = TextNode("[text](url)[text2](url2)whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url"),
            TextNode("text2", TextType.LINK, "url2"),
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_link([node]))

    def test_split_nodes_link_case10(self):
        node = TextNode("whatever[text](url)[text2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT),
            TextNode("text", TextType.LINK, "url"),
            TextNode("text2", TextType.LINK, "url2")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case11(self):
        node = TextNode("[text](url)whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url"),
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_link([node]))

    def test_split_nodes_link_case12(self):
        node = TextNode("whatever[text](url)", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT),
            TextNode("text", TextType.LINK, "url")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case13(self):
        node = TextNode("[text](url)whatever[text2](url2)", TextType.TEXT)
        self.assertListEqual([
            TextNode("text", TextType.LINK, "url"),
            TextNode("whatever", TextType.TEXT),
            TextNode("text2", TextType.LINK, "url2")
        ], split_nodes_link([node]))

    def test_split_nodes_link_case14(self):
        node = TextNode("whatever[text](url)whatever", TextType.TEXT)
        self.assertListEqual([
            TextNode("whatever", TextType.TEXT),
            TextNode("text", TextType.LINK, "url"),
            TextNode("whatever", TextType.TEXT)
        ], split_nodes_link([node]))


if __name__ == "__main__":
    unittest.main()