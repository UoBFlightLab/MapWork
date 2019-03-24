import lxml.etree as ET
parser=ET.XMLParser(encoding='UTF-8')
tree=ET.parse('log.kml', parser=parser)
root=tree.getroot()

string=''

for tour in root.findall('{http://www.google.com/kml/ext/2.2}Tour'):
    for play in tour.findall('{http://www.google.com/kml/ext/2.2}Playlist'):
        for fly in play.findall('{http://www.google.com/kml/ext/2.2}FlyTo'):
            for camera in fly.findall('{http://www.opengis.net/kml/2.2}Camera'):
                long=camera.find('{http://www.opengis.net/kml/2.2}longitude').text
                lat=camera.find('{http://www.opengis.net/kml/2.2}latitude').text
                string=string + long + ',' + lat + ' '

tree2=ET.parse('wptemplate.gml')
root2=tree2.getroot()
for coords in root2.iter('{http://www.opengis.net/gml}coordinates'):
    coords.text=string
tree2.write('convertedpath.gml')