import os
import shutil


def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Deleted: {destination}")
    
    os.mkdir(destination)
    print(f"Created: {destination}")
    
    copy_recursive_helper(source, destination)


def copy_recursive_helper(source, destination):
    items = os.listdir(source)
    
    for item in items:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")
        else:
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            copy_recursive_helper(src_path, dest_path)
