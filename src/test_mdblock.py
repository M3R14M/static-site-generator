import unittest
from mdblock import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just one paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph"])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels(self):
        for i in range(1, 7):
            md = f'{"#" * i} Heading {i}'
            self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_invalid_heading_no_space(self):
        self.assertNotEqual(block_to_block_type("#Heading"), BlockType.HEADING)
    
    def test_invalid_heading_length(self):
        self.assertNotEqual(block_to_block_type("####### Heading"), BlockType.HEADING)

    def test_code_block(self):
        md = "```\nprint(`hello`)\nx = 1\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_unclosed_code_block(self):
        md = "```\nprint('hello')"
        self.assertNotEqual(block_to_block_type(md), BlockType.CODE)
    
    def test_no_newline_code_block(self):
        md = "```print('hello')```"
        self.assertNotEqual(block_to_block_type(md), BlockType.CODE)

    def test_invalid_code_block(self):
        md = "`\nprint('hello')\n`"
        self.assertNotEqual(block_to_block_type(md), BlockType.CODE)

    def test_quote_block(self):
        md = "> quote line 1\n>quote line 2"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_invalid_quote_mixed_lines(self):
        md = "> quote line\nnot a quote"
        self.assertNotEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_unordered_list(self):
        md = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(md), BlockType.UL)

    def test_invalid_unordered_list_missing_space(self):
        md = "- item one\n-item two"
        self.assertNotEqual(block_to_block_type(md), BlockType.UL)

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(md), BlockType.OL)

    def test_invalid_ordered_list_non_incrementing(self):
        md = "1. first\n3. third\n2. second"
        self.assertNotEqual(block_to_block_type(md), BlockType.OL)

    def test_paragraph_fallback(self):
        md = "Just a normal paragraph with ```, 1. > and - "
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()