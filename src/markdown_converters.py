

def markdown_to_blocks(markdown):
    split_text = markdown.split("\n")
    output = []
    block = ""
    for text in split_text:
        if block=="" and text=="":
            continue
        elif block=="":
            block=text.strip()
        elif block!="" and text=="":
            output.append(block)
            block=""
        else:
            block+="\n"+text.strip()
    output.append(block.strip("\n"))
    return output
