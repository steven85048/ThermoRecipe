import re

def remove_punctuation(str):
    # No numbers, alphabetic characterse, or dashes removed
    str = re.sub(r'[^\w\s-]','',str)
    return str