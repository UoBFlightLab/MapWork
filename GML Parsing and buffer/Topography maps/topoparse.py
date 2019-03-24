# -*- coding: utf-8 -*-
import lxml.etree as ET

tree=ET.parse('topo.gml')
root=tree.getroot()
for carto in root.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}cartographicMember'):
    root.remove(carto)
 

for topo in root.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}topographicMember'):
    for topoline in topo.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}TopographicLine'):
        theme=topoline.find('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}theme').text
        if theme!='Roads Tracks And Paths' and theme!='Rail':
            root.remove(topo)

for topo in root.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}topographicMember'):
    for topoarea in topo.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}TopographicArea'):
        theme2=topoarea.find('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}theme').text
        if theme2!='Roads Tracks And Paths'and theme!='Rail':
            root.remove(topo)

for topo in root.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}topographicMember'):
    for topopoint in topo.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}TopographicPoint'):
        root.remove(topo)
        
for history in root.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}changeHistory'):
    history.getparent().remove(history)    
    
for versionDate in root.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}versionDate'):
    versionDate.getparent().remove(versionDate) 
    
tree.write('outputtopo.gml')

 