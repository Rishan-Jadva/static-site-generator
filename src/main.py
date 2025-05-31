import os, shutil, sys, re
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    static_dir = "./static"
    public_dir = "./docs"
    content_dir = "./content"
    template_path = "./template.html"
    directory_copy(static_dir, public_dir, True)
    generate_pages_recursive(content_dir, template_path, public_dir, basepath)

def preprocess_markdown(content):
    def replace_image(match):
        image_name = match.group(1).strip()
        return f"![{image_name}](/images/{image_name})"

    content = re.sub(r'!\[\[(.*?)\]\]', replace_image, content)
    return content

def directory_copy(source_path, destination_path, first_call=False):
    if first_call:
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)
        os.mkdir("./docs")
    
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        destination_item_path = os.path.join(destination_path, item)

        if os.path.isdir(source_item_path):
            os.mkdir(destination_item_path)
            directory_copy(source_item_path, destination_item_path)
        else:
            shutil.copy(source_item_path, destination_item_path)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if block[:2] == "# ":
                return block[2:].strip()
    raise Exception("No Level 1 Heading Detected")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as from_file:
        from_path_content = from_file.read()
    with open(template_path) as template:
        template_path_content = template.read()

    from_path_content = preprocess_markdown(from_path_content)
    node = markdown_to_html_node(from_path_content)
    html_string = node.to_html()

    title = extract_title(from_path_content)

    template_path_content = template_path_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace('href="/', 'href="' + basepath).replace('src="/', 'src="' + basepath)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_path_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        new_content = os.path.join(dir_path_content, item)
        new_dest = os.path.join(dest_dir_path, item)

        if os.path.isdir(new_content):
            os.mkdir(new_dest)
            generate_pages_recursive(new_content, template_path, new_dest, basepath)
        else:
            filename_without_ext = os.path.splitext(item)[0]
            new_dest_file = os.path.join(dest_dir_path, filename_without_ext + ".html")
            generate_page(new_content, template_path, new_dest_file, basepath)

main()