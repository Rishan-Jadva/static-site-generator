import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_h1_title(self):
        markdown = "# My Blog Title"
        title = extract_title(markdown)
        self.assertEqual(title, "My Blog Title")

    def test_multiple_headings_only_h1_used(self):
        markdown = "# First Title\n\n## Subheading\n\n### Another Subheading"
        title = extract_title(markdown)
        self.assertEqual(title, "First Title")

    def test_title_with_extra_whitespace(self):
        markdown = "#    Spaced Out Title    "
        title = extract_title(markdown)
        self.assertEqual(title, "Spaced Out Title")

    def test_ignores_non_h1_headings(self):
        markdown = "## Not a Title\n\n### Still Not a Title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No Level 1 Heading Detected", str(context.exception))

    def test_raises_exception_on_empty_input(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No Level 1 Heading Detected", str(context.exception))

    def test_title_not_returned_if_malformed_h1(self):
        markdown = "#This is not a valid H1 heading"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertIn("No Level 1 Heading Detected", str(context.exception))

if __name__ == "__main__":
    unittest.main()
