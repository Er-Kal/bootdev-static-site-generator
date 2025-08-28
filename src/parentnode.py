from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        output = f'<{self.tag}'
        if self.props is not None:
            output+=" "+self.props_to_html()
        output+='>'
        for child in self.children:
            output+=child.to_html()
        output+=f'</{self.tag}>'
        return output