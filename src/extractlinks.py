import re
from textnode import TextNode

def extract_markdown_images(text):
    matches = re.findall(r"!\[([\w\s]*)\]\((https?:\/\/[^\s)]+)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[([\w\s]*)\]\((https?:\/\/[^\s)]+)\)",text)
    return matches

def split_nodes_image(old_nodes):
    output = []
    for old_node in old_nodes:
        image_nodes = extract_markdown_images(old_node.text)
        if image_nodes is None:
            output.append(old_node)
        image_text = old_node.text
        for image_node in image_nodes:
            split_text = image_text.split(f"![{image_node[0]}]({image_node[1]})",1)
            if len(split_text[0])>0:
                output.append(TextNode(split_text[0],"text"))
            output.append(TextNode(image_node[0],"image",image_node[1]))
            if len(split_text)>1:
                image_text = split_text[1]
        if len(image_text)>0:
            output.append(TextNode(image_text,"text"))
    return output

def split_nodes_links(old_nodes):
    output = []
    for old_node in old_nodes:
        link_nodes = extract_markdown_links(old_node.text)
        if link_nodes is None:
            output.append(old_node)
        link_text = old_node.text
        for link_node in link_nodes:
            split_text = link_text.split(f"[{link_node[0]}]({link_node[1]})",1)
            if len(split_text[0])>0:
                output.append(TextNode(split_text[0],"text"))
            output.append(TextNode(link_node[0],"link",link_node[1]))
            if len(split_text)>1:
                link_text = split_text[1]
        if len(link_text)>0:
            output.append(TextNode(link_text,"text"))
    return output