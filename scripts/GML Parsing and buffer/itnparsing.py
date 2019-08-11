#import matplotlib.pyplot as plt
#from matplotlib import colors
#import numpy as np
import lxml.etree as ET
import pandas
#import shapely.geometry
tree=ET.parse('itn.gml')
root=tree.getroot()

#Remove unnecessary entries 
for other in root.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}roadMember'):
    root.remove(other)
    
for other in root.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}roadInformationMember'):
    root.remove(other)
    
for node in root.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}RoadNode'):
    parent=node.getparent()
    root.remove(parent)

for history in root.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}changeHistory'):
    history.getparent().remove(history)
    
    
#Write the output GML if necessary
tree.write('itnout.gml')

tree2=ET.parse('itnpaths.gml')
root2=tree2.getroot()

#Remove unnecessary entries 
for node in root2.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}PathNode'):
    parent=node.getparent()
    root2.remove(parent)

for other in root2.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}pathInformationMember'):
    root2.remove(other)

for other in root2.findall('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}pathMember'):
    root2.remove(other)
    
for node in root2.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}ConnectingNode'):
    parent=node.getparent()
    root2.remove(parent)
    
for node in root2.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}ConnectingLink'):
    parent=node.getparent()
    root2.remove(parent)


for history in root2.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}changeHistory'):
    history.getparent().remove(history)
    
    
#Write the output GML if necessary
tree2.write('itnpathsout.gml')

