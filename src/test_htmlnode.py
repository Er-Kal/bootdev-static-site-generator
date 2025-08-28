import unittest

from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_node_to_html_node,TextNode,TextType


class TestHTMLNode(unittest.TestCase):
    def test_eq_basic(self):
        node1 = HTMLNode("p","value1",[],{"href":"https://example.com"})
        node2 = HTMLNode("p","value1",[],{"href":"https://example.com"})
        self.assertEqual(node1, node2)
    
    def test_props_to_html(self):
        node1 = HTMLNode("p","value1",[],{"href":"https://example.com"})
        self.assertEqual(node1.props_to_html(), 'href="https://example.com"')

    def test_not_eq(self):
        node1 = HTMLNode("p","value1",[],{"href":"https://example.com"})
        node2 = HTMLNode("div","value2",[],{"style":"display:flex"})
        self.assertNotEqual(node1, node2)
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_div_with_props(self):
        node = LeafNode("div", "Content", {"class":"my-class", "id":"my-id"})
        self.assertEqual(node.to_html(), '<div class="my-class" id="my-id">Content</div>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError, msg="LeafNode must have a value"):
            node.to_html()
    
class TestParentNode(unittest.TestCase):
    def test_parent_node_with_p_child(self):
        node = LeafNode("p", "Hello, world!")
        parent = ParentNode("div",[node])
        self.assertEqual(parent.to_html(),"<div><p>Hello, world!</p></div>")
    
    def test_parent_node_bootdev_suggestion(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
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

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", "bold")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", "italic")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"i")
        self.assertEqual(html_node.value, "This is an italic node")
        
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"code")
        self.assertEqual(html_node.value, "This is a code node")
        
    def test_link(self):
        node = TextNode("This is a link", "link", "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props,{"href":"https://google.com"})
    
    def test_image(self):
        node = TextNode("This is an image","image","https://placehold.co/100x100")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"img")
        self.assertEqual(html_node.value,"")
        self.assertEqual(html_node.props,{"src":"https://placehold.co/100x100","alt":"This is an image"})
            
if __name__ == "__main__":
    unittest.main()