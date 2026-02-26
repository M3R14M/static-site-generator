import unittest
from generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_h1_with_extra_whitespace(self):
        markdown = "#   Hello World   "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_h1_in_middle_of_document(self):
        markdown = "Some text\n\n# My Title\n\nMore text"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_h1_with_leading_whitespace(self):
        markdown = "  # Title with leading space"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with leading space")
    
    def test_no_h1_raises_exception(self):
        markdown = "Just some text without headers"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_only_h2_raises_exception(self):
        markdown = "## This is h2\n\n### This is h3"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_h1_without_space_raises_exception(self):
        markdown = "#NoSpace"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))
    
    def test_multiple_h1_returns_first(self):
        markdown = "# First Title\n\n# Second Title"
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")


if __name__ == "__main__":
    unittest.main()
