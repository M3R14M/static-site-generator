from htmlnode import ParentNode, LeafNode
from inline_conversion import text_to_textnodes
from mdblock import *
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                nodes.append(heading_node(block))
            case BlockType.CODE:
                nodes.append(code_node(block))
            case BlockType.QUOTE:
                nodes.append(quote_node(block))
            case BlockType.UL:
                nodes.append(ul_node(block))
            case BlockType.OL:
                nodes.append(ol_node(block))
            case _:
                nodes.append(paragraph_node(block))
    return ParentNode("div", nodes)
        
    """
1. Split the markdown into blocks (you already have a function for this)
2. Loop over each block:

    1. Determine the type of block (you already have a function for this)
    2. Based on the type of block, create a new HTMLNode with the proper data
    3. Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
    4. The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.

3. Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
4. Create unit tests. Here are two to get you started:
"""

def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def heading_node(block):
    sections = re.findall(r"^(#+)\s(.*)", block)
    n = len(sections[0][0])
    return LeafNode(f"h{n}", sections[0][1])

def code_node(block):
    content = re.sub(r"`{3}\n?", '', block, flags=re.M)
    return ParentNode("pre", [LeafNode("code", content)])

def quote_node(block):
    content = re.sub(r'^>\s?', '', block, flags=re.M).strip()
    return ParentNode("blockquote", text_to_children(content))

def ul_node(block):
    return list_node(block, r"^-\s", "ul")
    
def ol_node(block):
    return list_node(block, r"^\d+\.\s", "ol")

def paragraph_node(block):
    content = block.replace("\n", " ")
    return ParentNode("p", text_to_children(content))

def list_node(block, pattern, tag):
    items = [
        ParentNode("li", text_to_children(re.sub(pattern, "", line)))
        for line in block.split("\n")
    ]
    return ParentNode(tag, items)