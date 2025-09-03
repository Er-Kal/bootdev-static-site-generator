from extractlinks import split_nodes_image,split_nodes_links

from splitdelimiter import split_nodes_delimiter

from textnode import TextNode, TextType


def text_to_nodes(text):
    node = TextNode(text, TextType.TEXT)
    output_nodes = []
    output_nodes = split_nodes_delimiter([node],"_",TextType.ITALIC)
    output_nodes = split_nodes_delimiter(output_nodes,"**",TextType.BOLD)
    output_nodes = split_nodes_delimiter(output_nodes,"`",TextType.CODE)
    output_nodes = split_nodes_image(output_nodes)
    output_nodes = split_nodes_links(output_nodes)
    return output_nodes