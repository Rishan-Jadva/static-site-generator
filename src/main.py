from textnode import TextNode, TextType

def main():
    node = TextNode("This is some anchor text", TextType("link"), "https://boot.dev")
    print(node)

main()