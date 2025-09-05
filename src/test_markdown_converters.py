import unittest

from markdown_converters import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_bootdev_markdown_to_blocks(self):
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
    
    def test_bootdev_markdown_to_blocks_one_line(self):
        md = """
        This is **bolded** paragraph
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )
    
    def test_bootdev_markdown_to_blocks_no_lines(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "",
            ],
        )
    
    def test_bootdev_markdown_to_blocks_no_lines_again(self):
        md = """
        
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "",
            ],
        )