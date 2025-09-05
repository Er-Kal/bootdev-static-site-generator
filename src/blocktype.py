from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if check_if_starts_with_char(block,"> "):
        return BlockType.QUOTE
    if check_if_starts_with_char(block,"- "):
        return BlockType.UNORDERED_LIST
    if check_if_ordered_list(block):
        return BlockType.ORDERED_LIST
    if re.match(r"^[#]{1,6} ",block):
        return BlockType.HEADING
    return BlockType.PARAGRAPH
    
def check_if_starts_with_char(block,prefix):
    flag = True
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(prefix):
            flag = False
    return flag

def check_if_ordered_list(block):
    flag = True
    lines = block.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            flag = False
    return flag