import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",])

    def test_heading_single_hash(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_multiple_hashes(self):
        for i in range(1, 7):
            block = "#" * i + " Heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block_valid(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_invalid_start(self):
        block = "```\ncode line 1\ncode line 2\n"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_invalid_end(self):
        block = "code line 1\ncode line 2\n```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_all_lines_start_with_gt(self):
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_one_line_missing_gt(self):
        block = "> quote line 1\nnot a quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_valid(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_unordered_list_invalid(self):
        block = "- item 1\nitem 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_valid(self):
        block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_ordered_list_invalid(self):
        block = "1. item 1\n3. item 2"  # Wrong numbering
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_missing_dot(self):
        block = "1 item 1\n2 item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_default_to_paragraph(self):
        block = "Just a regular paragraph without any markdown formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()