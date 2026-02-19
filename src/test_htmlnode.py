import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "click here", None, {"href": "https://meriam.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://meriam.dev" target="_blank"')
    
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "paragraph text")
        self.assertEqual(node.props_to_html(), '')
    
    def test_repr(self):
        node = HTMLNode("div", "content", None, {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, content, None, {'class': 'container'})")


if __name__ == "__main__":
    unittest.main()