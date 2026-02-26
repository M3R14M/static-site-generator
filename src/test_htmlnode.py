import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_single_child(self):
        child = LeafNode("span", "child text")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><span>child text</span></div>")

    def test_to_html_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode("i", "italic")
        node = ParentNode("p", [child1, child2])
        self.assertEqual(node.to_html(), "<p><b>bold</b><i>italic</i></p>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "content")
        node = ParentNode("section", [child], {"class": "main"})
        self.assertIn('class="main"', node.to_html())
        self.assertTrue(node.to_html().startswith('<section'))
        self.assertTrue(node.to_html().endswith('</section>'))

    def test_to_html_no_tag_raises(self):
        child = LeafNode("span", "content")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_nested_parent(self):
        leaf = LeafNode("em", "deep")
        inner = ParentNode("span", [leaf])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><span><em>deep</em></span></div>")


if __name__ == "__main__":
    unittest.main()