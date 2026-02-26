import re
from textnode import *


def text_to_textnodes(text):
   node = [TextNode(text, TextType.TEXT)]
   node = split_nodes_image(node)
   node = split_nodes_link(node)
   node = split_nodes_delimiter(node, "`", TextType.CODE)
   node = split_nodes_delimiter(node, "**", TextType.BOLD)
   node = split_nodes_delimiter(node, "_", TextType.ITALIC)
   return node

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

def split_nodes_image(old_nodes):
    regex = r"(!\[[^\]]*\]\([^\s)]+\))"
    fn = extract_markdown_images
    return split_nodes_helper(old_nodes, regex, TextType.IMAGE, fn)
    
def split_nodes_link(old_nodes):
    regex = r"((?<!\!)\[[^\(\)]*\]\([^\s)]+\))"
    fn = extract_markdown_links
    return split_nodes_helper(old_nodes, regex, TextType.LINK, fn)

def split_nodes_helper(old_nodes, regex, text_type, extraction_function):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = re.split(regex, node.text)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        split_nodes = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if re.match(regex, parts[i]):
                extr = extraction_function(parts[i])
                split_nodes.append(TextNode(extr[0][0], text_type, extr[0][1]))
            else:
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[([^\]]*)\]\(([^\s)]+)\)"
    return re.findall(regex, text)

def extract_markdown_links(text):
    regex = r"(?<!\!)\[([^\]]*)\]\(([^\s)]+)\)"
    return re.findall(regex, text)

