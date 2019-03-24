import lxml.etree as ET
from shapely.geometry import LineString, Polygon
from shapely.ops import cascaded_union
from osgeo import ogr
import os

#check if folder is empty 
if len(os.listdir('output') ) != 0:
    filelist = [ f for f in os.listdir('output')]
    for f in filelist:
        os.remove(os.path.join('output', f))

#import gml file for roads
tree=ET.parse('itnout.gml')
root=tree.getroot()

#import gml file for paths
tree2=ET.parse('itnpathsout.gml')
root2=tree2.getroot()


##Create a list that will be appended with the coordinates extracted from both ITN files
polylist=[]

#Create a buffer around roads
for link in root.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}networkMember'):
    for coords in link.iter('{http://www.opengis.net/gml}coordinates'):
        coordinate=coords.text
        road=[tuple(map(float,coords.split(','))) for coords in coordinate.split()]
        c=LineString(road)
        ## changing the 50 value below changes the buffer width
        bufd=c.buffer(50,0)
        polylist.append(bufd)

        

#create a buffer around paths
for link in root2.iter('{http://www.ordnancesurvey.co.uk/xml/namespaces/osgb}networkMember'):
    for coords in link.iter('{http://www.opengis.net/gml}coordinates'):
        coordinate=coords.text
        path=[tuple(map(float,coords.split(','))) for coords in coordinate.split()]
        c=LineString(path)
        bufd=c.buffer(50,0)
        polylist.append(bufd)

 
       
#Create a combined polygon (buffer) from the all the coordinate points
combinedpoly=cascaded_union(polylist)


        ####EXPORT THE COMBINED POLYGON AS A SHP FILE ###
                
# Now convert it to a shapefile with OGR    
driver = ogr.GetDriverByName('Esri Shapefile')
ds = driver.CreateDataSource('output/buffer.shp')
layer = ds.CreateLayer('', None, ogr.wkbPolygon)
# Add one attribute
layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
defn = layer.GetLayerDefn()

## If there are multiple geometries, put the "for" loop here


# Create a new feature (attribute and geometry)
feat = ogr.Feature(defn)
feat.SetField('id', 123)

# Make a geometry, from Shapely object
geom = ogr.CreateGeometryFromWkb(combinedpoly.wkb)
feat.SetGeometry(geom)

layer.CreateFeature(feat)
feat = geom = None  # destroy these

# Save and close everything
ds = layer = feat = geom = None


#bounded area and difference
bounds=combinedpoly.bounds
area=Polygon([(bounds[0],bounds[1]),(bounds[0],bounds[3]),(bounds[2],bounds[3]),(bounds[2],bounds[1])])
freespace=area.difference(combinedpoly)

        ####EXPORT AS A SHP FILE (free area)###
                
# Now convert it to a shapefile with OGR    
driver = ogr.GetDriverByName('Esri Shapefile')
ds = driver.CreateDataSource('output/freespace.shp')
layer = ds.CreateLayer('', None, ogr.wkbPolygon)
# Add one attribute
layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
defn = layer.GetLayerDefn()

## If there are multiple geometries, put the "for" loop here


# Create a new feature (attribute and geometry)
feat = ogr.Feature(defn)
feat.SetField('id', 123)

# Make a geometry, from Shapely object
geom = ogr.CreateGeometryFromWkb(freespace.wkb)
feat.SetGeometry(geom)

layer.CreateFeature(feat)
feat = geom = None  # destroy these

# Save and close everything
ds = layer = feat = geom = None



