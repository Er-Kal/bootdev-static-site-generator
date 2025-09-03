import unittest

from splitdelimiter import split_nodes_delimiter
from textnode import TextNode,TextType
from extractlinks import extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_links

class TestSplitDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_italics(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])
    
    
    def test_two_italics(self):
        node = TextNode("This is _text_ with two _italic_ words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,[
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.ITALIC),
            TextNode(" with two ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT),
        ])

    def test_starts_with_italics(self):
        node = TextNode("_This text_ starts with italics", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,[
            TextNode("This text", TextType.ITALIC),
            TextNode(" starts with italics", TextType.TEXT),
        ])

    def test_ends_with_italics(self):
        node = TextNode("This text _ends with italics_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,[
            TextNode("This text ", TextType.TEXT),
            TextNode("ends with italics", TextType.ITALIC),
        ])

    def test_has_no_closing_delimiter_italics(self):
        node = TextNode("This text _has an italic word","text")
        with self.assertRaises(Exception, msg="There was no closing delimiter"):
            new_nodes = split_nodes_delimiter([node],"_",TextType.ITALIC)

class TestMarkdownImageConverter(unittest.TestCase):
    def test_one_link(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(matches,[('rick roll', 'https://i.imgur.com/aKaOqIh.gif')])
    
    def test_two_link(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(matches,[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),('obi wan','https://i.imgur.com/fJRm4Vk.jpeg')])

class TestMarkdownLinkConverter(unittest.TestCase):
    def test_one_link(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertEqual(matches,[('to boot dev', 'https://www.boot.dev')])
    
    def test_two_link(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(matches,[('to boot dev', 'https://www.boot.dev'),('to youtube', 'https://www.youtube.com/@bootdotdev')])

class TestSplitImages(unittest.TestCase):
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

    def test_split_single_image(self):
        node = TextNode(
            "Here is an ![example](https://example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("example", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_no_image(self):
        node = TextNode(
            "Here is a text node with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is a text node with no images", TextType.TEXT),
            ],
            new_nodes,
        )
    
class TestSplitLinks(unittest.TestCase):
    def test_no_links(self):
        node = TextNode("This is just plain text.","text")
        result = split_nodes_links([node])
        self.assertEqual(result, [node])

    def test_single_link(self):
        node = TextNode("This is a [link](http://example.com) in text.","text")
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "http://example.com"),
            TextNode(" in text.", "text")
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode("Check [Google](https://google.com) and [Bing](https://bing.com).","text")
        expected = [
            TextNode("Check ", "text"),
            TextNode("Google", "link", "https://google.com"),
            TextNode(" and ", "text"),
            TextNode("Bing", "link", "https://bing.com"),
            TextNode(".", "text")
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode("[Start](http://start.com) and then some text.","text")
        expected = [
            TextNode("Start", "link", "http://start.com"),
            TextNode(" and then some text.", "text")
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    def test_link_only(self):
        node = TextNode("[Only](http://only.com)","text")
        expected = [
            TextNode("Only", "link", "http://only.com")
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)