import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "plain text")
        self.assertEqual(node.to_html(), "plain text")
    
    def test_to_html_with_tag(self):
        node = LeafNode("p", "paragraph text")
        self.assertEqual(node.to_html(), "<p>paragraph text</p>")
    
    def test_to_html_with_props(self):
        node = LeafNode("a", "link text", {"href": "https://meriam.dev"})
        self.assertEqual(node.to_html(), '<a href="https://meriam.dev">link text</a>')
    
    def test_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_empty_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_different_tags(self):
        node = LeafNode("b", "bold text")
        self.assertEqual(node.to_html(), "<b>bold text</b>")
        
        node = LeafNode("i", "italic text")
        self.assertEqual(node.to_html(), "<i>italic text</i>")
        
        node = LeafNode("span", "span text")
        self.assertEqual(node.to_html(), "<span>span text</span>")
    
    def test_to_html_multiple_props(self):
        node = LeafNode("a", "click here", {"href": "https://meriam.dev", "target": "_blank"})
        self.assertIn('href="https://meriam.dev"', node.to_html())
        self.assertIn('target="_blank"', node.to_html())


if __name__ == "__main__":
    unittest.main()