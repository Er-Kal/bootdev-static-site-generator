import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_basic(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_type(self):
        node = TextNode("This is an image", "image", "https://placehold.co/600x400")
        node2 = TextNode("This is an image", TextType.IMAGE, "https://placehold.co/600x400")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is an image", "image", "https://placehold.co/600x400")
        node2 = TextNode("This is an image", TextType.IMAGE, "https://placehold.co/400")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()