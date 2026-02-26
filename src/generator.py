import os
from block_conversion import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and not stripped.startswith('## '):
            return stripped[2:].strip()
    raise Exception("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(full_html)


def generate_pages_recursive(content_dir, template_path, dest_dir, basepath):
    items = os.listdir(content_dir)
    for item in items:
        src_path = os.path.join(content_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                dest_html = os.path.splitext(dest_path)[0] + ".html"
                generate_page(src_path, template_path, dest_html, basepath)
            continue
        os.makedirs(dest_path, exist_ok=True)
        generate_pages_recursive(src_path, template_path, dest_path, basepath)
