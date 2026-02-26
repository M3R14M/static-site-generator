from copy_directory import *
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(os.path.dirname(script_dir), "static")
    public_dir = os.path.join(os.path.dirname(script_dir), "public")
    
    print("Starting directory copy...")
    copy_directory(static_dir, public_dir)
    print("Directory copy completed!")

if __name__ == '__main__':
    main()