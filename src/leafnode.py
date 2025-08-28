from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        output = f'<{self.tag}'
        if self.props is not None:
            output+=" "+self.props_to_html()
        output+='>'
        output+=f'{self.value}'
        output+=f'</{self.tag}>'
        return output