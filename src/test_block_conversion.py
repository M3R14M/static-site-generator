import unittest
from block_conversion import *


class TestBlockConversion(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Heading</h1></div>")

    def test_unordered_list(self):
        md = """
- one
- two
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ul><li>one</li><li>two</li></ul></div>")

    def test_ordered_list(self):
        md = """
1. first
2. second
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ol><li>first</li><li>second</li></ol></div>")


if __name__ == "__main__":
    unittest.main()