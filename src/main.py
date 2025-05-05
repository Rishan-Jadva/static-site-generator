import os, shutil

def main():
    directory_copy("./static/", "./public/", first_call=True)

def directory_copy(source_path, destination_path, first_call=False):
    if first_call:
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)
        os.mkdir("./public")
    
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        destination_item_path = os.path.join(destination_path, item)

        if os.path.isdir(source_item_path):
            os.mkdir(destination_item_path)
            directory_copy(source_item_path, destination_item_path)
        else:
            shutil.copy(source_item_path, destination_item_path)
main()