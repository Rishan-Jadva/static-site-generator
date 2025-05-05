def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered = []
    for block in blocks:
        if block == "":
            continue
        filtered.append(block.strip())
    return filtered