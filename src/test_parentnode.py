import unittest
from parentnode import ParentNode
from leafnode import LeafNode

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