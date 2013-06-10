import xml.etree.ElementTree as ET

rep = open("./data/isbn_to_work.csv", "a")

xml = ET.parse("./data/feeds/works_to_isbn_small.xml")
for work in xml.getroot():
    for isbn in work.findall("./isbns/isbn"):
        rep.write(",".join([isbn.text, work.attrib["workcode"]+"\n"]))
