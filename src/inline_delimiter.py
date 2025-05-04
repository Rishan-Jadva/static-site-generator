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