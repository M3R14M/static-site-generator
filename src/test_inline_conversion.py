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
        
class TestSplitNodesLinksAndImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links_single(self):
        node = TextNode(
            "Text with a [link](https://example.com/page)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/page"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Start [one](https://a.com) middle [two](https://b.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://a.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "Here is ![img](https://i.imgur.com/x.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is ![img](https://i.imgur.com/x.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_images_only_images(self):
        node = TextNode(
            "![one](https://a.com/1.png)![two](https://b.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://a.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://b.com/2.png"),
            ],
            new_nodes,
        )

    def test_split_images_at_start_and_end(self):
        node = TextNode(
            "![start](https://a.com/s.png) middle ![end](https://b.com/e.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://a.com/s.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://b.com/e.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_matches(self):
        node = TextNode("No images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_no_matches(self):
        node = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_mixed_node_types(self):
        node1 = TextNode("Text [link](https://a.com)", TextType.TEXT)
        node2 = TextNode("img", TextType.IMAGE, "https://b.com/x.png")
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com"),
                node2,
            ],
            new_nodes,
        )

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_all_types(self):
        text = "This is **bold** and _italic_ with `code` and ![image](https://example.com/img.png) and [link](https://example.com)"
        new_nodes = text_to_textnodes(text)
        nodes_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, nodes_list)

    def test_text_to_textnodes_plain_text(self):
        text = "just plain text"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [TextNode("just plain text", TextType.TEXT)])

    def test_text_to_textnodes_multiple_same_formatting(self):
        text = "**bold one** and **bold two** with _italic one_ and _italic two_"
        new_nodes = text_to_textnodes(text)
        nodes_list = [
            TextNode("bold one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold two", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("italic one", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic two", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, nodes_list)


if __name__ == "__main__":
    unittest.main()