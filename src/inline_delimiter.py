import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        for i in range(len(split_nodes)):
            if i % 2 == 1:
                split_nodes[i] = TextNode(split_nodes[i], text_type)
            else:
                if split_nodes[i] == "":
                    continue
                split_nodes[i] = TextNode(split_nodes[i], TextType.TEXT)
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted_tuple = extract_markdown_images(node.text)
        if len(extracted_tuple) == 0:
            new_nodes.append(node)
            continue

        temp_text = node.text
        for alt, url in extracted_tuple:
            split_str = f"![{alt}]({url})"
            sections = temp_text.split(split_str, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            temp_text = sections[1]
        if temp_text != "":
            new_nodes.append(TextNode(temp_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted_tuple = extract_markdown_links(node.text)
        if len(extracted_tuple) == 0:
            new_nodes.append(node)
            continue

        temp_text = node.text
        for text, url in extracted_tuple:
            split_str = f"[{text}]({url})"
            sections = temp_text.split(split_str, 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            temp_text = sections[1]
        if temp_text != "":
            new_nodes.append(TextNode(temp_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
    