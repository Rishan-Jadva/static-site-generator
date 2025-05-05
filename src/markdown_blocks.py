from enum import Enum
from htmlnode import ParentNode
from inline_delimiter import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered = []
    for block in blocks:
        if block == "":
            continue
        filtered.append(block.strip())
    return filtered

def block_to_block_type(block):
    lines = block.split('\n')
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.OLIST:
            return ordered_list_to_html_node(block)
        case BlockType.ULIST:
            return unordered_list_to_html_node(block)
        case _:
            raise ValueError("Invalid Block Type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    hash = 0
    for char in block:
        if char == "#":
            hash += 1
        else:
            break
    text = block[hash:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{hash}", children)



def code_to_html_node(block):
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    new_children = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_line = ParentNode("li", children)
        new_children.append(html_line)
    return ParentNode("ol", new_children)
    

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    new_children = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_line = ParentNode("li", children)
        new_children.append(html_line)
    return ParentNode("ul", new_children)