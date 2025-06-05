import os
import shutil

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
notes_directory = os.path.join(parent_directory, "Notes")
writeups_directory = os.path.join(parent_directory, "Writeups")
content_notes_directory = os.path.join(current_directory, "content/notes")
content_thm_directory = os.path.join(current_directory, "content/tryhackme")
content_htb_directory = os.path.join(current_directory, "content/hackthebox")
image_dir = os.path.join(current_directory, "static/images")

def append_file(index_path, md_filename):
    html_filename = os.path.splitext(md_filename)[0] + '.html'
    link_line = f"- [{md_filename[:-3]}]({html_filename})"

    with open(index_path, "a") as f:
        f.write(link_line + "\n")

for file in os.listdir(writeups_directory):
    if file.startswith('.'):
        continue
    file_path = os.path.join(writeups_directory, file)

    if "HTB" in file:
        dest_path = os.path.join(content_htb_directory, file)
        if not os.path.exists(dest_path):
            shutil.copy2(file_path, content_htb_directory)
            index_path = os.path.join(content_htb_directory, "index.md")
            append_file(index_path, file)
    
    elif "THM" in file:
        dest_path = os.path.join(content_thm_directory, file)
        if not os.path.exists(dest_path):
            shutil.copy2(file_path, content_thm_directory)
            index_path = os.path.join(content_thm_directory, "index.md")
            append_file(index_path, file)
    
    elif os.path.isdir(file_path) and "attachments" in file_path:
        for image in os.listdir(file_path):
            src_image_path = os.path.join(file_path, image)
            dest_image_path = os.path.join(image_dir, image)
            if not os.path.exists(dest_image_path):
                shutil.copy2(src_image_path, image_dir)

for file in os.listdir(notes_directory):
    if file.startswith('.'):
        continue
    file_path = os.path.join(notes_directory, file)
    
    if ".md" in file:
        dest_path = os.path.join(content_notes_directory, file)
        if not os.path.exists(dest_path):
            shutil.copy2(file_path, content_notes_directory)
            index_path = os.path.join(content_notes_directory, "index.md")
            append_file(index_path, file)

    elif os.path.isdir(file_path) and "attachments" in file_path:
        for image in os.listdir(file_path):
            src_image_path = os.path.join(file_path, image)
            dest_image_path = os.path.join(image_dir, image)
            if not os.path.exists(dest_image_path):
                shutil.copy2(os.path.join(file_path, image), image_dir)