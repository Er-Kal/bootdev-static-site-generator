import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# This is a heading"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### Small heading"),
            BlockType.HEADING
        )

    def test_code_block(self):
        code_block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(
            block_to_block_type(code_block),
            BlockType.CODE
        )

    def test_quote_block(self):
        quote_block = "> This is a quote\n> with two lines"
        self.assertEqual(
            block_to_block_type(quote_block),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        ul_block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(
            block_to_block_type(ul_block),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        ol_block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(
            block_to_block_type(ol_block),
            BlockType.ORDERED_LIST
        )

    def test_paragraph(self):
        para = "This is a regular paragraph of text.\nIt has multiple lines."
        self.assertEqual(
            block_to_block_type(para),
            BlockType.PARAGRAPH
        )

    def test_mixed_list_failure(self):
        mixed_block = "1. First item\n3. Skipped number"
        self.assertEqual(
            block_to_block_type(mixed_block),
            BlockType.PARAGRAPH
        )

    def test_incorrect_heading(self):
        not_heading = "####### Too many hashes"
        self.assertEqual(
            block_to_block_type(not_heading),
            BlockType.PARAGRAPH
        )

if __name__ == '__main__':
    unittest.main()