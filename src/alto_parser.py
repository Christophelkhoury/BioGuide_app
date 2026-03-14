from lxml import etree

def alto_to_text(alto_xml: str) -> str:
    root = etree.fromstring(alto_xml.encode("utf-8", errors="ignore"))
    strings = root.xpath(".//*[local-name()='String']")
    words = []
    for s in strings:
        c = s.attrib.get("CONTENT")
        if c:
            words.append(c)
    return " ".join(words)
