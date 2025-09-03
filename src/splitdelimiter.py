from textnode import TextType,TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        split_text = node.text.split(delimiter)
        if len(split_text)%2==0:
            raise Exception("There was no closing delimiter")
        for i in range(len(split_text)):
            if i%2==0 and len(split_text[i])>0:
                new_nodes.append(TextNode(split_text[i],TextType.TEXT))
            elif i%2==1:
                new_nodes.append(TextNode(split_text[i],text_type))
    return new_nodes