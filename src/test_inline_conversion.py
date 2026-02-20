import unittest
from inline_conversion import *


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        nodes_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, nodes_list)
    
    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, nodes_list)

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        nodes_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, nodes_list)

    def test_multiple_same_type(self):
        node = TextNode("**one** and **two**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes_list = [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, nodes_list)

    def test_no_delimiter(self):
        node = TextNode("no delimiters here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_multiple_node_types(self):
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        node2 = TextNode("link", TextType.LINK, "https://meriam.dev")
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        nodes_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            node2,
        ]
        self.assertEqual(new_nodes, nodes_list)

    def test_no_closing_delimiter(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

class TestExtractLinksAndImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
     
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://meriam.dev)"
        )
        self.assertListEqual([("link", "https://meriam.dev")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with ![one](https://meriam.dev/one.png) and ![two](https://meriam.dev/two.png)"
        )
        self.assertListEqual(
            [("one", "https://meriam.dev/one.png"), ("two", "https://meriam.dev/two.png")],
            matches,
        )

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with [one](https://meriam.dev/one) and [two](https://meriam.dev/two)"
        )
        self.assertListEqual(
            [("one", "https://meriam.dev/one"), ("two", "https://meriam.dev/two")],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is text with ![image](https://i.imgur.com/aKaOqIh.gif) and [link](https://meriam.dev)"
        )
        self.assertNotIn(("image", "https://i.imgur.com/aKaOqIh.gif"), matches)
        
