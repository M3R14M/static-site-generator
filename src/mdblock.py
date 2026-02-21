import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL ="ordered_list"

def block_to_block_type(markdown):
    if isheading(markdown):
        return BlockType.HEADING
    if iscode(markdown):
        return BlockType.CODE
    if isquote(markdown):
        return BlockType.QUOTE
    if isulist(markdown):
        return BlockType.UL
    if isolist(markdown):
        return BlockType.OL
    return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    return list(map(lambda l: l.strip("\n"), filter(lambda m: m.strip(), markdown.split("\n\n"))))

# BlockType determination
def isheading(md):
    return re.match(r"^#{1,6}\s", md)

def iscode(md):
    return re.match(r"\A`{3}\n(?!.*`{3}.*\n)(?:.*\n)*`{3}\n?\Z", md, re.S)

def isquote(md):
    return re.match(r"\A(?:^>.*$\n?)+\Z", md, re.M)

def isulist(md):
    return re.match(r"\A(?:^\-\s.*$\n?)+\Z", md, re.M)

def isolist(md):
    match = re.findall(r"^([\d])+\.\s", md, re.M)
    if not match:
        return False
    for i in range(len(match)):
        if int(match[i]) != (i + 1):
            return False
    return True