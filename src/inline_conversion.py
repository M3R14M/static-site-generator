import re
from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if len(parts) % 2 == 0:
            raise Exception(f"closing delimiter ({delimiter}) not found in '{node.text}'")
        split_nodes = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if parts[i] == parts[i].strip():
                split_nodes.append(TextNode(parts[i], text_type))
            else:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[([\w\s]*)]\((.{0,5}://[^\s]*)\)"
    return re.findall(regex, text)

def extract_markdown_links(text):
    regex = r"(?<!\!)\[([\w\s]*)]\((.{0,5}://[^\s]*)\)"
    return re.findall(regex, text)
