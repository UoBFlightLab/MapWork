import lxml.etree as ET
with open ("wpout.txt", "r") as myfile:
    data=myfile.read().replace('\n', ' ')
    
tree=ET.parse('template.gml')
root=tree.getroot()
i=1
for coords in root.iter('{http://www.opengis.net/gml}coordinates'):
    coords.text=data
tree.write('path.gml')