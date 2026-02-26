from copy_directory import *
from generator import generate_page
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(os.path.dirname(script_dir), "static")
    public_dir = os.path.join(os.path.dirname(script_dir), "public")
    
    print("Starting directory copy...")
    copy_directory(static_dir, public_dir)
    print("Directory copy completed!")
    
    content_path = os.path.join(os.path.dirname(script_dir), "content", "index.md")
    template_path = os.path.join(os.path.dirname(script_dir), "template.html")
    dest_path = os.path.join(public_dir, "index.html")
    
    generate_page(content_path, template_path, dest_path)

if __name__ == '__main__':
    main()