class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        prop_string = ""
        if not self.props:
            return prop_string
        for prop, value in self.props.items():
            prop_string += f" {prop}=\"{value}\""
        return prop_string
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props


    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        return f"{"<"+self.tag}{super().props_to_html() + ">"}{self.value}{"</" +self.tag + ">"}"
    
    def __repr__(self):
        return f"LeafNode(tag = {self.tag}, value = {self.value}, props = {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("missing children")
        
        tag_string = f"<{self.tag}{super().props_to_html()}>"

        for child in self.children:
            tag_string += child.to_html()
        tag_string += f"</{self.tag}>"

        return tag_string