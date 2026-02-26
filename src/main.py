from copy_directory import *
from generator import generate_pages_recursive
import os
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(os.path.dirname(script_dir), "static")
    public_dir = os.path.join(os.path.dirname(script_dir), "docs")
    
    print("Starting directory copy...")
    copy_directory(static_dir, public_dir)
    print("Directory copy completed!")
    
    content_path = os.path.join(os.path.dirname(script_dir), "content")
    template_path = os.path.join(os.path.dirname(script_dir), "template.html")
    
    generate_pages_recursive(content_path, template_path, public_dir, basepath)

if __name__ == '__main__':
    main()