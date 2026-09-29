import re
_RULES = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "<EMAIL>"),
          (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "<CARD>"),
          (re.compile(r"\+?\d[\d ()-]{8,}\d"), "<PHONE>")]

def scrub(text):
    for rx, tag in _RULES:
        text = rx.sub(tag, str(text))
    return text
