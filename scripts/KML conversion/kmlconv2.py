import lxml.etree as ET
parser=ET.XMLParser(encoding='UTF-8')
tree=ET.parse('log.kml', parser=parser)
root=tree.getroot()

string=''

for folder in root.findall('{http://www.opengis.net/kml/2.2}Folder'):
    for play in folder.findall('{http://www.opengis.net/kml/2.2}Placemark'):
        for model in play.findall('{http://www.opengis.net/kml/2.2}Model'):
            for location in model.findall('{http://www.opengis.net/kml/2.2}Location'):
                long=location.find('{http://www.opengis.net/kml/2.2}longitude').text
                lat=location.find('{http://www.opengis.net/kml/2.2}latitude').text
                string=string + long + ',' + lat + ' '

tree2=ET.parse('wptemplate.gml')
root2=tree2.getroot()
for coords in root2.iter('{http://www.opengis.net/gml}coordinates'):
    coords.text=string
tree2.write('convertedpath.gml')